import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
export interface Field { name: string; kind: 'number' | 'category'; options: string[]; }
export interface ModelSchema { features: Field[]; classes: string[]; }
export interface PredictionResponse { prediction: string; probabilities?: Record<string, number>; disclaimer: string; model_version: string; }
@Injectable({providedIn: 'root'})
export class PredictionService {
  private readonly http = inject(HttpClient);
  schema() { return this.http.get<ModelSchema>('/api/schema'); }
  sample() { return this.http.get<Record<string, string | number>>('/api/sample'); }
  predict(values: Record<string, string | number>) { return this.http.post<PredictionResponse>('/api/predict', values); }
}
