from __future__ import annotations

import argparse
from pathlib import Path

import joblib
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42


def train_and_save(output_path: str | Path = "model/model.joblib") -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    x, y = make_classification(
        n_samples=400,
        n_features=3,
        n_informative=3,
        n_redundant=0,
        n_clusters_per_class=1,
        class_sep=1.2,
        random_state=RANDOM_STATE,
    )
    estimator = Pipeline(
        [
            ("scale", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=500, random_state=RANDOM_STATE)),
        ]
    )
    estimator.fit(x, y)
    joblib.dump({"estimator": estimator, "labels": {0: "low", 1: "high"}}, output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the synthetic TSI lab model.")
    parser.add_argument("--output", default="model/model.joblib")
    args = parser.parse_args()
    path = train_and_save(args.output)
    print(f"Model written to {path}")


if __name__ == "__main__":
    main()
