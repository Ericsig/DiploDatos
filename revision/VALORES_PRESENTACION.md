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
| texto_entero | Muestra común 2026 Q2 / Empresas | 9231 | conteo | `eda_cuartiles.csv`: Suma de los cuatro cuartiles; una observación por empresa y muestra común para ambos predictores |
| grafico | Empresas ordenadas por adopción / Grupo 1 (25% más bajo) | 0.00129982668977 | proporción | `eda_cuartiles.csv`: media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2 |
| grafico | Empresas ordenadas por adopción / Grupo 2 | 0.0051993067591 | proporción | `eda_cuartiles.csv`: media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2 |
| grafico | Empresas ordenadas por adopción / Grupo 3 | 0.028596187175 | proporción | `eda_cuartiles.csv`: media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2 |
| grafico | Empresas ordenadas por adopción / Grupo 4 (25% más alto) | 0.14781100997 | proporción | `eda_cuartiles.csv`: media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2 |
| grafico | Empresas ordenadas por inversión / Grupo 1 (25% más bajo) | 0.0216637781629 | proporción | `eda_cuartiles.csv`: media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2 |
| grafico | Empresas ordenadas por inversión / Grupo 2 | 0.0355285961872 | proporción | `eda_cuartiles.csv`: media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2 |
| grafico | Empresas ordenadas por inversión / Grupo 3 | 0.0507152145644 | proporción | `eda_cuartiles.csv`: media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2 |
| grafico | Empresas ordenadas por inversión / Grupo 4 (25% más alto) | 0.0749566724437 | proporción | `eda_cuartiles.csv`: media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2 |
| texto_redondeado | Mensaje / 0,13% | 0.129982668977 | porcentaje | `eda_cuartiles.csv`: Subtítulo: ai_adoption_rate, Q1, % de empresas con mejora > 20 |
| texto_redondeado | Mensaje / 7,5% | 7.49566724437 | porcentaje | `eda_cuartiles.csv`: Subtítulo: ai_investment_per_employee, Q4, % de empresas con mejora > 20 |
| texto_redondeado | Mensaje / 2,2% | 2.16637781629 | porcentaje | `eda_cuartiles.csv`: Subtítulo: ai_investment_per_employee, Q1, % de empresas con mejora > 20 |

## Diapositiva 3

| Elemento | Serie / categoría | Valor sin redondear | Unidad | Fuente y cálculo |
|---|---|---:|---|---|
| texto_entero | Categorías recuperadas / industry | 2250 | celdas | `curacion_resumen.json`: Categoría faltante completada con atributo único observado por empresa |
| texto_entero | Categorías recuperadas / company_size | 2250 | celdas | `curacion_resumen.json`: Categoría faltante completada con atributo único observado por empresa |

## Diapositiva 4

