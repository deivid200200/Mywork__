import os
import pathlib
import requests
from typing import Tuple

RAW_DIR = pathlib.Path("data/raw")

TRIPS_URL = "https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data1.csv"
ZONES_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"


def _ensure_dir(path: pathlib.Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _download(url: str, out_path: pathlib.Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)


def ingest_month_2020_01() -> Tuple[pathlib.Path, pathlib.Path]:
    """
    Descarga enero 2020 (parquet) y zonas (csv) al data lake local.
    Retorna rutas a archivos descargados.
    """
    trips_path = RAW_DIR / "uber_rides_sample.csv"
    zones_path = RAW_DIR / "taxi_zone_lookup.csv"
    if not trips_path.exists():
        _download(TRIPS_URL, trips_path)
    if not zones_path.exists():
        _download(ZONES_URL, zones_path)
    return trips_path, zones_path
