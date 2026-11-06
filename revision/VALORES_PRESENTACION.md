# Cifras de la presentación de TP3

Este documento se genera con `python scripts/calcular_valores_presentacion.py` a partir de los CSV ejecutados.

La presentación de entrega es `deck/IA_en_las_empresas_presentation_v3.pptx`. Se lee para verificarla, sin modificarla.

Los porcentajes de los gráficos se guardan como proporciones (0,1478 se muestra como 14,78%). Las cifras se redondean solo al presentar.

## Diapositiva 2

| Elemento | Serie / categoría | Valor sin redondear | Unidad | Fuente y cálculo |
|---|---|---:|---|---|
| texto_entero | Dataset / Respuestas | 150025 | conteo | `curacion_resumen.json`: Recuento del archivo company, antes de la curación |
| texto_entero | Dataset / Empresas | 10025 | conteo | `curacion_resumen.json`: Recuento del archivo company, antes de la curación |
| texto_entero | Dataset / Trimestres | 16 | conteo | `curacion_resumen.json`: Recuento del archivo company, antes de la curación |
| texto_entero | Categorías recuperadas / industry | 2250 | celdas | `curacion_resumen.json`: Categoría faltante completada con atributo único observado por empresa |
| texto_entero | Categorías recuperadas / company_size | 2250 | celdas | `curacion_resumen.json`: Categoría faltante completada con atributo único observado por empresa |
| texto_entero | Curación / Filas sin adopción o categoría irrecuperable | 2253 | conteo | `curacion_resumen.json`: filas_crudas − tras_faltantes |
| texto_entero | Curación / Filas con adopción fuera de rango | 301 | conteo | `curacion_resumen.json`: adopcion_invalida |
| texto_entero | Curación / Respuestas finales | 147471 | conteo | `curacion_resumen.json`: panel_observado: filas tras la curación, antes de imputar predictoras |
| texto_entero | Curación / Empresas finales | 10019 | conteo | `data/data_panel_observado.csv`: nunique(company_id); sin duplicados empresa-trimestre |
| texto_entero | Muestra común TWFE / Observaciones | 144743 | conteo | `h1_twfe.csv`: Casos completos de productividad, inversión e ingresos para las dos especificaciones |

## Diapositiva 4

| Elemento | Serie / categoría | Valor sin redondear | Unidad | Fuente y cálculo |
|---|---|---:|---|---|
| texto_entero | Muestra común 2026 Q2 / Empresas | 9231 | conteo | `eda_cuartiles.csv`: Suma de los cuatro cuartiles; una observación por empresa y muestra común para ambos predictores |
| grafico | Empresas ordenadas por adopción / Cuartil 1 (25% más bajo) | 0.00129982668977 | proporción | `eda_cuartiles.csv`: media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2 |
| grafico | Empresas ordenadas por adopción / Cuartil 2 | 0.0051993067591 | proporción | `eda_cuartiles.csv`: media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2 |
| grafico | Empresas ordenadas por adopción / Cuartil 3 | 0.028596187175 | proporción | `eda_cuartiles.csv`: media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2 |
| grafico | Empresas ordenadas por adopción / Cuartil 4 (25% más alto) | 0.14781100997 | proporción | `eda_cuartiles.csv`: media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2 |
| grafico | Empresas ordenadas por inversión / Cuartil 1 (25% más bajo) | 0.0216637781629 | proporción | `eda_cuartiles.csv`: media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2 |
| grafico | Empresas ordenadas por inversión / Cuartil 2 | 0.0355285961872 | proporción | `eda_cuartiles.csv`: media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2 |
| grafico | Empresas ordenadas por inversión / Cuartil 3 | 0.0507152145644 | proporción | `eda_cuartiles.csv`: media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2 |
| grafico | Empresas ordenadas por inversión / Cuartil 4 (25% más alto) | 0.0749566724437 | proporción | `eda_cuartiles.csv`: media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2 |
| texto_redondeado | Mensaje / 0,13% | 0.129982668977 | porcentaje | `eda_cuartiles.csv`: Subtítulo: ai_adoption_rate, Q1, % de empresas con mejora > 20 |
| texto_redondeado | Mensaje / 7,5% | 7.49566724437 | porcentaje | `eda_cuartiles.csv`: Subtítulo: ai_investment_per_employee, Q4, % de empresas con mejora > 20 |
| texto_redondeado | Mensaje / 2,2% | 2.16637781629 | porcentaje | `eda_cuartiles.csv`: Subtítulo: ai_investment_per_employee, Q1, % de empresas con mejora > 20 |

## Diapositiva 5