| Elemento | Serie / categoría | Valor sin redondear | Unidad | Fuente y cálculo |
|---|---|---:|---|---|
| texto_entero | Muestra común TWFE / Observaciones | 144743 | conteo | `h1_twfe.csv`: Casos completos de respuesta y controles para las dos especificaciones |
| grafico | Cambio de productividad / Inversión sin adopción | 1.04636185742 | puntos porcentuales | `h1_twfe.csv`: beta × sd(M_empresa,periodo X), ddof=1 |
| grafico | Cambio de productividad / Inversión con adopción | 0.241990655625 | puntos porcentuales | `h1_twfe.csv`: beta × sd(M_empresa,periodo X), ddof=1 |
| grafico | Cambio de productividad / Adopción con inversión | 2.33610992155 | puntos porcentuales | `h1_twfe.csv`: beta × sd(M_empresa,periodo X), ddof=1 |
| grafico | Modelo sin adopción / Todos los datos | 1.2733880239 | coeficiente de log1p(inversión) | `h1_sensibilidad.csv`: Reajuste TWFE en muestra: Completa; EE agrupados por empresa |
| grafico | Modelo sin adopción / Sin puntos muy alejados (leverage alto) | 4.4260162419 | coeficiente de log1p(inversión) | `h1_sensibilidad.csv`: Reajuste TWFE en muestra: Sin leverage alto; EE agrupados por empresa |
| grafico | Modelo sin adopción / Sin errores muy grandes (residuos) | 1.27390762023 | coeficiente de log1p(inversión) | `h1_sensibilidad.csv`: Reajuste TWFE en muestra: Sin residuos ∣z∣>3.5; EE agrupados por empresa |
| grafico | Modelo con adopción / Todos los datos | 0.294494682299 | coeficiente de log1p(inversión) | `h1_sensibilidad.csv`: Reajuste TWFE en muestra: Completa; EE agrupados por empresa |
| grafico | Modelo con adopción / Sin puntos muy alejados (leverage alto) | 1.60319982473 | coeficiente de log1p(inversión) | `h1_sensibilidad.csv`: Reajuste TWFE en muestra: Sin leverage alto; EE agrupados por empresa |
| grafico | Modelo con adopción / Sin errores muy grandes (residuos) | 0.294507051695 | coeficiente de log1p(inversión) | `h1_sensibilidad.csv`: Reajuste TWFE en muestra: Sin residuos ∣z∣>3.5; EE agrupados por empresa |
| texto_entero | Filas con leverage alto / Retiradas | 2187 | conteo | `h1_sensibilidad.csv`: n(Completa) − n(Sin leverage alto), modelo con adopción |
| texto_redondeado | Mensaje / 1,5% | 1.5109538976 | porcentaje | `h1_sensibilidad.csv`: Filas retiradas / n(Completa) |
| texto_redondeado | Mensaje / 0,29 | 0.294494682299 | coeficiente de log1p(inversión) | `h1_sensibilidad.csv`: Mensaje: pendiente con adopción, muestra Completa |
| texto_redondeado | Mensaje / 1,60 | 1.60319982473 | coeficiente de log1p(inversión) | `h1_sensibilidad.csv`: Mensaje: pendiente con adopción, muestra Sin leverage alto |

## Diapositiva 5

| Elemento | Serie / categoría | Valor sin redondear | Unidad | Fuente y cálculo |
|---|---|---:|---|---|
| grafico | MAE en empresas nuevas / Siempre el promedio (referencia) | 4.6657221533 | puntos porcentuales | `h1_prediccion.csv`: media(abs(y_test − pred_test)) |
| grafico | MAE en empresas nuevas / Ridge | 3.35674337599 | puntos porcentuales | `h1_prediccion.csv`: media(abs(y_test − pred_test)) |
| grafico | MAE en empresas nuevas / Gradient boosting | 3.34062624123 | puntos porcentuales | `h1_prediccion.csv`: media(abs(y_test − pred_test)) |
| texto | R² en test / Ridge | 0.428357856768 | R² | `h1_prediccion.csv`: 1 − sum((y − pred)^2) / sum((y − media(y_test))^2) |
| texto_redondeado | Mensaje / 42,8% | 42.8357856768 | porcentaje de variación explicada | `h1_prediccion.csv`: 100 × R² en test de Ridge |
| texto | R² en test / Gradient boosting | 0.434993251533 | R² | `h1_prediccion.csv`: 1 − sum((y − pred)^2) / sum((y − media(y_test))^2) |
| texto_redondeado | Mensaje / 43,5% | 43.4993251533 | porcentaje de variación explicada | `h1_prediccion.csv`: 100 × R² en test de Gradient boosting |

## Diapositiva 6

| Elemento | Serie / categoría | Valor sin redondear | Unidad | Fuente y cálculo |
|---|---|---:|---|---|
| grafico | Observaciones neutrales / 10–99 empleados | 0.409305328861 | proporción | `h3_neutral.csv`: media(jobs_created == jobs_displaced), dentro de cada grupo de dotación |
| grafico | Observaciones neutrales / 100–999 empleados | 0.0566440472777 | proporción | `h3_neutral.csv`: media(jobs_created == jobs_displaced), dentro de cada grupo de dotación |
| grafico | Observaciones neutrales / 1000+ empleados | 0.00345554442102 | proporción | `h3_neutral.csv`: media(jobs_created == jobs_displaced), dentro de cada grupo de dotación |

## Diapositiva 7

