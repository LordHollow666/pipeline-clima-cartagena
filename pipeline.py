import sqlite3
from pathlib import Path

import pandas as pd
import requests

URL = "https://api.open-meteo.com/v1/forecast"
PARAMETROS = {
    "latitude": 10.39,
    "longitude": -75.48,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
    "timezone": "America/Bogota",
    "past_days": 30,
    "forecast_days": 1,
}
RUTA_BD = Path("data/clima.db")


def extraer() -> dict:
    respuesta = requests.get(URL, params=PARAMETROS, timeout=10)
    respuesta.raise_for_status()
    return respuesta.json()


def transformar(datos: dict) -> pd.DataFrame:
    tabla = pd.DataFrame(datos["daily"])
    tabla = tabla.rename(columns={
        "time": "fecha",
        "temperature_2m_max": "temp_max",
        "temperature_2m_min": "temp_min",
        "precipitation_sum": "lluvia_mm",
        "wind_speed_10m_max": "viento_max_kmh",
    })
    tabla["fecha"] = pd.to_datetime(tabla["fecha"]).dt.strftime("%Y-%m-%d")
    tabla = tabla.dropna(subset=["temp_max", "temp_min"])
    tabla = tabla.drop_duplicates(subset="fecha")
    tabla["temp_promedio"] = (
        (tabla["temp_max"] + tabla["temp_min"]) / 2).round(1)
    return tabla


def guardar(tabla: pd.DataFrame) -> int:
    RUTA_BD.parent.mkdir(exist_ok=True)
    conexion = sqlite3.connect(RUTA_BD)
    try:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS clima_diario (
                fecha TEXT PRIMARY KEY,
                temp_max REAL,
                temp_min REAL,
                lluvia_mm REAL,
                viento_max_kmh REAL,
                temp_promedio REAL
            )
        """)
        columnas = ["fecha", "temp_max", "temp_min", "lluvia_mm",
                    "viento_max_kmh", "temp_promedio"]
        conexion.executemany(
            """INSERT OR REPLACE INTO clima_diario
               (fecha, temp_max, temp_min, lluvia_mm, viento_max_kmh, temp_promedio)
               VALUES (?, ?, ?, ?, ?, ?)""",
            list(tabla[columnas].itertuples(index=False, name=None)),
        )
        conexion.commit()
        total = conexion.execute(
            "SELECT COUNT(*) FROM clima_diario").fetchone()[0]
    finally:
        conexion.close()
    return total


def main():
    print("1/3 Extrayendo datos...")
    datos = extraer()

    print("2/3 Limpiando datos...")
    tabla = transformar(datos)
    print(f"    {len(tabla)} días listos")

    print("3/3 Guardando en la base de datos...")
    total = guardar(tabla)
    print(f"Listo. La base de datos tiene {total} días.")


if __name__ == "__main__":
    main()
