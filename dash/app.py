import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/warehouse/nyc_taxi.db")

st.set_page_config(page_title="Dashboard de Datos - Proyecto Data Engineer", layout="wide")
st.title("Dashboard de Datos - Mi Primer Proyecto Data Engineer")

if not DB_PATH.exists():
    st.warning("Primero ejecuta el pipeline: `python -m src.orchestrate.flow`")
    st.info("Ejecuta en terminal: `.\.venv\Scripts\python -m src.orchestrate.flow`")
else:
    con = sqlite3.connect(DB_PATH)
    
    # KPIs básicos
    df = pd.read_sql("SELECT COUNT(*) as total_registros FROM staging_trips", con)
    total_registros = df.iloc[0]['total_registros']
    
    st.metric("Total de registros procesados", total_registros)
    
    # Mostrar muestra de datos
    st.subheader("Muestra de datos procesados")
    sample_df = pd.read_sql("SELECT * FROM staging_trips LIMIT 10", con)
    st.dataframe(sample_df)
    
    # Estadísticas básicas
    st.subheader("Estadísticas del dataset")
    if len(sample_df.columns) > 0:
        st.write(f"Columnas en el dataset: {len(sample_df.columns)}")
        st.write("Nombres de columnas:")
        st.write(list(sample_df.columns))
    
    # Gráfico simple si hay columnas numéricas
    numeric_cols = sample_df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 0:
        st.subheader("Distribución de datos numéricos")
        col_to_plot = numeric_cols[0]
        plot_df = pd.read_sql(f"SELECT {col_to_plot} FROM staging_trips WHERE {col_to_plot} IS NOT NULL LIMIT 100", con)
        st.bar_chart(plot_df[col_to_plot])
    
    con.close()
    
    st.success("✅ Pipeline ejecutado correctamente. Base de datos SQLite creada y consultada.")
