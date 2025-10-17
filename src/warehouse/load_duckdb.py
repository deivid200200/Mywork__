import pathlib
import sqlite3
import pandas as pd

WAREHOUSE_DIR = pathlib.Path("data/warehouse")
DB_PATH = WAREHOUSE_DIR / "nyc_taxi.db"


def load_to_sqlite(processed_csv: pathlib.Path) -> pathlib.Path:
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Leer CSV procesado
    df = pd.read_csv(processed_csv)
    
    # Conectar a SQLite
    con = sqlite3.connect(DB_PATH)
    
    # Crear tablas
    df.to_sql("staging_trips", con, if_exists="replace", index=False)
    
    # Crear dim_zone
    con.execute("""
        CREATE TABLE IF NOT EXISTS dim_zone AS
        SELECT DISTINCT PULocationID AS LocationID, PUZone AS Zone, PUBorough AS Borough
        FROM staging_trips
        WHERE PULocationID IS NOT NULL
        UNION
        SELECT DISTINCT DOLocationID AS LocationID, DOZone AS Zone, DOBorough AS Borough
        FROM staging_trips
        WHERE DOLocationID IS NOT NULL;
    """)
    
    # Crear fact_trips
    con.execute("""
        CREATE TABLE IF NOT EXISTS fact_trips AS
        SELECT
          tpep_pickup_datetime,
          tpep_dropoff_datetime,
          passenger_count,
          trip_distance,
          fare_amount,
          total_amount,
          trip_duration_min,
          pickup_hour,
          pickup_dow,
          PULocationID,
          DOLocationID
        FROM staging_trips;
    """)
    
    con.close()
    return DB_PATH
