# 15-stage lab-manual evidence/checklist

| Stage | Delivered | Status / action required |
|---|---|---|
| 1 | Paper provenance, task, 83 raw candidate features, model metadata | Source confirmed; dataset raw input must be inspected locally |
| 2 | Requirements and setup commands | Install Python 3.12, Git, Node.js 22+, npm, Angular dependencies |
| 3 | Root folders and environment procedure | Create `.venv` locally |
| 4 | Re-train baseline and export fitted `model_bundle.joblib` | Requires original dataset download |
| 5 | Generator of sample payload; direct inference script | Requires training |
| 6 | Flask GET `/health`, GET `/schema`, POST `/predict` | Source ready; run locally after training |
| 7 | Mocked API tests and real requests script | Mock tests CI-safe; real API requires model |
| 8 | Angular scaffold and configuration | `npm install` and `npm start` on user's PC |
| 9 | Dynamically populated feature form from exact trained model | Angular app source ready |
| 10 | Dev proxy `/api/*` to Flask | Needs user machine end-to-end verification |
| 11 | `.gitignore`; root folder layout | `git init` and commit locally |
| 12 | GitHub remote | Requires GitHub account and user authorization |
| 13 | CI workflow for backend mock tests and frontend build | Commit and inspect Actions runs |
| 14 | Static Pages workflow; static-only notice | Requires user GitHub repository settings |
| 15 | README, research notes, checklist | User screenshots, run URLs, live testing required |

Never report GitHub CI, deployment or reproduction as completed without verifiable runs.
