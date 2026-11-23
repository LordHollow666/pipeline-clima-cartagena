import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

RUTA_BD = Path("data/clima.db")

st.set_page_config(page_title="Clima de Cartagena",
                   page_icon="🌴", layout="wide")


@st.cache_data(ttl=600)
def cargar_datos() -> pd.DataFrame:
    conexion = sqlite3.connect(RUTA_BD)
    try:
        tabla = pd.read_sql_query(
            "SELECT * FROM clima_diario ORDER BY fecha", conexion
        )
    finally:
        conexion.close()
    tabla["fecha"] = pd.to_datetime(tabla["fecha"])
    return tabla


st.title("🌴 Clima de Cartagena")
st.caption(
    "Datos de Open-Meteo, procesados con un pipeline propio en Python y SQLite.")

if not RUTA_BD.exists():
    st.error("No encuentro la base de datos. Ejecuta primero: python pipeline.py")
    st.stop()

datos = cargar_datos()

# Barra lateral: el usuario elige cuántos días ver
dias = st.sidebar.slider("Días a mostrar", 7, len(datos), len(datos))
vista = datos.tail(dias)

# Números destacados
dia_caluroso = vista.loc[vista["temp_max"].idxmax()]
col1, col2, col3, col4 = st.columns(4)
col1.metric("Temperatura promedio", f"{vista['temp_promedio'].mean():.1f} °C")
col2.metric(
    f"Día más caluroso ({dia_caluroso['fecha'].strftime('%d/%m')})",
    f"{dia_caluroso['temp_max']:.1f} °C",
)
col3.metric("Lluvia total", f"{vista['lluvia_mm'].sum():.1f} mm")
col4.metric("Días con lluvia", int((vista["lluvia_mm"] > 0).sum()))

# Gráficos
st.subheader("Temperatura")
st.line_chart(vista.set_index("fecha")[
              ["temp_max", "temp_min", "temp_promedio"]])

izquierda, derecha = st.columns(2)
with izquierda:
    st.subheader("Lluvia diaria (mm)")
    st.bar_chart(vista.set_index("fecha")["lluvia_mm"])
with derecha:
    st.subheader("Viento máximo (km/h)")
    st.line_chart(vista.set_index("fecha")["viento_max_kmh"])

with st.expander("Ver la tabla de datos"):
    st.dataframe(vista, use_container_width=True)
