import numpy as np
import pandas as pd
import pytest

from flightlab.analytics import ranking, summary
from flightlab.config import FEATURES
from flightlab.data import prepare
from flightlab.model import load_model, predict, temporal_split, train


def test_target_boundary_and_missing_arrival(flights):
    raw = flights.iloc[:4].copy()
    raw["arr_delay"] = [-1, 14, 15, np.nan]
    cleaned = prepare(raw)
    assert cleaned.delayed.tolist() == [0, 0, 1]
    assert len(cleaned) == 3


def test_schema_validation():
    with pytest.raises(ValueError, match="Colunas ausentes"):
        prepare(pd.DataFrame({"foo": [1]}))


def test_temporal_split_never_shares_dates(flights):
    training, validation, test = temporal_split(flights)
    assert training.date.max() < validation.date.min()
    assert validation.date.max() < test.date.min()
    assert len(training) + len(validation) + len(test) == len(flights)
    assert not {"arr_delay", "dep_delay", "dep_time", "arr_time", "air_time"} & set(FEATURES)


def test_ranking_uses_rates_and_minimum(flights):
    ranked = ranking(flights, "carrier", min_flights=301)
    assert ranked.empty
    stats = summary(flights)
    assert stats["delay_rate"] == pytest.approx(0.4)
    assert summary(flights.iloc[:0])["flights"] == 0


def test_training_serialization_and_unseen_category(flights, tmp_path):
    metrics = train(flights, {"source": "fixture"}, tmp_path)
    bundle = load_model(tmp_path)
    result = predict(
        bundle,
        {"date": "2013-03-01", "carrier": "ZZ", "origin": "JFK", "dest": "LAX", "distance": 2475},
    )
    assert 0 <= result["probability"] <= 1
    assert result["unknown_categories"] == ["carrier"]
    assert metrics["baseline_test"]["roc_auc"] == pytest.approx(0.5)
    assert (tmp_path / "metrics.json").exists()
