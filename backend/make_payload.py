from pathlib import Path
import json
import joblib
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
b=joblib.load(ROOT/'backend/models/model_bundle.joblib')
df=pd.read_csv(ROOT/'data/sample_inputs.csv',nrows=1)
payload={c:(None if pd.isna(df.loc[0,c]) else df.loc[0,c].item() if hasattr(df.loc[0,c],'item') else df.loc[0,c]) for c in b['features']}
(ROOT/'backend/test_payload.json').write_text(json.dumps(payload,indent=2))
print('Payload written, features:',len(payload))
