"""Ingestão explícita, validação e transformação compartilhadas por treino e serving."""

import hashlib
from pathlib import Path

import httpx
import pandas as pd

from flightlab.config import DATA_PATH, DATA_URL, FEATURES, TARGET_MINUTES


def download(path: Path = DATA_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    response = httpx.get(DATA_URL, follow_redirects=True, timeout=120)
    response.raise_for_status()
    temporary = path.with_suffix(".tmp")
    temporary.write_bytes(response.content)
    try:
        prepare(pd.read_csv(temporary))
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
    return path


def prepare(raw: pd.DataFrame) -> pd.DataFrame:
    required = {"year", "month", "day", "arr_delay", "carrier", "origin", "dest", "distance"}
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"Colunas ausentes: {sorted(missing)}")
    df = raw.copy()
    for col in ["year", "month", "day", "arr_delay", "distance"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["date"] = pd.to_datetime(df[["year", "month", "day"]], errors="coerce")
    df["day_of_week"] = df["date"].dt.day_of_week
    df = df.dropna(subset=FEATURES + ["date", "arr_delay"])
    df = df.loc[df["distance"].gt(0)].copy()
    df["delayed"] = df["arr_delay"].ge(TARGET_MINUTES).astype(int)
    df["route"] = df["origin"] + " → " + df["dest"]
    return df.sort_values("date", kind="stable").reset_index(drop=True)


def load(path: Path = DATA_PATH) -> tuple[pd.DataFrame, dict]:
    if not path.exists():
        raise FileNotFoundError("Base ausente. Execute: flightlab download")
    raw = pd.read_csv(path)
    df = prepare(raw)
    quality = {
        "raw_rows": len(raw),
        "usable_rows": len(df),
        "excluded_rows": len(raw) - len(df),
        "missing_arrival_delay": int(raw["arr_delay"].isna().sum()),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "source": DATA_URL,
    }
    return df, quality
