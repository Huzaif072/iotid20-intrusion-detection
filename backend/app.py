
"""
IoTID20 Intrusion Detection — Flask REST API.

Uses the locally trained Random Forest classification pipeline
and its original fitted preprocessing.

Endpoints:
    GET  /health
    GET  /schema
    GET  /sample
    POST /predict

Research/teaching prototype only.
"""

from pathlib import Path
import json
import logging

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request


# -------------------------------------------------------
# Application configuration
# -------------------------------------------------------

BASE = Path(__file__).resolve().parent
MODEL_PATH = BASE / "models" / "model_bundle.joblib"
SAMPLE_PATH = BASE / "test_payload.json"

app = Flask(__name__)

_CACHE = None


# -------------------------------------------------------
# Load trained model bundle
# -------------------------------------------------------

def get_bundle():
    global _CACHE

    if _CACHE is None:
        if not MODEL_PATH.is_file():
            raise FileNotFoundError(
                "Trained model not found. "
                "Run python scripts/train_model.py first."
            )

        # Only load artifacts created locally by trusted code.
        _CACHE = joblib.load(MODEL_PATH)

    return _CACHE


# -------------------------------------------------------
# Health endpoint
# -------------------------------------------------------

@app.get("/health")
def health():
    try:
        bundle = get_bundle()

        return jsonify(
            status="ok",
            features=len(bundle["features"]),
            task=bundle["task"],
            model_version=bundle["model_version"]
        ), 200

    except FileNotFoundError:
        return jsonify(
            status="untrained",
            message="Train the IoTID20 model before making predictions."
        ), 503


# -------------------------------------------------------
# Model input schema
# -------------------------------------------------------

@app.get("/schema")
def schema():
    try:
        bundle = get_bundle()

        feature_schema = []

        for feature in bundle["features"]:
            feature_schema.append({
                "name": feature,
                "kind": bundle["kinds"][feature],
                # These options are suggestions for the UI,
                # not a complete list of allowed categories.
                "options": bundle["categories"].get(feature, [])
            })

        return jsonify(
            features=feature_schema,
            classes=bundle["label_classes"]
        ), 200

    except FileNotFoundError:
        return jsonify(
            error="Model unavailable. Train the model first."
        ), 503


# -------------------------------------------------------
# Load sample record
# -------------------------------------------------------

@app.get("/sample")
def sample():
    if not SAMPLE_PATH.is_file():
        return jsonify(
            error="Sample payload not found."
        ), 404

    try:
        bundle = get_bundle()

        record = json.loads(
            SAMPLE_PATH.read_text(encoding="utf-8")
        )

        if not isinstance(record, dict):
            return jsonify(
                error="Sample must contain a JSON object."
            ), 500

        expected_features = set(bundle["features"])
        actual_features = set(record.keys())

        if expected_features != actual_features:
            return jsonify(
                error="Sample schema mismatch.",
                missing=sorted(expected_features - actual_features),
                extra=sorted(actual_features - expected_features)
            ), 500

        return jsonify(record), 200

    except FileNotFoundError:
        return jsonify(
            error="Trained model unavailable."
        ), 503

    except (OSError, ValueError, TypeError):
        app.logger.exception("Failed to load sample record")

        return jsonify(
            error="Unable to load sample record."
        ), 500


# -------------------------------------------------------
# Prediction endpoint
# -------------------------------------------------------

@app.post("/predict")
def predict():

    # Read JSON request
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(
            error="Expected a JSON object."
        ), 400

    # Load model
    try:
        bundle = get_bundle()

    except FileNotFoundError:
        return jsonify(
            error="Model unavailable. Train the model first."
        ), 503

    features = bundle["features"]
    kinds = bundle["kinds"]

    # Check required and unexpected features
    missing = [f for f in features if f not in data]
    extra = [f for f in data if f not in features]

    if missing or extra:
        return jsonify(
            error="Input schema mismatch.",
            missing=missing,
            extra=extra
        ), 400

    # Validate every feature
    row = {}

    for feature in features:
        value = data[feature]

        if value is None or isinstance(
            value, (dict, list, bool)
        ):
            return jsonify(
                error=f"Invalid value: {feature}"
            ), 400

        # Numeric input validation
        if kinds[feature] == "number":
            try:
                value = float(value)

                if not np.isfinite(value):
                    raise ValueError(
                        "Numeric value must be finite."
                    )

            except (TypeError, ValueError):
                return jsonify(
                    error=(
                        "Non-finite or invalid numeric value: "
                        f"{feature}"
                    )
                ), 400

        # Categorical input validation
        else:
            if not isinstance(value, str):
                return jsonify(
                    error=f"Invalid category type: {feature}"
                ), 400

            if not value.strip():
                return jsonify(
                    error=f"Empty category: {feature}"
                ), 400

            # Do not reject unseen categories.
            #
            # The fitted OneHotEncoder must support
            # handle_unknown='ignore' or an equivalent
            # unknown-category handling strategy.
            #
            # Preserve the original categorical value.
            # Do not change case or remove whitespace.

        row[feature] = value

    # Model inference
    try:
        frame = pd.DataFrame(
            [row],
            columns=features
        )

        model = bundle["pipeline"]

        prediction_index = int(
            model.predict(frame)[0]
        )

        classes = bundle["label_classes"]

        if not (0 <= prediction_index < len(classes)):
            raise ValueError(
                "Predicted class index is out of range."
            )

        prediction_label = classes[prediction_index]

        result = {
            "prediction": prediction_label,
            "prediction_index": prediction_index,
            "task": "classification",
            "model_version": bundle["model_version"],
            "disclaimer": (
                "Research/teaching prototype only; "
                "not a deployed security control."
            )
        }

        # Return probability for each class
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(frame)[0]

            result["probabilities"] = {
                str(class_label): float(probability)
                for class_label, probability in zip(
                    classes,
                    probabilities
                )
            }

        return jsonify(result), 200

    except Exception:
        app.logger.exception("Prediction failed")

        return jsonify(
            error="Prediction processing failed."
        ), 500


# -------------------------------------------------------
# Start development server
# -------------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
