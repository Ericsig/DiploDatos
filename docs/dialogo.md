Guion para la presentación — IA, productividad y empleo

Duración total: unos 9 minutos y 45 segundos a ritmo tranquilo. Va en las notas de cada diapositiva de la v3.

1. Portada · 35 segundos

“Somos Eric Sigwald, Gonzalo Marengo y Sebastian Rigo. Nos preguntamos qué pasa con la productividad y el empleo de una empresa cuando incorpora inteligencia artificial.

Planteamos dos hipótesis. H1: ¿más inversión en IA por empleado se asocia con una mayor mejora de productividad? H2: ¿cómo se relacionan la adopción y la automatización con el balance entre puestos creados y desplazados? Trabajamos con datos sintéticos, es decir simulados, que siguen a las mismas empresas durante varios trimestres. Por eso hablamos de asociaciones, no de causas.”

2. Los datos y cómo los limpiamos · 55 segundos

“Partimos de un panel con 150.025 respuestas de 10.025 empresas, encuestadas trimestre a trimestre entre 2023 y 2026.

[Señalar la tabla, fila por fila.] Encontramos cuatro problemas. A algunas filas les faltaba la industria o el tamaño, pero la empresa los tenía en otros trimestres: los recuperamos, 2.250 de cada uno. Otras filas no tenían adopción, o la tenían fuera de rango. Como la adopción es algo que estudiamos, no la inventamos: sacamos esas filas. Había también valores imposibles o aislados en otras variables, como ingresos negativos. Ahí corregimos solo la celda, con la mediana de empresas de la misma industria y tamaño. Y no encontramos duplicados.

Quedan 147.471 respuestas de 10.019 empresas. Cada modelo usa las filas que tienen todo lo que necesita, por eso el número cambia un poco entre diapositivas.”

3. Entrenamiento y prueba · 35 segundos

“Para no evaluar a un modelo con datos que ya vio, separamos según la pregunta.

[Señalar la tabla.] Para saber si sirve en empresas que nunca vio, reservamos el 20% de las empresas, enteras, para la prueba. Para saber si sirve hacia adelante, entrenamos con 2023 y 2024, ajustamos con 2025 y probamos con 2026. Y los rellenos, como las medianas, se calculan solo con los datos de entrenamiento.”

4. Primer vistazo · 50 segundos

“Para un primer vistazo tomamos un solo trimestre, el segundo de 2026, con 9.231 empresas. Las ordenamos dos veces, por adopción de IA y por inversión por empleado, y cada vez las partimos en cuartiles: cuatro grupos con el 25% de las empresas cada uno.

[Señalar el eje vertical.] Cada barra dice qué porcentaje de las empresas de ese cuartil mejoró su productividad más de un 20%.

[Señalar el último cuartil.] En el cuartil de mayor adopción es casi el 15%; en el de menor adopción, 0,13%. Por inversión también sube, pero menos: de 2,2% a 7,5%. Esto compara empresas distintas en un mismo momento. Ahora seguimos a cada empresa en el tiempo.”

5. H1 — Inversión y productividad · 1 minuto y 15 segundos

“¿Cuando una empresa invierte más en IA, mejora más su productividad? Para responderlo usamos un modelo TWFE, de efectos fijos. Compara a cada empresa consigo misma en el tiempo y descuenta lo que les pasó a todas en ese trimestre. Es un modelo para explicar, no para predecir, y usa las 144.743 respuestas que tienen productividad, inversión e ingresos.

[Señalar el gráfico de la izquierda.] Para comparar variables usamos la misma vara: un aumento típico de cada una dentro de la empresa. Un aumento típico de inversión se asocia con 1,05 puntos más de productividad. Si el modelo también incluye adopción, baja a 0,24, y la adopción se asocia con 2,34. Inversión y adopción se mueven juntas, y comparten parte de la asociación.

[Pasar al gráfico de la derecha.] Este gráfico está en la misma unidad. Probamos sacar 2.187 filas, el 1,5%, con valores muy alejados del resto: lo que se llama leverage alto. En el modelo con adopción, la asociación de la inversión sube de 0,24 a 1,32 puntos. Sacar los casos con errores muy grandes casi no la mueve. El signo se mantiene, pero el tamaño depende de pocos casos.”

6. H1 — Estimar en empresas nuevas · 45 segundos

“Ahora cambiamos de objetivo: ¿podemos estimar la productividad de una empresa que el modelo nunca vio? Comparamos dos modelos para predecir. Ridge es una regresión lineal que frena los coeficientes para no sobreajustar; boosting combina muchos árboles de decisión.

