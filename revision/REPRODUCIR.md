# Reproducir TP2 y TP3

## Entorno

Se utilizó Python 3.12 y semilla 42. `requirements-revision.txt` fija las versiones del entorno empleado. Los paquetes de panel, estadísticas, modelos y visualización se instalan en un entorno virtual del proyecto.

Desde la raíz, en PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-revision.txt
```

En Linux/macOS se pueden usar `python3.12 -m venv .venv` y `.venv/bin/python` en los comandos siguientes. No hace falta un kernel de Jupyter global: el ejecutor utiliza el mismo intérprete que lo invoca.

## Recalcular todo

```powershell
.\.venv\Scripts\python.exe scripts/ejecutar_revision.py
```

El orden es curación y después modelado. Se guardan los outputs en ambos notebooks y se regeneran los CSV de curación, las tablas de resultados, las figuras y la trazabilidad de la presentación. La búsqueda de modelos requiere varios minutos.

El ejecutor conserva el notebook con los outputs obtenidos incluso si una celda falla y devuelve el error. No convierte una ejecución incompleta en una ejecución exitosa.

## Comprobar una ejecución ya guardada

```powershell
.\.venv\Scripts\python.exe scripts/verificar_revision.py
```

Comprueba respuestas contra el crudo, lags exactos sin saltar huecos, medianas aprendidas con train, validez de los notebooks y ejecución de sus celdas, hashes de fuentes, orden temporal, muestra común de TWFE y cifras de la presentación. También comprueba que sigan presentes las 14 figuras de modelado.

## Recalcular solo las cifras de la presentación

```powershell
.\.venv\Scripts\python.exe scripts/calcular_valores_presentacion.py
```

Este comando no reentrena modelos ni modifica el PPTX. Lee los CSV ejecutados, verifica los datos de los ocho gráficos, la tabla de métricas y la matriz de la diapositiva 8, y genera:

- `revision/VALORES_PRESENTACION.md`.
- `revision/resultados/valores_presentacion.csv`.
- `revision/resultados/presentacion_v2_comprobacion.json`.

La presentación vigente es `deck/IA_en_las_empresas_presentation_v2.pptx`. La comprobación usa nombres de series, categorías, unidades y valores; no depende únicamente de que el archivo exista. Falla si encuentra cifras diferentes. El SHA-256 del PPTX queda registrado, sin alterar sus ediciones de diseño o texto.

## Archivos y dependencias entre pasos

`notebook/revision_analisis.py` implementa los modelos y exporta tablas. `notebook/revision_graficos.py` recupera las figuras a partir de esas tablas y reajusta únicamente lo necesario para los diagnósticos. `notebook/valores_presentacion.py` relaciona resultados y diapositivas. Los tres módulos forman parte de la entrega y deben acompañar al notebook.

`data_panel_observado.csv` mantiene la selección de adopción válida de TP2 y conserva faltantes predictivos anteriores a la imputación. TWFE aplica adicionalmente una muestra completa común para las especificaciones con y sin adopción. La evaluación temporal reconstruye una muestra propia desde `data/raw/`.

Para tiempo, la recuperación de categorías usa solo respuestas anteriores y no se detectan bandas con test. Se entrena con resultados de 2023–2024, se selecciona en 2025 y se evalúa 2026. Los lags exigen el trimestre calendario inmediatamente anterior. El escenario es secuencial a un trimestre, no una predicción de todo el año desde un único corte.

Los efectos anuales categóricos desconocidos se representan con la referencia del entrenamiento. No se estima un efecto nuevo de 2026 con test. Las muestras contemporánea y rezagada son distintas, y la evaluación temporal conserva productividad extrema del crudo.

## Fuentes, gráficos y versiones

`revision/resultados/manifest.json` registra versiones, semilla y hashes de los CSV fuente con rutas relativas portables. Los hashes normalizan CRLF a LF, igualando los saltos de línea que Git puede convertir entre sistemas. Los valores y archivos crudos no se reescriben. Las figuras quedan en `revision/resultados/graficos/` y embebidas en el notebook.

La presentación v2 contiene las ediciones finales del equipo. `scripts/generar_presentaciones.mjs` se conserva como fuente de la generación anterior, pero **no reproduce esas ediciones manuales**. Es opcional y requiere el motor de presentaciones de Codex y sus variables `DIPLO_ARTIFACT_MODULE`, `DIPLO_PRESENTATION_SKILL` y `DIPLO_RUNTIME_PYTHON`. El cálculo y la verificación de cifras solo requieren Python.

Los respaldos locales, entornos y recibos de renderizado con rutas de una computadora quedan excluidos por `.gitignore`. Los CSV de resultados, figuras, manifiesto y comprobación portable del PPTX sí se versionan.
