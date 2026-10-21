"""Train and persist the selected regression model."""
import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
import yaml
from sklearn.ensemble import RandomForestRegressor

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/processed_data")
    parser.add_argument("--params", default="configs/params.yaml")
    parser.add_argument("--best-params", default="models/best_params.json")
    parser.add_argument("--output", default="models/model.pkl")
    args = parser.parse_args()
    cfg = yaml.safe_load((ROOT / args.params).read_text())
    best = json.loads((ROOT / args.best_params).read_text())
    folder = ROOT / args.input_dir
    X = pd.read_csv(folder / "X_train_scaled.csv")
    y = pd.read_csv(folder / "y_train.csv").squeeze("columns")
    model = RandomForestRegressor(random_state=cfg["random_state"], n_jobs=cfg["model"]["n_jobs"], **best)
    model.fit(X, y)
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output)


if __name__ == "__main__":
    main()