[Señalar el eje.] Medimos el MAE, el error promedio en puntos de productividad. La referencia es no usar modelo y predecir siempre el promedio de entrenamiento: se equivoca 4,67 puntos. Ridge baja a 3,36 y boosting a 3,34. Debajo de cada barra está el R²: los dos explican alrededor del 43% de la variación. El modelo más complejo casi no mejora.”

7. H2 — Creación, desplazamiento y neutral · 55 segundos

“Pasamos a empleo. Cada observación cae en una de tres clases: creación si se crearon más puestos de los que se desplazaron, desplazamiento si pasó al revés, y neutral si hay empate exacto.

[Señalar el gráfico.] El empate depende mucho del tamaño: pasa en el 41% de las observaciones de empresas de 10 a 99 empleados y en menos del 1% de las de mil o más. Con pocos puestos, empatar es fácil.

[Señalar el recuadro.] Probamos otras dos definiciones. Sin neutral, el modelo acierta 79%, pero solo separa creación de desplazamiento. Con una banda de más o menos medio punto de la plantilla, neutral pasa del 18% al 28% de los casos. Las dos cambian la pregunta, así que sus métricas no se comparan con las de tres clases. Nos quedamos con el empate exacto, que es la pregunta original.”

8. H2 — Qué se asocia con crear o desplazar · 1 minuto y 10 segundos

“¿Qué se asocia con que una empresa cree o desplace puestos, en vez de quedar neutral? Lo estimamos con un logit multinomial, un modelo para explicar que sirve cuando hay más de dos resultados.

El modelo compara cocientes de probabilidades: la probabilidad de creación dividida por la de neutral, y la de desplazamiento dividida por la de neutral. Cada barra es un RRR, una razón de riesgos relativos: cuánto se multiplica ese cociente cuando una variable sube diez puntos y las demás quedan fijas. Uno significa sin cambio.

[Señalar adopción y después automatización.] Con diez puntos más de adopción, el cociente de creación se multiplica por 2,20. Con diez puntos más de automatización, el de desplazamiento se multiplica por 4,94. Las barras por debajo de uno muestran que, en cada caso, la otra clase retrocede.

Adopción y automatización suben juntas, por eso sus efectos se compensan. Decir que una “acompaña” y la otra “reemplaza” sería leer los nombres de las variables: para afirmarlo haría falta saber en qué se usa la IA.”

9. H2 — Elegir el clasificador · 1 minuto y 10 segundos

“Ahora queremos predecir la clase en empresas nuevas. [Señalar la tabla.] Comparamos cuatro versiones. El logit lineal supone una relación en línea recta con cada variable; el logit con curvas permite que esa relación se doble. El Random Forest son muchos árboles que votan: la versión base usa una configuración estándar y la ampliada prueba más opciones.

Fijamos de antemano la métrica: macro-F1. Va de 0 a 1, combina acertar cuando el modelo predice una clase con no dejar casos reales afuera, y pesa igual a las tres clases.

En validación cruzada, tres modelos quedan a menos de dos milésimas entre sí, menos de lo que varía el resultado entre particiones. Ante un empate elegimos el más simple: el logit lineal, que además es el mismo tipo de modelo que usamos para explicar.

[Señalar la tabla chica.] Acierta 7 de cada 10, contra 4 de cada 10 si predijéramos siempre la clase más frecuente. Detecta el 75% de las creaciones y el 71% de los desplazamientos, pero solo el 53% de los neutrales: es la clase que más cuesta.”

10. Anticipar el trimestre siguiente · 55 segundos

“Hasta acá usamos datos del mismo trimestre: eso explica, pero no anticipa. Para acercarnos a un pronóstico entrenamos con 2023 y 2024, ajustamos con 2025 y probamos con 2026, de dos maneras: con datos del mismo trimestre y solo con los del trimestre anterior. Si el trimestre anterior falta, ese caso queda afuera.

La referencia es lo que se obtiene sin modelo: el promedio para productividad y la clase más frecuente para empleo.

[Señalar el gráfico de productividad.] Acá menos es mejor: el error de Ridge pasa de 3,45 a 4,32 puntos, contra 4,79 de la referencia.

[Señalar el gráfico de empleo.] Acá más es mejor: el macro-F1 del logit baja de 0,68 a 0,53, contra 0,20 de la referencia. Anticipar cuesta, pero queda señal.”

11. Conclusiones · 40 segundos

“En productividad, dentro de una misma empresa, más inversión se asocia con más productividad. Pero ese tamaño baja al controlar por adopción y cambia mucho con pocos casos extremos.

En empleo, más adopción se asocia con más creación y más automatización con más desplazamiento, siempre frente a neutral. Los datos no alcanzan para decir por qué.

Anticipar un trimestre es posible, pero se predice peor. Como son datos sintéticos, los pasos siguientes son entender cómo se generaron, mirar en qué se usa la IA en cada empresa y probar estos patrones en datos reales. Gracias.”