| Elemento | Serie / categoría | Valor sin redondear | Unidad | Fuente y cálculo |
|---|---|---:|---|---|
| texto_entero | Muestra común TWFE / Observaciones | 144743 | conteo | `h1_twfe.csv`: Casos completos de productividad, inversión e ingresos para las dos especificaciones |
| texto_entero | Curación / Respuestas finales | 147471 | conteo | `curacion_resumen.json`: Total del que sale la muestra TWFE |
| grafico | Cambio de productividad / Inversión sin adopción | 1.04636185742 | puntos porcentuales | `h1_twfe.csv`: beta × sd(M_empresa,periodo X), ddof=1 |
| grafico | Cambio de productividad / Inversión con adopción | 0.241990655625 | puntos porcentuales | `h1_twfe.csv`: beta × sd(M_empresa,periodo X), ddof=1 |
| grafico | Cambio de productividad / Adopción con inversión | 2.33610992155 | puntos porcentuales | `h1_twfe.csv`: beta × sd(M_empresa,periodo X), ddof=1 |
| grafico | Modelo sin adopción / Todos los datos | 1.04636185742 | puntos porcentuales | `h1_sensibilidad.csv; h1_twfe.csv`: beta de la muestra Completa × sd within de inversión en la muestra completa (misma vara que el gráfico izquierdo) |
| grafico | Modelo sin adopción / Sin puntos muy alejados (leverage alto) | 3.63692330139 | puntos porcentuales | `h1_sensibilidad.csv; h1_twfe.csv`: beta de la muestra Sin leverage alto × sd within de inversión en la muestra completa (misma vara que el gráfico izquierdo) |
| grafico | Modelo sin adopción / Sin errores muy grandes (residuos) | 1.04678881744 | puntos porcentuales | `h1_sensibilidad.csv; h1_twfe.csv`: beta de la muestra Sin residuos ∣z∣>3.5 × sd within de inversión en la muestra completa (misma vara que el gráfico izquierdo) |
| grafico | Modelo con adopción / Todos los datos | 0.241990655625 | puntos porcentuales | `h1_sensibilidad.csv; h1_twfe.csv`: beta de la muestra Completa × sd within de inversión en la muestra completa (misma vara que el gráfico izquierdo) |
| grafico | Modelo con adopción / Sin puntos muy alejados (leverage alto) | 1.31737311403 | puntos porcentuales | `h1_sensibilidad.csv; h1_twfe.csv`: beta de la muestra Sin leverage alto × sd within de inversión en la muestra completa (misma vara que el gráfico izquierdo) |
| grafico | Modelo con adopción / Sin errores muy grandes (residuos) | 0.242000819742 | puntos porcentuales | `h1_sensibilidad.csv; h1_twfe.csv`: beta de la muestra Sin residuos ∣z∣>3.5 × sd within de inversión en la muestra completa (misma vara que el gráfico izquierdo) |
| texto_entero | Filas con leverage alto / Retiradas | 2187 | conteo | `h1_sensibilidad.csv`: n(Completa) − n(Sin leverage alto), modelo con adopción |
| texto_redondeado | Mensaje / 1,5% | 1.5109538976 | porcentaje | `h1_sensibilidad.csv`: Filas retiradas / n(Completa) |
| texto_redondeado | Mensaje / 0,24 | 0.241990655625 | puntos porcentuales | `h1_sensibilidad.csv; h1_twfe.csv`: Mensaje: inversión con adopción, muestra Completa, por un aumento típico |
| texto_redondeado | Mensaje / 1,32 | 1.31737311403 | puntos porcentuales | `h1_sensibilidad.csv; h1_twfe.csv`: Mensaje: inversión con adopción, muestra Sin leverage alto, por un aumento típico |

## Diapositiva 6

