Leí las tres notebooks completas. Te propongo seis slides en el orden del proceso. Cada slide tiene el contenido y la decisión clave que conviene remarcar en la exposición. Calculé unos 90 a 100 segundos por slide.

---

**Slide 1 — Datos y preguntas (≈1 min)**

- Tres archivos en esquema estrella: `company` (150.025 × 43, tabla central), `country` (30 países, contexto macro) e `industry` (9 industrias).
- La estructura es de panel: unas 10.000 empresas observadas en hasta 16 trimestres (2023 Q1 a 2026 Q2).
- Hallazgo temprano: `industry` no aporta información nueva, porque son promedios calculados sobre la propia tabla `company`. Esto se vuelve importante más adelante.
- Pregunta general: más allá del entusiasmo por la IA, ¿qué muestran los datos sobre su efecto en las empresas?

**Slide 2 — EDA: patrones e hipótesis (≈1,5 min)**

- Technology y Finance lideran en nivel de adopción (unos 8 puntos sobre la última industria), pero todas las industrias crecen a ritmo similar. Figura “Evolución de la adopción mediana de IA por industria” (Figura 1).
- La relación entre inversión por empleado y productividad es positiva pero débil (r = 0,19). La madurez digital del país se asocia con la adopción (r = 0,52), con muchas excepciones.
- La adopción y la madurez en IA marcan mucho más diferencia que la inversión. P(mejora > 20 %) pasa de 0,13 % en el cuartil bajo de adopción a 14,8 % en el alto. Los años de uso casi no discriminan.
- Decisiones de método: se usó un solo corte temporal para no tratar las filas repetidas de una empresa como independientes, y `none` en etapa de adopción se conservó como categoría válida en lugar de tratarla como faltante.
- Hipótesis: **H1** inversión → productividad; **H2** diferencias entre industrias con controles; **H3** IA → destrucción o transformación del empleo.

**Slide 3 — Curación: integración, faltantes y outliers (≈2 min)**

- Left join sobre `company`. En `region`, que estaba duplicada, se priorizó la versión de `country`.
- Faltantes: cerca del 1,5 % por variable, pero en filas distintas, así que borrar todas las filas incompletas costaba un 7,3 %. Por eso se decidió variable por variable:
  - target, industria o tamaño faltante → se elimina la fila (no se fabrica la respuesta ni el estrato);
  - predictoras numéricas → mediana del estrato industria × tamaño;
  - categóricas sin respuesta → moda más un indicador de no respuesta.
- **Decisión central: tres tipos de outlier, no uno.**
  - Valores imposibles por definición: 807 (tasas fuera de 0–100, montos negativos).
  - Grupos aislados por un hueco vacío y distribuidos uniformemente: 1.003 valores. Son una huella de contaminación sintética. El ejemplo más claro es el de la satisfacción, con valores de 102 a 104 en una escala de 0 a 10.
  - Colas pesadas legítimas → se conservan. El IQR marcaba alrededor del 18 % como outlier solo por la asimetría.
- Las celdas inválidas se trataron individualmente, y solo se eliminaron filas cuando el inválido era el target. Resultado: unas 143.000 observaciones.

**Slide 4 — Diseño del modelado (≈1,5 min)**

- Control de fuga de información:
  - se excluyeron las columnas `avg_*`, porque predecirían el target con su propio promedio;
  - `ai_stage_enc` (r = 0,86) y `ai_maturity_score` (r = 0,84) quedaron marcadas: no pueden predecir la adopción, ya que son el target medido de otra forma.
- Redundancia: los cuatro indicadores de país se mueven juntos y se redujeron a `gdp_per_capita`. Se aplicó `log1p` a la inversión y a los ingresos por su asimetría.
- **Decisión central: respetar el panel.**
  - Partición train/test agrupada por empresa (8.014 / 2.004 empresas).
  - Validación cruzada con `GroupKFold`.
  - Efectos fijos de empresa y período en H1.
- Priorización: por indicación de la mentora se trabajó primero H1 y luego H3. H2 quedó abierta.
- Para cada hipótesis se ajustó un modelo explicativo y uno predictivo.

**Slide 5 — Resultados (≈2 min)**

- **H1.** Panel con efectos fijos (TWFE):
  - +10 puntos de adopción se asocian con +2,4 puntos de productividad;
  - duplicar la inversión se asocia con apenas unos +0,2 puntos;
  - el spline confirma una curva (casi plana con inversión baja), pero el R² dentro de empresa solo pasa de 0,244 a 0,251.
  - Figura: gráfico de la curva del spline (Figura 2), que compara la curva TWFE spline con la recta del modelo lineal. Muestra que la curva es casi plana con poca inversión y sube después. Usá solo el panel superior: el inferior es la distribución de la inversión y suma ruido.
- **H1 predictiva.** Gradient boosting logra R² = 0,43 y MAE = 3,35 en empresas nuevas, casi igual que Ridge (0,43). El límite está en la información disponible, no en la técnica.
- **H3.** Logit multinomial:
  - +10 puntos de adopción duplican la chance de creación neta y reducen a la mitad la de desplazamiento;
  - +10 puntos de automatización hacen lo contrario (desplazamiento ×4,9).
- **H3 predictiva.** El modelo acierta el 68 % de los casos, frente al 43 % de la referencia. El Random Forest llega al 69 %. La versión ampliada mejora la detección de creación y desplazamiento, pero a costa de la clase neutral: la métrica que se elige cambia cuál es "el mejor" modelo.
  - Figura: logit spline y Random Forest ampliado lado a lado (Figura 3).

**Slide 6 — Conclusiones y límites (≈1,5 min)**

- Adoptar pesa más que invertir.

- La IA no crea ni destruye empleo por sí misma: depende de si acompaña el trabajo o lo reemplaza.
- El sector importa menos de lo que sugería el EDA. La ventaja de Tecnología y Finanzas casi desaparece al controlar por madurez, aunque eso puede ser fuga.
- Límites:
  - el dataset es sintético y tiene huellas de su generador (madurez reconstruible con R² ≈ 0,996, tasas de empleo con r ≈ 0,85 con adopción y automatización);
  - las asociaciones no son causales y se miden en el mismo trimestre;
  - la evaluación es sobre empresas nuevas, no sobre períodos futuros.
- Próximos pasos:
  - validación temporal;
  - variables rezagadas;
  - modelo de efectos mixtos para H2;
  - modelar la reconversión de puestos (`reskilling_rate`).

---