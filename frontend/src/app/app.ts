import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PredictionService, Field, PredictionResponse } from './prediction.service';

type InputMode = 'sample' | 'csv' | 'manual';

@Component({
  selector: 'app-root', standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html', styleUrl: './app.css'
})
export class App implements OnInit {
  private readonly api = inject(PredictionService);
  readonly fields = signal<Field[]>([]);
  readonly fetched = signal(false);
  readonly loading = signal(false);
  readonly busySample = signal(false);
  readonly error = signal('');
  readonly info = signal('');
  readonly result = signal<PredictionResponse | null>(null);
  readonly mode = signal<InputMode>('sample');
  readonly csvRows = signal<Record<string, string>[]>([]);
  readonly csvName = signal('');
  readonly selectedRow = signal(0);
  readonly deployedStatic = !['localhost', '127.0.0.1'].includes(window.location.hostname);
  values: Record<string, string | number | null> = {};

  ngOnInit(): void {
    if (this.deployedStatic) return;
    this.api.schema().subscribe({
      next: schema => {
        this.fields.set(schema.features);
        this.values = Object.fromEntries(schema.features.map(f => [f.name, null]));
        this.fetched.set(true);
        this.loadSample();
      },
      error: err => this.error.set(`Unable to load schema (${err.status || 'network error'}). Start Flask and check the proxy.`)
    });
  }

  setMode(mode: InputMode): void {
    this.mode.set(mode);
    this.result.set(null);
    this.error.set('');
    this.info.set('');
    if (mode === 'sample') this.loadSample();
    if (mode === 'csv' && this.csvRows().length) this.loadCsvRow();
  }

  private populate(record: Record<string, unknown>): void {
    const updated: Record<string, string | number | null> = {};
    for (const field of this.fields()) {
      const raw = record[field.name];
      updated[field.name] = raw === null || raw === undefined || raw === ''
        ? null : field.kind === 'number' ? Number(raw) : String(raw);
    }
    this.values = updated;
  }

  loadSample(): void {
    if (this.deployedStatic || !this.fetched()) return;
    this.busySample.set(true);
    this.error.set('');
    this.api.sample().subscribe({
      next: data => {
        this.populate(data);
        this.info.set('All 83 inputs populated from the saved training sample. Ready to predict.');
        this.busySample.set(false);
      },
      error: err => {
        this.error.set(`Unable to load sample (${err.status || 'network error'}). Verify backend/test_payload.json exists.`);
        this.busySample.set(false);
      }
    });
  }

  async onCsvFile(event: Event): Promise<void> {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    this.csvRows.set([]);
    this.csvName.set('');
    this.result.set(null);
    this.error.set('');
    this.info.set('');
    if (!file) return;
    try {
      if (file.size > 8 * 1024 * 1024) throw new Error('CSV exceeds 8 MB. Export a smaller sample of rows first.');
      const content = await file.text();
      const table = this.parseCsv(content);
      if (table.length < 2) throw new Error('CSV must contain a header and at least one record.');
      const headers = table[0].map(s => s.trim());
      if (new Set(headers).size !== headers.length) throw new Error('Duplicate CSV headers are not supported.');
      const missing = this.fields().map(f => f.name).filter(f => !headers.includes(f));
      if (missing.length) throw new Error(`Missing required columns: ${missing.slice(0, 8).join(', ')}${missing.length > 8 ? '…' : ''}`);
      const rows = table.slice(1).filter(r => r.some(c => c.trim() !== '')).slice(0, 1000).map(row =>
        Object.fromEntries(headers.map((h, i) => [h, row[i] ?? '']))
      );
      if (!rows.length) throw new Error('CSV contains no data records.');
      this.csvRows.set(rows);
      this.csvName.set(file.name);
      this.selectedRow.set(0);
      this.loadCsvRow();
      this.info.set(`Loaded ${rows.length} row(s) from ${file.name}. Choose a row and predict. Extra target columns are ignored.`);
    } catch (err) {
      this.error.set(err instanceof Error ? err.message : 'Unable to read CSV.');
    } finally {
      input.value = '';
    }
  }

  loadCsvRow(): void {
    const row = this.csvRows()[this.selectedRow()];
    if (row) {
      this.populate(row);
      this.result.set(null);
      this.error.set('');
    }
  }

  // Supports quoted commas, embedded newlines, doubled quotes, and CRLF.
  private parseCsv(text: string): string[][] {
    const rows: string[][] = [];
    let row: string[] = [], cell = '', quoted = false;
    text = text.replace(/^\uFEFF/, '');
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      if (c === '"') {
        if (quoted && text[i + 1] === '"') { cell += '"'; i++; }
        else if (quoted || cell === '') quoted = !quoted;
        else throw new Error('Invalid quote in CSV.');
      } else if (!quoted && (c === ',' || c === '\n' || c === '\r')) {
        row.push(cell); cell = '';
        if (c !== ',') {
          if (row.some(v => v !== '')) rows.push(row);
          row = [];
          if (c === '\r' && text[i + 1] === '\n') i++;
        }
      } else cell += c;
    }
    if (quoted) throw new Error('Unclosed quoted CSV field.');
    if (cell !== '' || row.length) { row.push(cell); rows.push(row); }
    return rows;
  }

  submit(): void {
    this.result.set(null);
    this.error.set('');
    if (this.deployedStatic) { this.error.set('Static GitHub Pages demo only. Run Flask locally to predict.'); return; }
    if (!this.fetched()) { this.error.set('The schema has not loaded.'); return; }
    const payload: Record<string, string | number> = {};
    for (const field of this.fields()) {
      const raw = this.values[field.name];
      if (raw === null || raw === undefined || raw === '') { this.error.set(`Missing ${field.name}`); return; }
      if (field.kind === 'number') {
        const n = Number(raw);
        if (!Number.isFinite(n)) { this.error.set(`Invalid numeric value: ${field.name}`); return; }
        payload[field.name] = n;
      } else {
        const val = String(raw).trim();

        if (!val) {
          this.error.set(`Missing category: ${field.name}`);
          return;
        }

        payload[field.name] = val;
      }
    }
    this.loading.set(true);
    this.api.predict(payload).subscribe({
      next: response => { this.result.set(response); this.loading.set(false); },
      error: err => { this.error.set(err.error?.error || err.message || 'Prediction failed'); this.loading.set(false); }
    });
  }
}