| Elemento | Serie / categoría | Valor sin redondear | Unidad | Fuente y cálculo |
|---|---|---:|---|---|
| grafico | MAE en empresas nuevas / Siempre el promedio (referencia) R² ≈ 0% | 4.6657221533 | puntos porcentuales | `h1_prediccion.csv`: media(abs(y_test − pred_test)); el rótulo incluye el R² en test |
| texto_redondeado | Mensaje / 4,67 | 4.6657221533 | puntos porcentuales | `h1_prediccion.csv`: Mensaje: MAE en test de Media train |
| grafico | MAE en empresas nuevas / Ridge R² = 42,8% | 3.35674337599 | puntos porcentuales | `h1_prediccion.csv`: media(abs(y_test − pred_test)); el rótulo incluye el R² en test |
| texto_redondeado | Mensaje / 3,36 | 3.35674337599 | puntos porcentuales | `h1_prediccion.csv`: Mensaje: MAE en test de Ridge |
| grafico | MAE en empresas nuevas / Gradient boosting R² = 43,5% | 3.34062624123 | puntos porcentuales | `h1_prediccion.csv`: media(abs(y_test − pred_test)); el rótulo incluye el R² en test |
| texto_redondeado | Mensaje / 3,34 | 3.34062624123 | puntos porcentuales | `h1_prediccion.csv`: Mensaje: MAE en test de Gradient boosting |
| texto | R² en test / Ridge | 0.428357856768 | R² | `h1_prediccion.csv`: 1 − sum((y − pred)^2) / sum((y − media(y_test))^2); se muestra en el rótulo del gráfico |
| texto | R² en test / Gradient boosting | 0.434993251533 | R² | `h1_prediccion.csv`: 1 − sum((y − pred)^2) / sum((y − media(y_test))^2); se muestra en el rótulo del gráfico |

## Diapositiva 7

| Elemento | Serie / categoría | Valor sin redondear | Unidad | Fuente y cálculo |
|---|---|---:|---|---|
| grafico | Observaciones neutrales / 10–99 empleados | 0.409305328861 | proporción | `h3_neutral.csv`: media(jobs_created == jobs_displaced), dentro de cada grupo de dotación |
| grafico | Observaciones neutrales / 100–999 empleados | 0.0566440472777 | proporción | `h3_neutral.csv`: media(jobs_created == jobs_displaced), dentro de cada grupo de dotación |
| grafico | Observaciones neutrales / 1000+ empleados | 0.00345554442102 | proporción | `h3_neutral.csv`: media(jobs_created == jobs_displaced), dentro de cada grupo de dotación |
| texto_redondeado | Mensaje / 18% | 17.9534820641 | porcentaje | `h3_etiquetas.csv`: Recuadro: % de neutrales con empate exacto |
| texto_redondeado | Mensaje / 28% | 28.2206550485 | porcentaje | `h3_etiquetas.csv`: Recuadro: % de neutrales con banda ±0,5% |
| texto_redondeado | Mensaje / 79% | 78.7352528669 | porcentaje | `h3_targets_alternativos.csv`: Recuadro: accuracy en test sin neutral (RF ampliado) |

## Diapositiva 8

| Elemento | Serie / categoría | Valor sin redondear | Unidad | Fuente y cálculo |
|---|---|---:|---|---|
| grafico | Adopción (+10 puntos) / P(creación) / P(neutral) | 2.20360147752 | RRR | `h3_contrastes.csv`: exp(coeficiente MNLogit); adopción/automatización divididas por 10; neutral es referencia |
| texto_redondeado | Mensaje / 2,20 | 2.20360147752 | RRR | `h3_contrastes.csv`: Mensaje: RRR de ai_adoption_rate, net_creation frente a neutral, por +10 puntos |
| texto_redondeado | Mensaje / 0,79 | 0.790093057118 | log(RRR) | `h3_contrastes.csv`: Pie: ejemplo e^coef |
| grafico | Adopción (+10 puntos) / P(desplazamiento) / P(neutral) | 0.470040466699 | RRR | `h3_contrastes.csv`: exp(coeficiente MNLogit); adopción/automatización divididas por 10; neutral es referencia |
| grafico | Automatización (+10 puntos) / P(creación) / P(neutral) | 0.191063203246 | RRR | `h3_contrastes.csv`: exp(coeficiente MNLogit); adopción/automatización divididas por 10; neutral es referencia |
| grafico | Automatización (+10 puntos) / P(desplazamiento) / P(neutral) | 4.94244386276 | RRR | `h3_contrastes.csv`: exp(coeficiente MNLogit); adopción/automatización divididas por 10; neutral es referencia |
| texto_redondeado | Mensaje / 4,94 | 4.94244386276 | RRR | `h3_contrastes.csv`: Mensaje: RRR de task_automation_rate, net_displacement frente a neutral, por +10 puntos |
| contexto | VIF máximo / company_size_Startup | 19.8859870572 | VIF | `h3_vif.csv`: max(1/(1 − R² auxiliar)) del diseño de entrenamiento; no se muestra en la diapositiva |
| texto_redondeado | Mensaje / 0,7 | 0.703666544894 | correlación de Pearson | `data/raw/company_limpio.csv`: Pie: r entre adopción y automatización, todas las filas con ambos datos |

## Diapositiva 9

