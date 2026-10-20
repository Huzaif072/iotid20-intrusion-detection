# IoTID20 Input Usability Upgrade

Update for your **existing trained project** (Windows 10): adds one-click sample loading, local CSV upload with row selection, and optional manual entry. **Does not retrain or replace your model.**

## 1. Back up your current code

From `D:\Huzaif\iotid20_lab` in PowerShell:

```powershell
Copy-Item frontend\src\app\app.ts frontend\src\app\app.ts.bak
Copy-Item frontend\src\app\app.html frontend\src\app\app.html.bak
Copy-Item frontend\src\app\app.css frontend\src\app\app.css.bak
Copy-Item frontend\src\app\prediction.service.ts frontend\src\app\prediction.service.ts.bak
Copy-Item backend\app.py backend\app.py.bak
```

## 2. Copy the four frontend files from this upgrade package

Copy `frontend/src/app/app.ts`, `app.html`, `app.css`, and `prediction.service.ts` to the **same paths** in your existing project, replacing the old frontend files. Do not overwrite the whole project or the trained model.

## 3. Add ONE Flask route to your existing `backend/app.py`

Insert this before its last `if __name__ == '__main__':` line:

```python
@app.get('/sample')
def sample():
    """Local development sample, generated during model training."""
    import json
    path = BASE / 'test_payload.json'
    if not path.is_file():
        return jsonify(error='Sample payload not found. Run training first.'), 404
    try:
        record = json.loads(path.read_text(encoding='utf-8'))
        bundle = get_bundle()
        expected = set(bundle['features'])
        if not isinstance(record, dict) or set(record) != expected:
            return jsonify(error='Sample record does not match model feature schema'), 500
        return jsonify(record)
    except (OSError, ValueError) as exc:
        app.logger.warning('Sample loading failed: %s', exc)
        return jsonify(error='Unable to read sample record'), 500
```

This endpoint reads only the model's already generated `backend/test_payload.json`. No data/model files are modified. Keep Flask bound to `127.0.0.1`, as in the existing project.

## 4. Restart and test

From your project root, with virtual environment activated:

```powershell
python backend\app.py
```

In another terminal:

```powershell
curl.exe --noproxy "*" -i http://127.0.0.1:5000/sample
```

Expected: `HTTP 200` and a JSON object with **83 input keys**.

In the Angular terminal:

```powershell
cd frontend
npm run build
npm start
```

Open `http://localhost:4200` and click **Load sample**, then **Predict network flow**. Alternatively choose **Upload CSV**, load a CSV with all 83 input columns, select a row, and predict. **Advanced manual input** preserves the full editable form.

## CSV limitations and safety

- The CSV never leaves the browser; only the selected record is posted to `/api/predict`.
- Maximum file size is **8 MB**. Only the first **1,000 non-empty records** can be selected. Export a small representative CSV rather than uploading the full dataset.
- Column names must match the 83 trained input feature names exactly (order can differ); extra columns, including targets, are ignored.
- The chosen row must contain valid numeric values and categories recognized by your trained model.
- Uploaded content is for local research demonstration only. Avoid sensitive or private traffic logs.

## Troubleshooting

- `GET /api/sample` 404: Flask route not added, Flask not restarted, or `backend/test_payload.json` is missing.
- Sample loads but prediction fails: regenerate `test_payload.json` from the current trained model, then recheck the schema.
- Angular build fails: ensure all **four frontend files** were copied together and avoid mixing old signal-based templates with new source.
- Schema still loading: check `http://localhost:4200/api/schema` and restart Angular with `npm start`.
