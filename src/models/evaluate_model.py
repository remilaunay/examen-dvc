"""Evaluate the trained model and save predictions and regression metrics."""
import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/processed_data")
    parser.add_argument("--model", default="models/model.pkl")
    parser.add_argument("--predictions", default="data/predictions.csv")
    parser.add_argument("--metrics", default="metrics/scores.json")
    args = parser.parse_args()
    folder = ROOT / args.input_dir
    X = pd.read_csv(folder / "X_test_scaled.csv")
    y = pd.read_csv(folder / "y_test.csv").squeeze("columns")
    model = joblib.load(ROOT / args.model)
    prediction = model.predict(X)
    pred_path = ROOT / args.predictions
    pred_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"y_true": y, "y_pred": prediction}).to_csv(pred_path, index=False)
    scores = {"mse": float(mean_squared_error(y, prediction)),
              "rmse": float(mean_squared_error(y, prediction) ** 0.5),
              "mae": float(mean_absolute_error(y, prediction)),
              "r2": float(r2_score(y, prediction))}
    metrics_path = ROOT / args.metrics
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(scores, indent=2) + "\n")


if __name__ == "__main__":
    main()