| Elemento | Serie / categoría | Valor sin redondear | Unidad | Fuente y cálculo |
|---|---|---:|---|---|
| grafico | Adopción (+10 puntos) / Creación frente a neutral | 0.790093057118 | log(RRR) | `h3_contrastes.csv`: Coeficiente MNLogit; adopción/automatización divididas por 10; neutral es referencia |
| texto_redondeado | Mensaje / 2,2 | 2.20360147752 | RRR | `h3_contrastes.csv`: Mensaje: exp(coef) de ai_adoption_rate, net_creation frente a neutral, por +10 puntos |
| grafico | Adopción (+10 puntos) / Desplazamiento frente a neutral | -0.754936488624 | log(RRR) | `h3_contrastes.csv`: Coeficiente MNLogit; adopción/automatización divididas por 10; neutral es referencia |
| grafico | Automatización (+10 puntos) / Creación frente a neutral | -1.65515099863 | log(RRR) | `h3_contrastes.csv`: Coeficiente MNLogit; adopción/automatización divididas por 10; neutral es referencia |
| grafico | Automatización (+10 puntos) / Desplazamiento frente a neutral | 1.59785991793 | log(RRR) | `h3_contrastes.csv`: Coeficiente MNLogit; adopción/automatización divididas por 10; neutral es referencia |
| texto_redondeado | Mensaje / 4,9 | 4.94244386276 | RRR | `h3_contrastes.csv`: Mensaje: exp(coef) de task_automation_rate, net_displacement frente a neutral, por +10 puntos |
| contexto | VIF máximo / company_size_Startup | 19.8859870572 | VIF | `h3_vif.csv`: max(1/(1 − R² auxiliar)) del diseño de entrenamiento; no se muestra en la diapositiva |
| texto_redondeado | Mensaje / 0,7 | 0.703666544894 | correlación de Pearson | `data/raw/company_limpio.csv`: Pie: r entre adopción y automatización, todas las filas con ambos datos |

## Diapositiva 8

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
| matriz | Neutral / Neutral | 0.54542013626 | proporción por fila | `h3_matrices.csv`: conteo(real, predicha) / sum_predicha conteo(real, predicha) |
| matriz | Neutral / Creación | 0.233345950038 | proporción por fila | `h3_matrices.csv`: conteo(real, predicha) / sum_predicha conteo(real, predicha) |
| matriz | Neutral / Desplaz. | 0.221233913702 | proporción por fila | `h3_matrices.csv`: conteo(real, predicha) / sum_predicha conteo(real, predicha) |
| matriz | Creación / Neutral | 0.0709380365226 | proporción por fila | `h3_matrices.csv`: conteo(real, predicha) / sum_predicha conteo(real, predicha) |
| matriz | Creación / Creación | 0.75339472452 | proporción por fila | `h3_matrices.csv`: conteo(real, predicha) / sum_predicha conteo(real, predicha) |
| matriz | Creación / Desplaz. | 0.175667238957 | proporción por fila | `h3_matrices.csv`: conteo(real, predicha) / sum_predicha conteo(real, predicha) |
| matriz | Desplaz. / Neutral | 0.0751662583129 | proporción por fila | `h3_matrices.csv`: conteo(real, predicha) / sum_predicha conteo(real, predicha) |
| matriz | Desplaz. / Creación | 0.214998249912 | proporción por fila | `h3_matrices.csv`: conteo(real, predicha) / sum_predicha conteo(real, predicha) |
| matriz | Desplaz. / Desplaz. | 0.709835491775 | proporción por fila | `h3_matrices.csv`: conteo(real, predicha) / sum_predicha conteo(real, predicha) |
| contexto | Selección por CV / RF ampliado | 0.678486283703 | macro-F1 CV | `h3_modelos_cv.csv`: max de macro-F1 promedio en GroupKFold, sin elegir con test |
| texto | Referencia mayoritaria / Accuracy | 0.433990381359 | proporción | `h3_modelos.csv`: media(y_test == clase más frecuente de train) |
| texto_redondeado | Mensaje / 7 de cada 10 | 0.699315857211 | proporción | `h3_modelos.csv`: Mensaje: accuracy en test de RF ampliado, redondeada a décimos |
| texto_redondeado | Mensaje / 4 de cada 10 | 0.433990381359 | proporción | `h3_modelos.csv`: Mensaje: accuracy en test de Mayoritaria, redondeada a décimos |
| texto_redondeado | Mensaje / 55% | 54.542013626 | porcentaje | `h3_modelos.csv`: Pie: recall de neutral del RF ampliado |

