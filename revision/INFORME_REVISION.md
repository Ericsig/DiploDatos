# Informe de revisión y comprobaciones

Equipo: Eric Sigwald, Gonzalo Marengo y Sebastian Rigo.

## Versión de entrega

La presentación vigente es `deck/IA_en_las_empresas_presentation_v2.pptx`, editada por el equipo. Esta preparación la conserva sin cambios. `deck/IA_en_las_empresas_presentation.pptx` es la versión histórica. El borrador `deck/deck.md` fue retirado por el equipo y no se restaura.

El detalle de decisiones y cálculos está en [CAMBIOS_TP3.md](CAMBIOS_TP3.md). La trazabilidad numérica de cada diapositiva se genera en [VALORES_PRESENTACION.md](VALORES_PRESENTACION.md). El procedimiento está en [REPRODUCIR.md](REPRODUCIR.md).

## Contenido reproducible

- Curación con recuperación de categorías por empresa, mediana/moda por estrato, indicadores y exportación de mediciones observadas.
- TWFE con y sin adopción sobre una muestra común, errores agrupados, magnitudes estandarizadas y sensibilidad a leverage y residuos.
- Ridge y boosting con selección por MAE en validación agrupada.
- H3 con componentes del saldo, neutral por dotación, logit multinomial, VIF y sensibilidad al retirar variables de tamaño.
- Comparación de cuatro clasificadores con macro-F1 estable, métricas por clase, matrices y bootstrap por empresa.
- Respuestas alternativas con banda proporcional y exclusión de neutral.
- Validación por años con X contemporánea y con rezagos calendario exactos.
- Catorce figuras embebidas, incluidos residuos, curvatura spline y observado frente a estimado.

Los 43 bloques del notebook de modelado, más la celda final de trazabilidad incorporada a esta preparación, conservan los outputs de los cálculos. La preparación principal y las visualizaciones se ejecutaron en sesiones documentadas; no se repitieron los grids para cambiar únicamente documentación. La celda de trazabilidad se ejecuta sobre los CSV guardados.

## Comprobaciones

`scripts/verificar_revision.py` comprueba:

1. Que productividad, adopción y empleo no hayan sido fabricados por imputación de targets.
2. Que un salto de dos trimestres no genere un lag t−1 ni se crucen empresas.
3. Que medianas de estrato y respaldo global provengan del entrenamiento.
4. Que los notebooks sean válidos y sus celdas estén ejecutadas sin outputs de error.
5. Que los hashes de los CSV fuente coincidan.
6. Que train, validación y test temporal tengan orden estricto.
7. Que TWFE use la misma muestra y las cuatro familias tengan configuración seleccionada por CV.
8. Que los ocho gráficos y las tablas numéricas del PPTX coincidan con los CSV.
9. Que se conserven las catorce figuras de modelado.

La comprobación de la presentación es numérica y de solo lectura. No certifica una evaluación causal ni sustituye la revisión visual de las ediciones finales. La exportación inicial se renderizó y revisó; el PPTX de entrega contiene ediciones posteriores del equipo.

## Archivos necesarios

Se incluyen los notebooks, `revision_analisis.py`, `revision_graficos.py`, `valores_presentacion.py`, los scripts de ejecución/comprobación/cálculo, dependencias fijadas, datasets curados, resultados tabulares, figuras y presentación v2. Los respaldos y registros locales con rutas absolutas permanecen en la computadora y se excluyen del versionado.

## Alcance

El dataset es sintético y el test ya había sido consultado históricamente. La revisión es exploratoria. No establece mediación, causalidad o mecanismos de asistencia/reemplazo por el nombre de las variables. H2, los casos de uso y la transformación de tareas requieren trabajo adicional. Las métricas temporales contemporáneas y rezagadas no se interpretan como una comparación con idéntica muestra.
