import pandas as pd
from src.quality.quality_checks import validate_trips

def test_validate_trips_basic():
    df = pd.DataFrame({
        "tpep_pickup_datetime": ["2020-01-01 00:00:00"],
        "tpep_dropoff_datetime": ["2020-01-01 00:10:00"],
        "passenger_count": [1],
        "trip_distance": [2.5],
        "fare_amount": [10.0],
        "total_amount": [12.0],
        "PULocationID": [1],
        "DOLocationID": [2],
    })
    summary = validate_trips(df)
    assert summary["missing_required_cols"] is False
    assert summary["invalid_datetime"] == 0
