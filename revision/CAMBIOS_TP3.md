# Cambios del TP3 y fundamento de los cálculos

Les dejo el detalle de los cambios que hice a partir de la devolución de Caro. La idea fue corregir las decisiones metodológicas, recalcular las cifras y conservar los gráficos que ayudan a entender el recorrido del análisis.

La presentación de entrega es **`deck/IA_en_las_empresas_presentation_v2.pptx`**. El notebook principal es **`notebook/modelado.ipynb`**. El detalle numérico por diapositiva está en **`revision/VALORES_PRESENTACION.md`**, generado desde los mismos CSV que producen los modelos.

## 1. Preparación: recuperar información y no fabricar respuestas

Antes se descartaban filas por falta de industria o tamaño, aunque esos datos estuvieran en otro trimestre de la misma empresa. Cambié esa decisión por una recuperación controlada: completo un atributo solo cuando todos sus valores observados dentro de la empresa coinciden. En este dataset no detectamos cambios de industria o tamaño, pero no doy por supuesto que sean constantes en cualquier panel.

Se recuperaron **2.250 datos de industria y 2.250 de tamaño**. Quedan tres industrias y un tamaño sin resolver. No completé las categorías contradictorias o sin ninguna observación disponible.

Mantuve las medianas por **industria × tamaño**, con respaldo global. Para ética y privacidad usé la moda del estrato y el respaldo global, conservando indicadores de ausencia de respuesta. El cambio importante para TP3 fue separar dos productos:

- La tabla curada de TP2, con las transformaciones de esa etapa.
- Un **panel observado anterior a la imputación de predictoras**, que permite aprender las medianas dentro de cada entrenamiento del modelado.

No imputé productividad, adopción ni empleo como respuestas. Si falta una respuesta o se marca como inválida, esa fila se excluye del modelo que la necesita. Esto evita evaluar el modelo contra respuestas fabricadas por la propia preparación.

La recuperación retrospectiva sirve para describir el panel. En la evaluación temporal reconstruí los datos desde el crudo y solo arrastré categorías desde observaciones anteriores. No usé un trimestre futuro para completar el pasado.

## 2. Tamaño empresarial, tiempo y transformación logarítmica

Revisé la distribución de empleados e ingresos antes de aceptar un orden para Startup, SME y Enterprise. Los rangos de empleados están separados en estos datos, pero mantuve `company_size` como categoría: no impuse que los saltos entre sus niveles tengan la misma distancia.

El tiempo se representa con:

```text
period_index = 4 × (survey_year − 2023) + quarter_num − 1
```

Así 2023 Q4 vale 3 y 2024 Q1 vale 4. El trimestre aislado puede representar estacionalidad, pero no progreso entre años. Verifiqué que empresa y período formen una clave única y ordenada.

También corregí la evaluación del logaritmo. Comparar una media en dólares con otra en log-dólares no permite concluir que la transformación funcionó. Usé el **skew**, que compara la forma de la distribución. Ingresos pasa de 2,27 a 0,33 e inversión de 4,50 a −2,80: la inversión sigue siendo asimétrica y no corresponde decir que quedó normalizada.

## 3. H1: dos especificaciones TWFE y la misma muestra

La pregunta original era por la relación entre inversión y productividad, controlando industria y tamaño. Por eso agregué una especificación **sin adopción** y conservé otra **con adopción**. Incluir adopción cambia la pregunta: si fuera parte del camino entre inversión y productividad, estaríamos condicionando una variable intermedia. Los datos simultáneos no alcanzan para probar que ese sea el mecanismo causal.

Ambos modelos usan exactamente **144.743 observaciones completas**. Esquemáticamente:

```text
M1: productividad_it = α_i + λ_t + β_inv log1p(inversión_it) + ε_it
M2: productividad_it = α_i + λ_t + β_inv log1p(inversión_it)
                       + β_adop adopción_it + ε_it
```

`α_i` representa los efectos de empresa y `λ_t` los de período. Industria, tamaño e ingresos constantes dentro de una empresa quedan absorbidos. Los errores estándar se agrupan por empresa, para contemplar dependencia entre sus respuestas.

La pendiente de inversión quedó en **1,273 sin adopción** y **0,294 con adopción**. No los presenté como retornos causales ni interpreté la diferencia como una mediación demostrada.

También corregí ingresos: sin imputar sus faltantes, resulta constante dentro de cada empresa. No corresponde estimar una asociación within a partir de variación introducida por la imputación.

## 4. Comparación de magnitudes: un cambio de escala explícito

Saqué la comparación de duplicar inversión contra subir un punto de adopción. Aunque cada cálculo individual fuera correcto, esos incrementos no justificaban concluir que una variable “pesa más”.

Ahora calculo, para cada predictor residualizado por efectos de empresa y período:

```text
cambio por un desvío within = β_j × sd(X_j residualizado)
cambio por IQR within      = β_j × [P75(X_j residualizado) − P25(X_j residualizado)]
```

Uso la desviación estándar muestral (`ddof=1`). Los cambios por un desvío son **1,05 puntos de productividad** para inversión sin adopción, **0,24** para inversión con adopción y **2,34** para adopción en el segundo modelo. Son comparaciones dentro de las especificaciones indicadas, no un ranking causal general.

