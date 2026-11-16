"""Classificação pré-voo com holdouts por data e baseline explícito."""

import json
from datetime import UTC, datetime
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from flightlab.config import ARTIFACTS, CATEGORICAL, FEATURES, NUMERIC


def temporal_split(df):
    dates = df["date"].drop_duplicates().sort_values().tolist()
    if len(dates) < 10:
        raise ValueError("São necessárias pelo menos dez datas distintas")
    train_end = dates[int(len(dates) * 0.65)]
    validation_end = dates[int(len(dates) * 0.82)]
    return (
        df.loc[df["date"] < train_end],
        df.loc[(df["date"] >= train_end) & (df["date"] < validation_end)],
        df.loc[df["date"] >= validation_end],
    )


def scores(y, probability):
    predicted = probability >= 0.5
    return {
        "roc_auc": float(roc_auc_score(y, probability)),
        "average_precision": float(average_precision_score(y, probability)),
        "brier": float(brier_score_loss(y, probability)),
        "precision_at_0_5": float(precision_score(y, predicted, zero_division=0)),
        "recall_at_0_5": float(recall_score(y, predicted, zero_division=0)),
        "prevalence": float(y.mean()),
    }


def train(df: pd.DataFrame, quality: dict, directory: Path = ARTIFACTS) -> dict:
    train_df, validation, test = temporal_split(df)
    for partition in (train_df, validation, test):
        if partition["delayed"].nunique() != 2:
            raise ValueError("Cada partição precisa de voos com e sem atraso")
    preprocessing = ColumnTransformer(
        [
            ("categories", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
            (
                "numeric",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="median")),
                        ("scale", StandardScaler()),
                    ]
                ),
                NUMERIC,
            ),
        ]
    )
    pipeline = Pipeline(
        [
            ("preprocess", preprocessing),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )
    pipeline.fit(train_df[FEATURES], train_df["delayed"])
    baseline = DummyClassifier(strategy="prior").fit(train_df[FEATURES], train_df["delayed"])
    metrics = {
        "created_at": datetime.now(UTC).isoformat(),
        "sklearn_version": sklearn.__version__,
        "features": FEATURES,
        "target": "arr_delay >= 15 minutos",
        "decision_threshold": 0.5,
        "quality": quality,
        "partitions": {},
        "limitations": [
            "Base histórica de 2013; não validado para operação atual.",
            "Sem clima, congestionamento ou horário programado na base original.",
            "Voos sem atraso de chegada registrado são excluídos; não prevê cancelamento.",
            "Probabilidade estimada; calibração não garantida em períodos futuros.",
        ],
    }
    for name, partition in [("train", train_df), ("validation", validation), ("test", test)]:
        metrics["partitions"][name] = {
            "rows": len(partition),
            "start": str(partition["date"].min().date()),
            "end": str(partition["date"].max().date()),
        }
    for name, partition in [("validation", validation), ("test", test)]:
        metrics[name] = scores(
            partition["delayed"], pipeline.predict_proba(partition[FEATURES])[:, 1]
        )
        metrics[f"baseline_{name}"] = scores(
            partition["delayed"], baseline.predict_proba(partition[FEATURES])[:, 1]
        )
    coefficients = pipeline.named_steps["classifier"].coef_[0]
    names = preprocessing.get_feature_names_out()
    metrics["global_coefficients"] = sorted(
        [{"feature": str(n), "coefficient": float(v)} for n, v in zip(names, coefficients)],
        key=lambda item: abs(item["coefficient"]),
        reverse=True,
    )[:20]
    directory.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": pipeline, "metrics": metrics}, directory / "model.joblib")
    (directory / "metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return metrics


def load_model(directory: Path = ARTIFACTS):
    path = directory / "model.joblib"
    if not path.exists():
        raise FileNotFoundError("Modelo ausente. Execute: flightlab train")
    # Carregar apenas artefatos locais confiáveis: joblib não é seguro para uploads.
    return joblib.load(path)


def predict(bundle: dict, flight: dict) -> dict:
    date = pd.Timestamp(flight["date"])
    row = {key: flight[key] for key in CATEGORICAL}
    row.update(month=date.month, day_of_week=date.day_of_week, distance=flight["distance"])
    encoder = bundle["pipeline"].named_steps["preprocess"].named_transformers_["categories"]
    unknown = [
        col
        for col, categories in zip(CATEGORICAL, encoder.categories_)
        if row[col] not in categories
    ]
    probability = float(bundle["pipeline"].predict_proba(pd.DataFrame([row])[FEATURES])[0, 1])
    return {
        "probability": probability,
        "delayed": probability >= 0.5,
        "threshold_minutes": 15,
        "unknown_categories": unknown,
        "warning": "Estimativa educacional baseada em 2013; não é previsão operacional atual.",
    }
