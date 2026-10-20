import json
from pathlib import Path
import joblib,pandas as pd
r=Path(__file__).resolve().parents[1]
b=joblib.load(r/'backend/models/model_bundle.joblib')
x=json.loads((r/'backend/test_payload.json').read_text())
assert set(x)==set(b['features'])
y=b['pipeline'].predict(pd.DataFrame([x],columns=b['features']))
print('PASS local inference:',y.tolist())
