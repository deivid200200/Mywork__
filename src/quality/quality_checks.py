import pandas as pd

REQUIRED_COLUMNS = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "fare_amount",
    "total_amount",
    "PULocationID",
    "DOLocationID",
]


def validate_trips(df: pd.DataFrame) -> dict:
    """Corre validaciones básicas y devuelve un resumen con counts y flags."""
    summary = {
        "rows": len(df),
        "missing_required_cols": False,
        "nulls_in_required": 0,
        "negative_fare": 0,
        "negative_distance": 0,
        "invalid_datetime": 0,
    }

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        summary["missing_required_cols"] = True
        return summary

    req_df = df[REQUIRED_COLUMNS]
    summary["nulls_in_required"] = int(req_df.isna().sum().sum())

    summary["negative_fare"] = int((df["fare_amount"] < 0).sum())
    summary["negative_distance"] = int((df["trip_distance"] < 0).sum())

    # Fechas válidas: dropoff >= pickup
    try:
        pickup = pd.to_datetime(df["tpep_pickup_datetime"], errors="coerce")
        dropoff = pd.to_datetime(df["tpep_dropoff_datetime"], errors="coerce")
        summary["invalid_datetime"] = int(((dropoff < pickup) | pickup.isna() | dropoff.isna()).sum())
    except Exception:
        summary["invalid_datetime"] = len(df)

    return summary