| Elemento | Serie / categoría | Valor sin redondear | Unidad | Fuente y cálculo |
|---|---|---:|---|---|
| tabla_metricas | Logit lineal / Macro-F1 | 0.67266377728 | F1 | `h3_modelos.csv`: F1=2PR/(P+R); macro-F1=media de F1 de las tres clases |
| tabla_metricas | Logit lineal / F1 creación | 0.739686184462 | F1 | `h3_modelos.csv`: F1=2PR/(P+R); macro-F1=media de F1 de las tres clases |
| tabla_metricas | Logit lineal / F1 desplaz. | 0.708547082862 | F1 | `h3_modelos.csv`: F1=2PR/(P+R); macro-F1=media de F1 de las tres clases |
| tabla_metricas | Logit con curvas / Macro-F1 | 0.675531927467 | F1 | `h3_modelos.csv`: F1=2PR/(P+R); macro-F1=media de F1 de las tres clases |
| tabla_metricas | Logit con curvas / F1 creación | 0.7394466464 | F1 | `h3_modelos.csv`: F1=2PR/(P+R); macro-F1=media de F1 de las tres clases |
| tabla_metricas | Logit con curvas / F1 desplaz. | 0.707808564232 | F1 | `h3_modelos.csv`: F1=2PR/(P+R); macro-F1=media de F1 de las tres clases |
| tabla_metricas | RF base / Macro-F1 | 0.671380300581 | F1 | `h3_modelos.csv`: F1=2PR/(P+R); macro-F1=media de F1 de las tres clases |
| tabla_metricas | RF base / F1 creación | 0.735051231075 | F1 | `h3_modelos.csv`: F1=2PR/(P+R); macro-F1=media de F1 de las tres clases |
| tabla_metricas | RF base / F1 desplaz. | 0.701880506729 | F1 | `h3_modelos.csv`: F1=2PR/(P+R); macro-F1=media de F1 de las tres clases |
| tabla_metricas | RF ampliado / Macro-F1 | 0.674993183432 | F1 | `h3_modelos.csv`: F1=2PR/(P+R); macro-F1=media de F1 de las tres clases |
| tabla_metricas | RF ampliado / F1 creación | 0.738129826439 | F1 | `h3_modelos.csv`: F1=2PR/(P+R); macro-F1=media de F1 de las tres clases |
| tabla_metricas | RF ampliado / F1 desplaz. | 0.706620209059 | F1 | `h3_modelos.csv`: F1=2PR/(P+R); macro-F1=media de F1 de las tres clases |
| contexto | Macro-F1 en validación cruzada / Logit lineal | 0.676610849329 | macro-F1 CV | `h3_modelos_cv.csv`: Promedio en GroupKFold de la configuración elegida en cada familia (empatado con el mejor) |
| contexto | Macro-F1 en validación cruzada / Logit spline | 0.677972326024 | macro-F1 CV | `h3_modelos_cv.csv`: Promedio en GroupKFold de la configuración elegida en cada familia (empatado con el mejor) |
| contexto | Macro-F1 en validación cruzada / RF base | 0.673891138872 | macro-F1 CV | `h3_modelos_cv.csv`: Promedio en GroupKFold de la configuración elegida en cada familia |
| contexto | Macro-F1 en validación cruzada / RF ampliado | 0.678486283703 | macro-F1 CV | `h3_modelos_cv.csv`: Promedio en GroupKFold de la configuración elegida en cada familia (empatado con el mejor) |
| texto_redondeado | Mensaje / 0,002 | 0.0018754343739 | macro-F1 CV | `h3_modelos_cv.csv`: Mensaje: mayor diferencia entre los modelos empatados |
| texto_redondeado | Mensaje / 0,003 | 0.00311954940479 | macro-F1 CV | `h3_modelos_cv.csv`: Mensaje: desvío entre pliegues del mejor (RF ampliado); umbral de empate = mejor − desvío |
| tabla_clases | Neutral / Cuando la predice, acierta | 0.609577221743 | proporción | `h3_modelos.csv`: precision en test de Logit lineal |
| tabla_clases | Neutral / De los casos reales, detecta | 0.534822104466 | proporción | `h3_modelos.csv`: recall en test de Logit lineal |
| tabla_clases | Creación / Cuando la predice, acierta | 0.725743466506 | proporción | `h3_modelos.csv`: precision en test de Logit lineal |
| tabla_clases | Creación / De los casos reales, detecta | 0.754175120961 | proporción | `h3_modelos.csv`: recall en test de Logit lineal |
| tabla_clases | Desplaz. / Cuando la predice, acierta | 0.7040781061 | proporción | `h3_modelos.csv`: precision en test de Logit lineal |
| tabla_clases | Desplaz. / De los casos reales, detecta | 0.713073153658 | proporción | `h3_modelos.csv`: recall en test de Logit lineal |
| texto | Referencia mayoritaria / Accuracy | 0.433990381359 | proporción | `h3_modelos.csv`: media(y_test == clase más frecuente de train) |
| texto_redondeado | Mensaje / 7 de cada 10 | 0.699011041116 | proporción | `h3_modelos.csv`: Pie: accuracy en test de Logit lineal, redondeada a décimos |
| texto_redondeado | Mensaje / 4 de cada 10 | 0.433990381359 | proporción | `h3_modelos.csv`: Pie: accuracy en test de Mayoritaria, redondeada a décimos |

