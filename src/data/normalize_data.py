"""Fit feature scaling on training data and transform train and test sets."""
import argparse
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/processed_data")
    args = parser.parse_args()
    folder = ROOT / args.input_dir
    train = pd.read_csv(folder / "X_train.csv")
    test = pd.read_csv(folder / "X_test.csv")
    scaler = StandardScaler().fit(train)
    pd.DataFrame(scaler.transform(train), columns=train.columns).to_csv(folder / "X_train_scaled.csv", index=False)
    pd.DataFrame(scaler.transform(test), columns=test.columns).to_csv(folder / "X_test_scaled.csv", index=False)


if __name__ == "__main__":
    main()
