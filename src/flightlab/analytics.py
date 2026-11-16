import pandas as pd

from flightlab.config import TARGET_MINUTES


def ranking(df: pd.DataFrame, by: str, min_flights: int = 100) -> pd.DataFrame:
    if by not in {"carrier", "route", "month", "origin", "tailnum"}:
        raise ValueError("Agrupamento não permitido")
    result = (
        df.groupby(by)
        .agg(
            flights=("delayed", "size"),
            delayed_flights=("delayed", "sum"),
            delay_rate=("delayed", "mean"),
            mean_arrival_deviation=("arr_delay", "mean"),
        )
        .reset_index()
    )
    return result.loc[result["flights"].ge(min_flights)].sort_values("delay_rate", ascending=False)


def summary(df: pd.DataFrame, min_flights: int = 100) -> dict:
    if df.empty:
        return {"flights": 0, "message": "Nenhum voo para os filtros selecionados."}
    return {
        "flights": len(df),
        "delay_threshold_minutes": TARGET_MINUTES,
        "delay_rate": float(df["delayed"].mean()),
        "mean_arrival_deviation_minutes": float(df["arr_delay"].mean()),
        "period": [str(df["date"].min().date()), str(df["date"].max().date())],
        "minimum_group_flights": min_flights,
        "carriers": ranking(df, "carrier", min_flights).to_dict("records"),
        "top_routes": ranking(df, "route", min_flights).head(10).to_dict("records"),
        "monthly": ranking(df, "month", 1).sort_values("month").to_dict("records"),
    }