## Diapositiva 10

| Elemento | Serie / categoría | Valor sin redondear | Unidad | Fuente y cálculo |
|---|---|---:|---|---|
| texto_entero | Muestra temporal de test / Mismo trimestre | 37544 | conteo | `validacion_temporal.csv`: Filas con respuesta disponible en 2026; pares calendario exactos para t−1 |
| texto_entero | Muestra temporal de test / Rezago exacto t-1 | 35233 | conteo | `validacion_temporal.csv`: Filas con respuesta disponible en 2026; pares calendario exactos para t−1 |
| grafico | Modelo / Mismo trimestre · H1 | 3.44795349106 | puntos porcentuales | `validacion_temporal.csv`: MAE en 2026; entrenar 2023–24, elegir penalización en 2025 |
| texto_redondeado | Mensaje / 3,45 | 3.44795349106 | puntos porcentuales | `validacion_temporal.csv`: Mensaje: MAE de H1 en 2026, Mismo trimestre |
| grafico | Modelo / Trimestre anterior · H1 | 4.31500613318 | puntos porcentuales | `validacion_temporal.csv`: MAE en 2026; entrenar 2023–24, elegir penalización en 2025 |
| texto_redondeado | Mensaje / 4,32 | 4.31500613318 | puntos porcentuales | `validacion_temporal.csv`: Mensaje: MAE de H1 en 2026, Trimestre anterior |
| grafico | Referencia: siempre el promedio / Mismo trimestre · H1 | 4.79371969041 | puntos porcentuales | `validacion_temporal.csv`: MAE en 2026; entrenar 2023–24, elegir penalización en 2025 |
| grafico | Referencia: siempre el promedio / Trimestre anterior · H1 | 4.78706625949 | puntos porcentuales | `validacion_temporal.csv`: MAE en 2026; entrenar 2023–24, elegir penalización en 2025 |
| grafico | Modelo / Mismo trimestre · H3 | 0.67576609189 | F1 | `validacion_temporal.csv`: macro_F1 en 2026; entrenar 2023–24, elegir penalización en 2025 |
| texto_redondeado | Mensaje / 0,68 | 0.67576609189 | F1 | `validacion_temporal.csv`: Mensaje: macro_F1 de H3 en 2026, Mismo trimestre |
| grafico | Modelo / Trimestre anterior · H3 | 0.529362970181 | F1 | `validacion_temporal.csv`: macro_F1 en 2026; entrenar 2023–24, elegir penalización en 2025 |
| texto_redondeado | Mensaje / 0,53 | 0.529362970181 | F1 | `validacion_temporal.csv`: Mensaje: macro_F1 de H3 en 2026, Trimestre anterior |
| grafico | Referencia: siempre la clase más frecuente / Mismo trimestre · H3 | 0.203914608293 | F1 | `validacion_temporal.csv`: macro_F1 en 2026; entrenar 2023–24, elegir penalización en 2025 |
| grafico | Referencia: siempre la clase más frecuente / Trimestre anterior · H3 | 0.203863154231 | F1 | `validacion_temporal.csv`: macro_F1 en 2026; entrenar 2023–24, elegir penalización en 2025 |

## Comprobación contra el PPTX

Se verificaron 8 gráficos, 35 valores, 12 celdas de métricas, 6 celdas de aciertos por clase y 24 cifras redondeadas en frases. La comprobación falla si una cifra deja de coincidir.

El gráfico del logit muestra la RRR por +10 puntos de adopción o automatización: exp(coeficiente), el factor por el que se multiplica P(clase)/P(neutral). El gráfico derecho de H1 lleva cada pendiente a puntos con el mismo desvío within de inversión que el izquierdo. La diapositiva 9 elige el modelo más simple entre los que quedan a menos de un desvío entre pliegues del mejor en validación cruzada. TWFE usa cambios de una misma empresa y no es intercambiable con el modelo predictivo entre empresas. Las métricas temporales contemporáneas y rezagadas se calculan sobre muestras distintas.
