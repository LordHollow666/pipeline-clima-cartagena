-- los 5 dias mas recientes
SELECT * FROM clima_diario ORDER BY fecha DESC LIMIT 5;

-- cual fue el dia mas caluroso
SELECT fecha, temp_max FROM clima_diario ORDER BY temp_max DESC LIMIT 1;

-- cuantos dias llovio
SELECT COUNT(*) AS dias_con_lluvia FROM clima_diario WHERE lluvia_mm > 0;

-- cual fue la temperatura promedio del mes
SELECT ROUND(AVG(temp_promedio), 1) AS promedio FROM clima_diario;

-- cuanta lluvia cayo en total
SELECT ROUND(SUM(lluvia_mm), 1) AS lluvia_total_mm FROM clima_diario;

-- dias con vientos fuertes (mas de 25km/h) 
SELECT fecha, viento_max_kmh FROM clima_diario
WHERE viento_max_kmh > 25
ORDER BY viento_max_kmh DESC;

-- resumen por semana
SELECT strf time('%Y-S%W', fecha) AS semana,
       ROUND(AVG(temp_promedio), 1) AS temp_promedio,
       ROUND(SUM(lluvia_mm), 1) AS lluvia_total
FROM clima_diario
GROUP BY semana
ORDER BY semana;


-- clasificar los dias segun la lluvia
SELECT CASE
           WHEN lluvia_mm = 0 THEN 'Seco'
           WHEN lluvia_mm < 5 THEN 'Llovizna'
           ELSE 'Lluvioso'
       END AS tipo_de_dia,
       COUNT(*) AS dias
FROM clima_diario
WHERE lluvia_mm IS NOT NULL
GROUP BY tipo_de_dia
ORDER BY dias DESC;