## 5. Leverage, residuos y curvatura

Agregué sensibilidad a observaciones influyentes, diferenciándola de la normalidad de los residuos. Para la especificación con adopción calculé el leverage de las pendientes después de absorber ambos efectos:

```text
h_i = diagonal[X_within (X_within' X_within)^−1 X_within']
umbral de diagnóstico = 4p/n
```

Esta medida no incluye todo el leverage de las dummies de efectos fijos. Volví a ajustar los dos modelos retirando:

1. Filas con leverage por encima del umbral.
2. Empresas completas que contienen esas filas.
3. Por separado, residuos estandarizados con `|z| > 3,5`.

Al retirar **2.187 filas con leverage alto**, la pendiente de inversión con adopción pasa de **0,294 a 1,603**. Retirar residuos extremos la deja aproximadamente en **0,295**. Por eso no presenté la magnitud de inversión como robusta: la pendiente es mucho más sensible a la posición de ciertas observaciones que a sus residuos extremos.

Conservé el histograma, Q–Q, residuos parciales y sensibilidad gráfica. La normalidad no es necesaria para estimar las pendientes; agrupar errores tampoco corrige confusión, simultaneidad o una forma funcional equivocada. Excluir según residuos es solo un diagnóstico, porque selecciona usando la respuesta.

Recuperé además la curva **spline** con los datos corregidos. Se compara con la recta y con la distribución de inversión, usando diferencias respecto de la mediana e intervalos puntuales agrupados. El R² de la proyección TWFE pasa de aproximadamente 0,244 a 0,253. No uso esa curva para identificar un umbral rentable ni para volver a elegir un modelo con test.

## 6. H1 predictiva: mismos datos, criterio estable y referencia

Conservé Ridge y gradient boosting, junto con la media de entrenamiento como referencia. Los predictores son inversión, adopción, industria, tamaño, empleados, ingresos, edad, año, trimestre y PBI per cápita.

Separé el 20% de las empresas para test y usé tres pliegues de **GroupKFold** en el resto. En cada ajuste se aprenden medianas, categorías y escalas exclusivamente con entrenamiento. Fijé **MAE** como criterio principal de esta revisión.

La búsqueda queda explícita y acotada: tres penalizaciones de Ridge y cuatro combinaciones de boosting. No la describo como el óptimo de todos los hiperparámetros posibles.

| Modelo | MAE de test (pp) | R² de test |
|---|---:|---:|
| Media de train | 4,67 | −0,0004 |
| Ridge | 3,36 | 0,428 |
| Gradient boosting | 3,34 | 0,435 |

MAE es la media del error absoluto. R² compara el error cuadrático con la media del conjunto evaluado y puede ser negativo. Las diferencias entre Ridge y boosting son pequeñas en estas configuraciones; no demuestran un límite general de la técnica. El gráfico de observado frente a estimado se recalcula con la configuración ya elegida y verifica que reproduce las métricas guardadas.

## 7. H3: componentes del saldo y alcance de la interpretación

Dejé explícito que:

```text
saldo = jobs_created − jobs_displaced
tasa de creación = jobs_created / num_employees
tasa de desplazamiento = jobs_displaced / num_employees
```

La clasificación del saldo no mide por sí sola transformación de tareas. Revisé los componentes por separado y la discriminación entre creación y desplazamiento, excluyendo neutral para ese análisis binario. La AUC de test es aproximadamente **0,573 con adopción**, **0,708 con automatización** y **0,874 con ambas**, separando empresas.

Retiré la explicación de que los nombres de las variables comprueban asistencia frente a reemplazo. En el logit, los signos describen asociaciones condicionales. Para distinguir mecanismos haría falta analizar `ai_use_case` y conocer la construcción del dataset.

El logit multinomial usa neutral como referencia. Adopción y automatización entran divididas por diez: sus coeficientes corresponden a **+10 puntos**. La presentación muestra `log(RRR)`; al exponenciarlo se obtiene la razón de probabilidades relativas frente a neutral. No es un cambio directo en la probabilidad de creación o desplazamiento.

## 8. Neutral y colinealidad

Neutral original significa **creados = desplazados**, incluso cuando ambos son positivos. Mostré su frecuencia por dotación: **40,9%** entre 10 y 99 empleados, **5,7%** entre 100 y 999 y **0,35%** desde 1.000. Esto permite ver cuánto depende el empate exacto de la resolución del conteo.

Reentrené la especificación elegida con dos respuestas alternativas: banda de **±0,5% de la plantilla** y clasificación binaria excluyendo neutral. Sus F1 corresponden a tareas diferentes y no los usé para declarar una mejora frente a las tres clases originales.

Agregué VIF, rango de diseño, errores agrupados y sensibilidad al retirar empleados o tamaño. El VIF máximo del diseño completo es aproximadamente **19,9**. Rango completo descarta colinealidad perfecta, pero no que dos variables compartan mucha información. Los resultados de estas variantes quedan como diagnóstico, no como una nueva selección hecha mirando test.

