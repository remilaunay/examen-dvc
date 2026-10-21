"""Split raw flotation data into train/test feature and target CSV files."""
import argparse
from pathlib import Path

import pandas as pd
import yaml
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/raw_data/raw.csv")
    parser.add_argument("--output-dir", default="data/processed_data")
    parser.add_argument("--params", default="configs/params.yaml")
    args = parser.parse_args()
    with (ROOT / args.params).open() as f:
        params = yaml.safe_load(f)
    data = pd.read_csv(ROOT / args.input)
    target = "silica_concentrate"
    if target not in data.columns:
        raise ValueError(f"Target column {target!r} is absent from {args.input}")
    if data[target].isna().any():
        raise ValueError("Target contains missing values")
    features = data.drop(columns=target).select_dtypes(include="number")
    if features.empty:
        raise ValueError("No numeric feature columns were found")
    X_train, X_test, y_train, y_test = train_test_split(
        features, data[target], test_size=params["test_size"],
        random_state=params["random_state"])
    out = ROOT / args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    for name, value in (("X_train", X_train), ("X_test", X_test),
                        ("y_train", y_train), ("y_test", y_test)):
        value.to_csv(out / f"{name}.csv", index=False)


if __name__ == "__main__":
    main()
