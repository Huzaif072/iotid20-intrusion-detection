import json
from pathlib import Path
import requests
r=Path(__file__).resolve().parent
with requests.Session() as s:
 s.trust_env=False
 response=s.post('http://127.0.0.1:5000/predict',json=json.loads((r/'test_payload.json').read_text()),timeout=60)
 print(response.status_code,response.text)
 response.raise_for_status()
 print('PASS: live API request')
