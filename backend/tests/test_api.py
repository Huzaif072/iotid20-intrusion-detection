
"""
IoTID20 Flask API — Automated Tests

Uses a mock model so GitHub Actions can run these
tests without downloading or training the IoTID20 dataset.

Tests:
1. Health endpoint
2. Valid prediction
3. Missing features
4. Invalid JSON
5. Extra and invalid inputs
6. Unknown categorical values
7. Empty categorical values
8. Sample endpoint
"""

import sys
from pathlib import Path
from unittest.mock import patch

import numpy as np

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

import app as api


# -------------------------------------------------------
# Mock trained model
# -------------------------------------------------------

class FakePipe:
    def predict(self, frame):
        return np.array([1])

    def predict_proba(self, frame):
        return np.array([[0.1, 0.9]])


MOCK = {
    "features": ["Flow Duration", "Protocol"],
    "kinds": {
        "Flow Duration": "number",
        "Protocol": "category"
    },
    "categories": {
        "Protocol": ["TCP", "UDP"]
    },
    "label_classes": ["Normal", "Attack"],
    "pipeline": FakePipe(),
    "model_version": "test-double",
    "task": "classification"
}


# -------------------------------------------------------
# Mock Flask client
# -------------------------------------------------------

def client():
    with patch.object(
        api,
        "get_bundle",
        return_value=MOCK
    ):
        yield api.app.test_client()


# -------------------------------------------------------
# Test 1 — Health endpoint
# -------------------------------------------------------

def test_health():
    for c in client():
        response = c.get("/health")

        assert response.status_code == 200
        assert response.json["status"] == "ok"
        assert response.json["features"] == 2
        assert response.json["task"] == "classification"


# -------------------------------------------------------
# Test 2 — Valid prediction
# -------------------------------------------------------

def test_predict_valid():
    for c in client():
        response = c.post(
            "/predict",
            json={
                "Flow Duration": 4.2,
                "Protocol": "TCP"
            }
        )

        assert response.status_code == 200
        assert response.json["prediction"] == "Attack"
        assert response.json["prediction_index"] == 1

        probabilities = response.json["probabilities"]

        assert probabilities["Normal"] == 0.1
        assert probabilities["Attack"] == 0.9


# -------------------------------------------------------
# Test 3 — Missing feature
# -------------------------------------------------------

def test_predict_missing_feature():
    for c in client():
        response = c.post(
            "/predict",
            json={
                "Protocol": "TCP"
            }
        )

        assert response.status_code == 400
        assert response.json["error"] == "Input schema mismatch."


# -------------------------------------------------------
# Test 4 — Invalid JSON
# -------------------------------------------------------

def test_predict_invalid_json():
    for c in client():
        response = c.post(
            "/predict",
            data="broken",
            content_type="application/json"
        )

        assert response.status_code == 400


# -------------------------------------------------------
# Test 5 — Extra and invalid inputs
# -------------------------------------------------------

def test_extra_and_invalid():
    for c in client():

        # Extra feature
        response = c.post(
            "/predict",
            json={
                "Flow Duration": 1,
                "Protocol": "TCP",
                "extra": 2
            }
        )

        assert response.status_code == 400

        # Infinite numeric value
        response = c.post(
            "/predict",
            json={
                "Flow Duration": "inf",
                "Protocol": "TCP"
            }
        )

        assert response.status_code == 400

        # Invalid numeric string
        response = c.post(
            "/predict",
            json={
                "Flow Duration": "invalid",
                "Protocol": "TCP"
            }
        )

        assert response.status_code == 400


# -------------------------------------------------------
# Test 6 — Unknown category is accepted
# -------------------------------------------------------

def test_predict_unknown_category():
    for c in client():

        response = c.post(
            "/predict",
            json={
                "Flow Duration": 1,
                "Protocol": "SMB"
            }
        )

        # Unknown nonempty categories are allowed.
        assert response.status_code == 200
        assert response.json["prediction"] == "Attack"


# -------------------------------------------------------
# Test 7 — Empty category is rejected
# -------------------------------------------------------

def test_predict_empty_category():
    for c in client():

        response = c.post(
            "/predict",
            json={
                "Flow Duration": 1,
                "Protocol": ""
            }
        )

        assert response.status_code == 400

        # Whitespace-only category
        response = c.post(
            "/predict",
            json={
                "Flow Duration": 1,
                "Protocol": "   "
            }
        )

        assert response.status_code == 400


# -------------------------------------------------------
# Test 8 — Sample endpoint handles missing file
# -------------------------------------------------------

def test_sample_missing_file():
    with patch.object(
        api,
        "SAMPLE_PATH",
        Path("__missing_test_sample__.json")
    ):
        response = api.app.test_client().get("/sample")

        assert response.status_code == 404
        assert "error" in response.json