## 9. Elección del clasificador y errores por clase

Corregí el cambio de criterio entre macro-F1 y F1 de empleo. Durante toda esta revisión usé **macro-F1 de las tres clases** como métrica principal; F1 de creación y desplazamiento quedó secundaria. Sin una función de costos definida, mantuve igual peso entre clases.

Comparé logit lineal, logit con splines, RF base y RF ampliado con las mismas empresas y ocho predictores. Las búsquedas usan dos penalizaciones para cada logit, una configuración RF base y cuatro alternativas RF ampliado.

| Modelo | Macro-F1 de test | F1 creación | F1 desplazamiento |
|---|---:|---:|---:|
| Logit lineal | 0,673 | 0,740 | 0,709 |
| Logit spline | 0,676 | 0,739 | 0,708 |
| RF base | 0,671 | 0,735 | 0,702 |
| RF ampliado | 0,675 | 0,738 | 0,707 |

RF ampliado queda elegido por **macro-F1 de CV ≈ 0,67849**. No cambié la elección porque el logit spline obtenga un valor de test apenas mayor. La referencia mayoritaria acierta **43,4%**.

Los F1 se calculan como `2 × precisión × recall / (precisión + recall)`; macro-F1 promedia las tres clases. La matriz se normaliza por fila observada. Por ejemplo, el **54,5%** de la fila neutral es el recall de neutral del RF ampliado, no la precisión de sus predicciones neutrales.

Agregué 200 remuestreos por empresa para la diferencia entre RF ampliado y RF base. Su intervalo es condicional a estos ajustes y a este test; no incorpora toda la incertidumbre de entrenamiento y selección. La revisión sigue siendo exploratoria porque test ya se había consultado durante el trabajo original.

## 10. Tiempo: generalizar a otras empresas y anticipar son preguntas distintas

Implementé train **2023–2024**, selección en **2025** y test **2026**. Mantuve el entrenamiento en 2023–2024 después de elegir la penalización.

Comparé dos escenarios: predictores del mismo trimestre y del trimestre inmediatamente anterior. El primero evalúa transferencia a períodos posteriores si esas variables ya se conocen; el segundo se acerca a anticipación a un trimestre.

Los rezagos se construyen con una unión exacta por empresa y período destino `t = origen + 1`. Si falta un trimestre, no uso una fila más antigua como si fuera `t−1`. La disponibilidad supuesta es secuencial: al predecir un trimestre ya se observa el anterior.

| Evaluación en 2026 | X contemporánea | X de t−1 |
|---|---:|---:|
| Productividad, Ridge, MAE (pp) | 3,45 | 4,32 |
| Empleo, logit, macro-F1 | 0,676 | 0,529 |

Las muestras son distintas: **37.544 filas** contemporáneas y **35.233 pares** consecutivos. La diferencia entre métricas no aísla exclusivamente la pérdida de información. La preparación temporal parte del crudo, conserva productividad extrema y no busca bandas con datos de test. Los años categóricos desconocidos usan la referencia: es una limitación de extrapolación del efecto anual.

## 11. Gráficos, archivos y cálculo de las cifras de la presentación

Conservé **14 figuras embebidas** en el notebook. La presentación mantiene diez diapositivas y ocho gráficos editables. Los gráficos muestran la dispersión, las curvas y los errores; las tablas quedan como respaldo de las cifras.

La implementación se reparte así:

- `notebook/revision_analisis.py`: preparación, modelos, métricas y particiones.
- `notebook/revision_graficos.py`: diagnósticos y figuras desde los resultados ejecutados.
- `notebook/valores_presentacion.py`: relación entre cifras, unidades, fórmulas y fuentes de cada diapositiva.
- `scripts/calcular_valores_presentacion.py`: regenera esa relación y comprueba el PPTX de entrega sin modificarlo.
- `scripts/ejecutar_revision.py`: ejecuta curación y modelado con el mismo intérprete.
- `scripts/verificar_revision.py`: comprueba targets, lags, imputación, hashes, resultados y cifras del PPTX.

La comprobación de la presentación contrasta los **35 valores de sus ocho gráficos**, las **12 celdas de métricas** y las **9 celdas de la matriz** con los CSV. Se acepta únicamente el redondeo numérico utilizado al exportar el gráfico; los porcentajes se guardan como proporciones y se formatean al mostrar. Los resultados principales no se modifican para hacerlos coincidir con una diapositiva.

La preparación para ejecutar y revisar todo está en `revision/REPRODUCIR.md`. Los respaldos y recibos con rutas de esta computadora quedan fuera de la entrega versionada. También normalicé los saltos de línea para los hashes de CSV: clonar con CRLF o LF no invalida la comprobación si los valores son los mismos.

## 12. Alcance que mantuve explícito

El dataset es sintético. Las relaciones contemporáneas no establecen causalidad, los nombres de las variables no identifican mecanismos y la revisión posterior al feedback no es una validación prospectiva independiente. H2 y la transformación de tareas siguen abiertas. Las conclusiones de la presentación se leen como asociaciones condicionadas a la especificación y a esta muestra.
