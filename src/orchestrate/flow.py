import pathlib
import csv
import sqlite3

from src.ingest.ingest_tlc import ingest_month_2020_01


def simple_pipeline():
    """Pipeline simplificado usando solo librerías estándar de Python"""
    print("=== Iniciando pipeline de datos ===")
    
    # 1. Ingesta
    print("1. Descargando datos...")
    csv_path, zones_csv_path = ingest_month_2020_01()
    print(f"   Descargado: {csv_path}")
    
    # 2. Validación básica
    print("2. Validando datos...")
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    
    print(f"   Filas: {len(rows)}, Columnas: {len(headers)}")
    print(f"   Columnas: {headers}")
    
    # 3. Transformación simple - tomar solo las primeras 100 filas
    print("3. Transformando datos...")
    sample_rows = rows[:100]
    
    processed_dir = pathlib.Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    processed_path = processed_dir / "rides_clean.csv"
    
    with open(processed_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(sample_rows)
    
    # 4. Carga a SQLite
    print("4. Cargando a SQLite...")
    warehouse_dir = pathlib.Path("data/warehouse")
    warehouse_dir.mkdir(parents=True, exist_ok=True)
    db_path = warehouse_dir / "nyc_taxi.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Crear tabla
    placeholders = ', '.join(['?' for _ in headers])
    cursor.execute(f"DROP TABLE IF EXISTS staging_trips")
    cursor.execute(f"CREATE TABLE staging_trips ({', '.join([f'`{h}` TEXT' for h in headers])})")
    
    # Insertar datos
    cursor.executemany(f"INSERT INTO staging_trips VALUES ({placeholders})", sample_rows)
    conn.commit()
    conn.close()
    
    print(f"   Base de datos creada: {db_path}")
    print("=== Pipeline completado ===")
    return db_path


if __name__ == "__main__":
    simple_pipeline()
