from pathlib import Path
def test_source_files_exist():
 r=Path(__file__).resolve().parents[2]
 for f in ['backend/app.py','scripts/train_model.py','frontend/package.json','README.md','.github/workflows/ci.yml']:
  assert (r/f).exists(),f
