"""Find and persist the best random forest hyperparameters."""
import argparse
import json
from pathlib import Path

import pandas as pd
import yaml
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/processed_data")
    parser.add_argument("--params", default="configs/params.yaml")
    parser.add_argument("--output", default="models/best_params.json")
    args = parser.parse_args()
    with (ROOT / args.params).open() as f:
        cfg = yaml.safe_load(f)
    folder = ROOT / args.input_dir
    X = pd.read_csv(folder / "X_train_scaled.csv")
    y = pd.read_csv(folder / "y_train.csv").squeeze("columns")
    model_cfg = cfg["model"]
    if model_cfg["name"] != "RandomForestRegressor":
        raise ValueError("Only RandomForestRegressor is currently supported")
    search = GridSearchCV(RandomForestRegressor(random_state=cfg["random_state"], n_jobs=1),
                          model_cfg["grid"], cv=cfg["cv"], scoring="neg_mean_squared_error", n_jobs=1)
    search.fit(X, y)
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(search.best_params_, indent=2) + "\n")


if __name__ == "__main__":
    main()
