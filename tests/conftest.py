import pandas as pd
import pytest

from flightlab.data import prepare


@pytest.fixture
def flights():
    rows = []
    for date in pd.date_range("2013-01-01", periods=60):
        for i in range(10):
            rows.append(
                {
                    "year": date.year,
                    "month": date.month,
                    "day": date.day,
                    "carrier": "AA" if i % 2 else "UA",
                    "origin": "JFK",
                    "dest": "LAX",
                    "distance": 2475,
                    "arr_delay": 30 if i % 3 == 0 else -5,
                }
            )
    return prepare(pd.DataFrame(rows))
