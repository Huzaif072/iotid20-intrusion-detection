# IoTID20 Intrusion Detection System

**A Full-Stack Machine Learning and DevOps Research Prototype**

An IoT network intrusion detection system developed using Python, Scikit-learn, Flask, Angular, Git, GitHub Actions, and GitHub Pages.

The project trains a Random Forest classifier on the IoTID20 dataset, exposes the fitted model through a REST API, and provides a web interface for classifying network traffic as **Normal** or **Anomaly**.

## Live Project

| Resource | Link |
|---|---|
| GitHub Repository | [View Source Code](https://github.com/Huzaif072/iotid20-intrusion-detection) |
| GitHub Pages | [View Static Website](https://huzaif072.github.io/iotid20-intrusion-detection/) |
| GitHub Actions | [View CI/CD Workflows](https://github.com/Huzaif072/iotid20-intrusion-detection/actions) |
| Dataset | [IoTID20 on Kaggle](https://www.kaggle.com/datasets/rohulaminlabid/iotid20-dataset) |

**Note:** The deployed GitHub Pages website is a static demonstration. Live predictions require the Flask backend and trained model running locally.

---

## 1. Project Overview

Internet of Things (IoT) environments generate large volumes of network traffic and can be vulnerable to cyberattacks.

This project explores the use of machine learning for binary IoT network intrusion detection.

The application accepts 83 network traffic features, processes them using a fitted Scikit-learn pipeline, and predicts whether the supplied network flow is normal or anomalous.

### Project Objectives

- Use a real-world IoT intrusion detection dataset.
- Prepare and preprocess network traffic data.
- Train and evaluate a binary classification model.
- Save the complete fitted machine learning pipeline.
- Develop a REST API using Flask.
- Build an interactive frontend using Angular.
- Integrate frontend and backend components.
- Implement automated backend tests.
- Configure continuous integration using GitHub Actions.
- Deploy a static Angular demonstration using GitHub Pages.

## 2. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.12 |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Model Serialization | Joblib |
| Backend | Flask |
| Frontend | Angular 22, TypeScript |
| Frontend Runtime | Node.js 24 |
| Testing | Pytest |
| Version Control | Git |
| Repository Hosting | GitHub |
| Continuous Integration | GitHub Actions |
| Static Deployment | GitHub Pages |
| Research Environment | Jupyter Notebook |

## 3. Dataset Information

**Dataset:** IoTID20 (IoT Intrusion Detection Dataset 2020)

**Source:** [Kaggle — IoTID20 Dataset](https://www.kaggle.com/datasets/rohulaminlabid/iotid20-dataset)

The dataset contains network flow information relevant to detecting attacks against IoT networks.

| Property | Value |
|---|---|
| Dataset | IoTID20 |
| Records processed locally | 625,783 |
| Original columns | 86 |
| Target columns excluded from predictors | `Label`, `Cat`, `Sub_Cat` |
| Original input features | 83 |
| Classification task | Binary |
| Target classes | Anomaly, Normal |
| Training percentage | 80% |
| Testing percentage | 20% |
| Random state | 42 |

The dataset is downloaded separately and is not committed to this repository.

The pipeline uses the `Label` column as its binary classification target.

## 4. Research Paper

**Title:** Attention-Enhanced Hybrid Deep Learning for Intrusion Detection in IoT Networks

**Authors:** Zaki, Yaseen, Imran, and Kazim

**Published:** 2026

**Journal:** IET Networks

**DOI:** https://doi.org/10.1049/ntw2.70037

The referenced study investigates intrusion detection using a hybrid deep learning architecture that combines convolutional neural networks, gated recurrent units, and attention mechanisms.

### Research Reproduction Scope

This repository contains a research notebook exploring the paper's methodology and a separate deployable Random Forest baseline.

**The deployed Random Forest does not reproduce the paper's CNN–GRU–attention architecture.**

Results from the local Random Forest experiment must therefore be interpreted independently of the paper's published results.

Differences in dataset versions, preprocessing, class balancing, feature selection, architecture, and evaluation procedures may affect comparisons.

## 5. Machine Learning Pipeline

The deployable model uses a Scikit-learn pipeline with the following stages:

1. Load the IoTID20 CSV data.
2. Identify the binary target column.
3. Remove target columns from the predictors.
4. Separate numerical and categorical features.
5. Impute missing values.
6. Scale numeric features.
7. Encode categorical features using One-Hot Encoding.
8. Apply ANOVA-based feature selection.
9. Train a Random Forest classifier.
10. Evaluate the model on the held-out test set.
11. Save the fitted pipeline and feature metadata.

### Model Configuration

| Parameter | Value |
|---|---|
| Algorithm | Random Forest Classifier |
| Number of estimators | 50 |
| Maximum tree depth | 15 |
| Minimum samples per leaf | 4 |
| Maximum features | sqrt |
| Random state | 42 |
| Feature selection | SelectKBest, ANOVA F-test |
| Selected encoded features | Up to 70 |
| Split | Stratified 80/20 |

The saved model bundle includes preprocessing, feature selection, classification, feature names, input types, class labels, and model version information.

## 6. Experimental Results

The Random Forest model was trained using all 625,783 locally processed records.

### Full-Dataset Evaluation

| Metric | Result |
|---|---:|
| Accuracy | 99.8666% |
| Weighted F1-score | 99.8659% |
| Macro F1-score | 99.4380% |
| Training records | 500,626 |
| Testing records | 125,157 |
| Original input features | 83 |

These are the locally observed results of the Random Forest baseline, not the published CNN–GRU model.

**Evaluation limitation:** These results use a stratified random record-level split. Potential dependencies among network flows, duplicated records, identifiers, IP addresses, and timestamps may produce optimistic estimates. The reported accuracy should not be interpreted as validated performance against previously unseen networks or attacks.

The generated evaluation data is saved locally in:

`docs/actual_metrics.json`

This file is excluded from Git because it is generated during training.

## 7. Project Structure

```text
iotid20_lab/
|
|-- .github/
|   |-- workflows/
|       |-- ci.yml
|       |-- pages.yml
|
|-- backend/
|   |-- app.py
|   |-- requirements.txt
|   |-- test_api.py
|   |-- test_pipeline.py
|   |-- tests/
|   |-- models/                 # Generated locally
|   |-- test_payload.json       # Generated locally
|
|-- data/
|   |-- raw/                    # Downloaded dataset
|   |-- sample_inputs.csv       # Generated sample
|
|-- docs/
|   |-- research_notes.md
|   |-- stages_status.md
|   |-- actual_metrics.json     # Generated metrics
|
|-- frontend/
|   |-- src/
|   |-- public/
|   |-- angular.json
|   |-- package.json
|   |-- package-lock.json
|   |-- proxy.conf.json
|
|-- notebooks/
|   |-- IoTID20_Research_Reproduction.ipynb
|
|-- scripts/
|   |-- download_dataset.py
|   |-- train_model.py
|
|-- .gitignore
|-- README.md
|-- requirements-training.txt
```

Generated datasets, model artifacts, evaluation output, virtual environments, and Node.js dependencies are not included in the repository.

## 8. Installation and Setup

### Prerequisites

Install:

- Python 3.12
- Node.js 24
- Git
- A code editor such as Visual Studio Code

The following instructions use Windows PowerShell.

### Step 1 — Clone the Repository

```powershell
git clone https://github.com/Huzaif072/iotid20-intrusion-detection.git
cd iotid20-intrusion-detection
```

### Step 2 — Create a Python Virtual Environment

```powershell
py -3.12 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### Step 3 — Install Python Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
python -m pip install -r requirements-training.txt
python -m pip install kagglehub
```

### Step 4 — Download IoTID20

```powershell
python scripts\download_dataset.py
```

The downloader obtains the dataset from Kaggle and places the CSV files under `data/raw/`.

Internet access is required. Kaggle authentication may also be required depending on the download environment.

### Step 5 — Train the Model

```powershell
python scripts\train_model.py
```

Training uses the available labeled dataset records by default.

For a smaller debugging run, you can optionally use:

```powershell
python scripts\train_model.py --max-rows 100000
```

The reduced run is for development and should not be confused with the full-dataset results reported above.

Training generates files including:

- `backend/models/model_bundle.joblib`
- `backend/test_payload.json`
- `data/sample_inputs.csv`
- `docs/actual_metrics.json`

Model artifacts are generated locally and excluded from Git.

**Security:** Only load model bundles created by trusted sources. Joblib model files can execute code when deserialized.

## 9. Running the Flask Backend

From the project root, with the virtual environment active:

```powershell
python backend\app.py
```

The Flask development server runs at:

`http://127.0.0.1:5000`

### REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Model readiness and metadata |
| GET | `/schema` | Expected input features and classes |
| GET | `/sample` | Saved sample network flow |
| POST | `/predict` | Predict traffic classification |

The prediction endpoint accepts a JSON object containing all 83 required features.

It returns a predicted class, class index, class probabilities, model version, and a research-use disclaimer.

### Test Model Readiness

```powershell
curl.exe --noproxy "*" http://127.0.0.1:5000/health
```

When the trained model is available, the endpoint reports that the model is ready.

### Test a Real Prediction

In a second terminal, with Flask running:

```powershell
python backend\test_api.py
```

This script submits a saved input record to the live API.

## 10. Running the Angular Frontend

Open a separate terminal.

```powershell
cd frontend
npm install
npm start
```

Open:

`http://localhost:4200`

The Angular development server uses a proxy configuration to forward API requests to the locally running Flask backend.

### Input Methods

The interface provides three input methods:

**Load Sample:** Automatically populates the 83 features using the saved sample record.

**Upload CSV:** Allows the user to choose a local CSV file and select a row for classification.

**Advanced Manual Input:** Provides the complete feature input form for entering values manually.

CSV upload is intended for small local demonstrations. The interface limits file size and the number of selectable rows.

### Prediction Output

After submitting a valid network flow, the application displays:

- Predicted traffic category
- Normal class probability
- Anomaly class probability
- Research prototype disclaimer

The application is a research demonstration rather than a production intrusion prevention system.

## 11. Automated Testing

The project includes backend tests using Pytest.

Run:

```powershell
python -m pytest -q backend\tests
```

These tests use a mock classifier to verify API behavior without requiring the full IoTID20 dataset or the trained model.

Test cases cover:

- Health endpoint
- Valid predictions
- Missing features
- Invalid JSON requests
- Unexpected input fields
- Invalid numeric values
- Unknown categorical values
- Empty categorical values
- Missing sample file

For an additional live integration test, run:

```powershell
python backend\test_api.py
```

The live integration test requires the trained model and running Flask server.

## 12. Continuous Integration

GitHub Actions automatically checks the project when changes are pushed to the `main` branch or submitted through a pull request.

**Workflow:** `.github/workflows/ci.yml`

The workflow includes:

**Backend CI**
- Set up Python 3.12.
- Install backend dependencies.
- Execute Pytest API tests.

**Frontend CI**
- Set up Node.js 24.
- Install frontend dependencies.
- Build the Angular application.

The CI workflow does not retrain the full Random Forest model or reproduce the research paper.

[View GitHub Actions](https://github.com/Huzaif072/iotid20-intrusion-detection/actions)

## 13. GitHub Pages Deployment

**Workflow:** `.github/workflows/pages.yml`

The workflow builds the Angular application for GitHub Pages and deploys the generated static files.

**Public URL:**

https://huzaif072.github.io/iotid20-intrusion-detection/

### Deployment Limitation

GitHub Pages supports static frontend hosting. It does not run the Flask backend or host the trained Python model.

Therefore:

| Environment | Functionality |
|---|---|
| Local Angular + Flask | Complete network traffic prediction |
| GitHub Pages | Static demonstration of the frontend |

For real predictions, use the local development environment with Flask and the trained model available.

## 14. Reproducibility and Limitations

This project is intended for academic research and DevOps education.

Important limitations include:

- The deployed model is a Random Forest baseline, not the paper's CNN–GRU–attention model.
- The saved model is not distributed through the Git repository.
- The original dataset must be downloaded separately.
- Results may differ across dataset versions and software environments.
- The reported accuracy is based on a record-level train/test split.
- The system has not been validated as a production security control.
- GitHub Pages cannot provide server-side inference.
- CI tests validate application behavior but do not establish model accuracy or paper reproduction.

## 15. Future Improvements

Potential extensions include:

- Group-aware or time-based data splitting.
- Duplicate-flow and identifier-leakage analysis.
- Additional intrusion detection metrics and comparisons.
- Broader validation on unseen network environments.
- Authenticated API deployment.
- Secure hosted model inference.
- Expanded frontend visualizations.
- Monitoring and model performance tracking.

These are possible future improvements and are not claimed as implemented features.

## 16. References

1. [IoTID20 Dataset — Kaggle](https://www.kaggle.com/datasets/rohulaminlabid/iotid20-dataset)
2. Zaki, Yaseen, Imran, and Kazim (2026), *Attention-Enhanced Hybrid Deep Learning for Intrusion Detection in IoT Networks*, IET Networks. https://doi.org/10.1049/ntw2.70037
3. [Scikit-learn Documentation](https://scikit-learn.org/)
4. [Flask Documentation](https://flask.palletsprojects.com/)
5. [Angular Documentation](https://angular.dev/)
6. [GitHub Actions Documentation](https://docs.github.com/en/actions)
7. [GitHub Pages Documentation](https://docs.github.com/en/pages)

---

## Disclaimer

This software is provided for academic and research purposes only. It is not intended to replace professionally validated network security monitoring, threat detection, or intrusion prevention systems.