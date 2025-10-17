import pathlib
import pandas as pd

PROCESSED_DIR = pathlib.Path("data/processed")


def transform_trips(parquet_path: pathlib.Path, zones_csv_path: pathlib.Path) -> pathlib.Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(parquet_path)
    zones = pd.read_csv(zones_csv_path)

    # Cast de fechas
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"], errors="coerce")
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"], errors="coerce")

    # Derivados
    df["trip_duration_min"] = (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]).dt.total_seconds() / 60.0
    df["pickup_hour"] = df["tpep_pickup_datetime"].dt.hour
    df["pickup_dow"] = df["tpep_pickup_datetime"].dt.dayofweek

    # Join con zonas
    zones = zones.rename(columns={"LocationID": "LocationID", "Zone": "Zone", "Borough": "Borough"})
    pu = zones[["LocationID", "Zone", "Borough"]].rename(columns={"LocationID": "PULocationID", "Zone": "PUZone", "Borough": "PUBorough"})
    do = zones[["LocationID", "Zone", "Borough"]].rename(columns={"LocationID": "DOLocationID", "Zone": "DOZone", "Borough": "DOBorough"})

    df = df.merge(pu, on="PULocationID", how="left").merge(do, on="DOLocationID", how="left")

    out_path = PROCESSED_DIR / "yellow_tripdata_2020-01_clean.csv"
    df.to_csv(out_path, index=False)
    return out_path
