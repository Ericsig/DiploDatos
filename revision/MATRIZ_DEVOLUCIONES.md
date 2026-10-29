# Cobertura de la devolución docente

Revisión del 29/10/2026. Equipo: Eric Sigwald, Gonzalo Marengo y Sebastian Rigo.

| Devolución | Corrección verificable |
|---|---|
| TP2: extensión, contexto TP1 y dos hipótesis | La presentación integrada de entrega es `deck/IA_en_las_empresas_presentation_v2.pptx`: H1/H3 antes de datos, contexto y curación resumidos. La reentrega separada de TP2 no forma parte de esta versión seleccionada por el equipo. |
| Integrantes | Nombres en ambas portadas y notebooks, identidades de Git y confirmación de Gonzalo Marengo. |
| Caso testigo confuso | Curación sección 5 compara franjas de la misma variable, con unidad y recuentos recalculados. Distingue facturación de beneficio. |
| Redundancia confusa | Curación sección 8: familia, comparación y decisión explícita. Una correlación alta no demuestra fuga. |
| Datos recuperables entre trimestres | Curación sección 4: atributo único observado por empresa; conflictos y faltantes residuales informados. Temporal: solo arrastre desde el pasado. |
| Mediana por estrato y targets | Se conserva mediana industria×tamaño con respaldo global. Exportación observada para TP3; las respuestas no se imputan. Predictoras se imputan dentro de cada fit. |
| Ética/privacidad | Moda por industria×tamaño, respaldo global e indicador de ausencia. |
| Ordinalidad de tamaño | Distribuciones de empleados e ingresos calculadas. Se conserva nominal en modelos, sin imponer distancias entre categorías. |
| Año y trimestre | Índice continuo `4*(año-2023)+trimestre-1`, unicidad y orden del panel. `quarter` aislado solo representa estacionalidad. |
| Skew | Comparación de forma antes/después de log1p, sin comparar medias de unidades distintas ni afirmar normalidad. |
| Árboles y explicación | Se corrige la exclusión conceptual de árboles. Se distingue exploración de asociaciones, interpretación de parámetros y causalidad. |
| Leverage y normalidad | TWFE con proyección de ambos efectos, leverage de pendientes, VIF within, Q–Q, skew/curtosis y sensibilidades por filas/empresas/residuos extremos. |
| TWFE con/sin adopción | Misma muestra observada, dos preguntas condicionales, errores agrupados. No se interpreta diferencia como mediación probada. |
| Comparación de magnitudes | Cambios por un desvío e IQR de predictores residualizados por ambos efectos fijos. |
| H3 y signos opuestos | Modelos de componentes en tasas, correlación y AUC por empresa para adopción, automatización y ambas. Se retira el mecanismo causal inferido de nombres. |
| Neutral | Prevalencia por dotación, conteos pequeños, tabla de etiquetas y reentrenamiento con banda ±0,5% y excluyendo neutral. Tareas no comparables directamente. |
| Colinealidad H3 | VIF, rango, errores agrupados y sensibilidad retirando dotación o tamaño, con desempeño. |
| Elección RF ampliado y métrica | Macro-F1 de tres clases en todos los grids y selección de familia; F1 empleo secundaria. Se reporta precisión/recall/F1 por clase, accuracy, log-loss y bootstrap por empresa. |
| Empresas vs. futuro | GroupKFold y 80/20 por empresa se conservan. Validación temporal 2023–24/2025/2026 se ejecuta como experimento distinto. |
| Rezagos con huecos | Join exacto por empresa y trimestre calendario; prueba que un salto de dos trimestres no produce lag. |
| TP3: pregunta/hipótesis y modelos antes de resultados | Presentación v2 de diez slides. Cada modelo declara respuesta, finalidad y funcionamiento antes de su tabla. H2 fuera de las conclusiones. |
| TP3: porcentaje aislado de productividad | Barras editables por cuatro cuartiles de adopción/inversión, muestra común de 2026 Q2, umbral >20% explícito. |
| TP3: tabla mezclada y titulares/matrices incoherentes | Resultados junto a cada hipótesis; tabla final con nombres exactos de modelos y métricas. No se reutilizan imágenes o números históricos. |

Los resultados son exploratorios: la muestra histórica de test ya se había consultado. La revisión fija una métrica estable, sin fingir que fue fijada antes del trabajo original. El dataset sintético requiere validación externa para cualquier aplicación real.

Las cifras de la presentación se verifican con `scripts/calcular_valores_presentacion.py` y se documentan en `VALORES_PRESENTACION.md`.
