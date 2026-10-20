"""Download the original IoTID20 Kaggle dataset (requires network access).
Run: python scripts/download_dataset.py
Source: https://www.kaggle.com/datasets/rohulaminlabid/iotid20-dataset
"""
from pathlib import Path
import shutil
import kagglehub
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'data'/'raw'
out.mkdir(parents=True,exist_ok=True)
path=Path(kagglehub.dataset_download('rohulaminlabid/iotid20-dataset'))
files=list(path.rglob('*.csv'))
if not files:
 raise FileNotFoundError(f'No CSV in Kaggle download directory: {path}')
for f in files:
 dst=out/f.name
 if f.resolve()!=dst.resolve(): shutil.copy2(f,dst)
 print(f'Copied {dst} ({dst.stat().st_size:,} bytes)')
print('Original source:',path)
