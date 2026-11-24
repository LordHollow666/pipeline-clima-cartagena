# Pipeline del clima de Cartagena

Proceso automatizado que obtiene cada día el clima de Cartagena, lo limpia,
lo guarda en una base de datos SQL y lo muestra en un dashboard interactivo.



## Qué hace

1. **Extrae** datos diarios (temperatura, lluvia y viento) de la API gratuita
   [Open-Meteo](https://open-meteo.com).
2. **Transforma** los datos con pandas: renombra columnas, unifica fechas,
   elimina vacíos y duplicados, y calcula la temperatura promedio.
3. **Carga** el resultado en una base de datos SQLite.
4. **Se ejecuta solo cada día** con GitHub Actions y guarda la base de datos
   actualizada en el repositorio.
5. **Muestra** los resultados en un dashboard hecho con Streamlit.

La API solo ofrece los últimos 30 días, pero la base de datos acumula
el historial: cada ejecución agrega los días nuevos sin duplicar los anteriores.

## Tecnologías

Python · pandas · requests · SQLite · SQL · Streamlit · GitHub Actions

## Estructura

```
.
├── .github/workflows/   # Ejecución diaria automática
├── data/clima.db        # Base de datos (se actualiza sola)
├── docs/img/            # Capturas
├── sql/consultas.sql    # Consultas SQL de ejemplo
├── pipeline.py          # Extraer, transformar y cargar (ETL)
├── dashboard.py         # Tablero con Streamlit
└── requirements.txt
```

## Cómo ejecutarlo

```bash
git clone https://github.com/TU_USUARIO/pipeline-clima-cartagena.git
cd pipeline-clima-cartagena

python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows PowerShell
# source .venv/bin/activate       # Mac / Linux

pip install -r requirements.txt
python pipeline.py                # actualiza la base de datos
streamlit run dashboard.py        # abre el dashboard
```

## Consultas SQL

En [`sql/consultas.sql`](sql/consultas.sql) hay consultas que responden preguntas
como: ¿cuál fue el día más caluroso?, ¿cuántos días llovió?, ¿cuál fue el
promedio semanal? Usan `WHERE`, `GROUP BY`, funciones de agregación y `CASE`.

## Decisiones técnicas

- **`INSERT OR REPLACE` con fecha como clave primaria:** el pipeline se puede
  ejecutar muchas veces sin duplicar datos.
- **`timeout` en las peticiones y `raise_for_status()`:** si la API falla, el
  programa se detiene con un error claro en vez de guardar datos malos.
- **SQLite versionada en el repositorio:** es la forma más simple de conservar
  los datos entre ejecuciones de GitHub Actions, dado que su máquina se destruye al terminar.
- **Caché en el dashboard:** evita releer la base de datos en cada interacción.

## Limitaciones conocidas

- Guardar una base de datos en Git funciona bien a esta escala, pero no es la
  solución para grandes volúmenes. Con más datos usaría una base de datos en la nube.
- Los datos son pronósticos y reanálisis del modelo de Open-Meteo, no mediciones
  de una estación local.
- Si la API cambia su formato, el pipeline fallará hasta que se ajuste.

## Cómo usé IA en este proyecto

Usé asistentes de IA para aprender los conceptos (ETL, SQL, pipelines) y acelerar
la escritura de código. Ejecuté, probé y entendí cada parte, y escribí consultas SQL
propias para responder preguntas sobre los datos.

## Próximos pasos

- Pruebas automatizadas para la función de limpieza
- Publicar el dashboard en línea (Streamlit Community Cloud)
- Agregar más ciudades de Colombia para compararlas