## Diapositiva 9

| Elemento | Serie / categoría | Valor sin redondear | Unidad | Fuente y cálculo |
|---|---|---:|---|---|
| texto_entero | Muestra temporal de test / Mismo trimestre | 37544 | conteo | `validacion_temporal.csv`: Filas con respuesta disponible en 2026; pares calendario exactos para t−1 |
| texto_entero | Muestra temporal de test / Rezago exacto t-1 | 35233 | conteo | `validacion_temporal.csv`: Filas con respuesta disponible en 2026; pares calendario exactos para t−1 |
| grafico | Modelo / Mismo trimestre · H1 | 3.44795349106 | puntos porcentuales | `validacion_temporal.csv`: MAE en 2026; entrenar 2023–24, elegir penalización en 2025 |
| texto_redondeado | Mensaje / 3,45 | 3.44795349106 | puntos porcentuales | `validacion_temporal.csv`: Mensaje: MAE de H1 en 2026, Mismo trimestre |
| grafico | Modelo / Trimestre anterior · H1 | 4.31500613318 | puntos porcentuales | `validacion_temporal.csv`: MAE en 2026; entrenar 2023–24, elegir penalización en 2025 |
| texto_redondeado | Mensaje / 4,32 | 4.31500613318 | puntos porcentuales | `validacion_temporal.csv`: Mensaje: MAE de H1 en 2026, Trimestre anterior |
| grafico | Referencia sin modelo / Mismo trimestre · H1 | 4.79371969041 | puntos porcentuales | `validacion_temporal.csv`: MAE en 2026; entrenar 2023–24, elegir penalización en 2025 |
| grafico | Referencia sin modelo / Trimestre anterior · H1 | 4.78706625949 | puntos porcentuales | `validacion_temporal.csv`: MAE en 2026; entrenar 2023–24, elegir penalización en 2025 |
| grafico | Modelo / Mismo trimestre · H3 | 0.67576609189 | F1 | `validacion_temporal.csv`: macro_F1 en 2026; entrenar 2023–24, elegir penalización en 2025 |
| texto_redondeado | Mensaje / 0,68 | 0.67576609189 | F1 | `validacion_temporal.csv`: Mensaje: macro_F1 de H3 en 2026, Mismo trimestre |
| grafico | Modelo / Trimestre anterior · H3 | 0.529362970181 | F1 | `validacion_temporal.csv`: macro_F1 en 2026; entrenar 2023–24, elegir penalización en 2025 |
| texto_redondeado | Mensaje / 0,53 | 0.529362970181 | F1 | `validacion_temporal.csv`: Mensaje: macro_F1 de H3 en 2026, Trimestre anterior |
| grafico | Referencia sin modelo / Mismo trimestre · H3 | 0.203914608293 | F1 | `validacion_temporal.csv`: macro_F1 en 2026; entrenar 2023–24, elegir penalización en 2025 |
| grafico | Referencia sin modelo / Trimestre anterior · H3 | 0.203863154231 | F1 | `validacion_temporal.csv`: macro_F1 en 2026; entrenar 2023–24, elegir penalización en 2025 |

## Comprobación contra el PPTX

Se verificaron 8 gráficos, 35 valores, 12 celdas de métricas, 9 celdas de la matriz de confusión y 18 cifras redondeadas en frases. La comprobación falla si una cifra deja de coincidir.

El coeficiente de adopción/automatización del logit se expresa por +10 puntos y en log(RRR); exponenciarlo da la RRR frente a neutral. TWFE usa cambios de una misma empresa y no es intercambiable con el modelo predictivo entre empresas. Las métricas temporales contemporáneas y rezagadas se calculan sobre muestras distintas.
