Guion para el video — IA, productividad y empleo

1. Portada · 40 segundos

“Somos Eric Sigwald, Gonzalo Marengo y Sebastian Rigo. Partimos de una pregunta que parece simple. Cuando una empresa incorpora inteligencia artificial, ¿qué vemos en su productividad y en su empleo?

Del primer práctico retomamos dos hipótesis. La primera, H1, pregunta si una mayor inversión en IA por empleado se asocia con una mayor mejora de productividad. La tercera, H3, pregunta cómo se relacionan la adopción y la automatización con el balance entre puestos creados y desplazados. Para responderlas usamos un panel sintético, donde podemos seguir a las mismas empresas a lo largo de varios trimestres.”

2. Productividad, adopción e inversión · 55 segundos

“Cada fila representa la respuesta de una empresa en un trimestre. En total tenemos más de 150 mil respuestas de unas 10 mil empresas, a lo largo de 16 trimestres.

[Señalar los dos gráficos.] Para tener una primera lectura, tomamos el segundo trimestre de 2026 y usamos las mismas 9.231 empresas en los dos gráficos. En uno las ordenamos por adopción de IA y en el otro por inversión por empleado. En cada grupo preguntamos qué proporción de empresas reportó una mejora de productividad superior al 20%.

En adopción, esa proporción va de casi cero en el grupo más bajo a cerca del 15% en el más alto. En inversión también sube, de aproximadamente 2% a 7,5%. Como cada gráfico ordena a las empresas por una variable distinta, una misma empresa puede quedar en grupos diferentes. Este corte nos muestra el patrón inicial. Ahora queremos saber qué vemos cuando seguimos a una misma empresa en el tiempo.”

3. Curación y diseño de la evaluación · 1 minuto

“Antes de modelar, separamos los datos que podíamos recuperar de los que teníamos que estimar. Por ejemplo, si a una empresa le faltaba la industria en un trimestre y tenía una única industria registrada en sus otras respuestas, podíamos recuperar esa categoría. Así completamos 2.250 valores de industria y otros 2.250 de tamaño. Para la evaluación temporal usamos únicamente categorías observadas hasta ese momento.

Para los predictores numéricos faltantes usamos medianas por industria y tamaño, con la mediana global como respaldo. Las medianas y las escalas se calcularon con los datos de entrenamiento. Si faltaba el resultado que queríamos estudiar, excluíamos esa fila del modelo correspondiente.

[Señalar las dos primeras filas de la tabla.] También separamos dos preguntas. Para evaluar empresas nuevas, reservamos empresas enteras. Para evaluar trimestres posteriores, ordenamos los datos por fecha. Cada prueba representa un uso distinto del modelo.”

4. H1 — Inversión con y sin controlar por adopción · 1 minuto y 15 segundos

“Para estudiar la inversión usamos un modelo con efectos fijos por empresa y por trimestre. En términos simples, comparamos a cada empresa consigo misma, descontando tanto sus características estables como los movimientos que todas comparten en un trimestre.

[Señalar el primer gráfico.] Sobre la misma muestra, un aumento de un desvío típico en la inversión, calculado sobre la variación que queda después de esos ajustes, se asocia con 1,05 puntos de productividad en el modelo sin adopción. Al incluir adopción, la cifra baja a 0,24 puntos. Eso indica que parte de la asociación que observábamos para inversión se comparte con adopción. Cada coeficiente describe una relación condicionada a las otras variables del modelo.

[Pasar al gráfico de sensibilidad.] También revisamos cuánto depende la pendiente de observaciones con valores de predictores muy alejados del resto, lo que llamamos leverage alto. Al retirarlas, el coeficiente de inversión del modelo con adopción sube de 0,294 a 1,603. En cambio, retirar casos con residuos extremos casi no lo mueve. El signo se mantiene positivo en estas pruebas, pero la magnitud cambia mucho según qué observaciones quedan.”

5. H1 — Estimar productividad en empresas nuevas · 45 segundos

“Ahora cambiamos de pregunta. Si recibimos los datos de una empresa que quedó fuera del entrenamiento, ¿qué tan cerca podemos estimar su productividad usando información de ese mismo trimestre?

[Señalar primero la barra de referencia.] Si siempre damos el promedio de entrenamiento, el error medio absoluto es de 4,67 puntos de productividad. Con Ridge baja a 3,36 y con Boosting, que combina árboles, llega a 3,34. Ese error nos dice cuánto se aleja la estimación del valor observado, en promedio.

Los dos modelos mejoran frente a la referencia. En este test, la diferencia entre ellos es de alrededor de dos centésimas de punto. Más adelante vemos qué pasa cuando solo tenemos información del trimestre anterior.”

6. H3 — Qué significa «neutral» · 50 segundos

“Para empleo comparamos cuántos puestos se crearon y cuántos se desplazaron. Si una empresa creó cinco puestos y desplazó cinco, el saldo es cero y queda en la clase neutral. Ese mismo saldo también podría corresponder a una empresa con cero movimientos. La categoría resume el balance y puede reunir situaciones muy distintas.

[Señalar los extremos del gráfico.] Además, el empate exacto aparece en aproximadamente el 41% de las observaciones de empresas de 10 a 99 empleados, y en menos del 1% de las de mil empleados o más. Cuando contamos puestos enteros, la frecuencia del empate depende mucho de la escala. Por eso probamos dos definiciones alternativas, una excluyendo los empates y otra considerando neutral un saldo de hasta medio punto porcentual de la plantilla, en cualquier dirección.”

7. H3 — Cómo leer las asociaciones del logit · 1 minuto

“Usamos un logit multinomial porque tenemos tres resultados posibles. En el gráfico, cada barra compara creación o desplazamiento con la misma categoría de referencia, que es neutral.

[Señalar primero adopción y después automatización.] Para un aumento de diez puntos en adopción, la creación gana peso relativo frente a neutral y el desplazamiento pierde peso relativo. Con diez puntos más de automatización aparece el patrón inverso. Cada comparación mantiene constantes las demás variables del modelo. La altura de la barra está en una escala logarítmica, así que la leemos por su signo y su distancia de cero. Para el video, lo importante es la dirección de cada comparación.

También encontramos que la dotación y la categoría de tamaño aportan información superpuesta. Probamos retirar cada una por separado para revisar la estabilidad. Con estos datos podemos describir cómo se mueven juntas las variables. Para atribuirle a la adopción o a la automatización un efecto sobre los puestos haría falta otro diseño.”

8. H3 — Elección del clasificador y errores por clase · 55 segundos

“Para comparar clasificadores usamos macro-F1. Calculamos un F1 por clase, que combina qué tan precisas son las predicciones y cuántos casos reales recuperamos. Después promediamos las tres clases con el mismo peso, incluida neutral.

[Señalar la tabla.] Elegimos el Random Forest ampliado por validación cruzada agrupada por empresa. En el test final, el logit con spline quedó apenas arriba, 0,676 frente a 0,675. Son resultados muy cercanos y la elección se hizo antes de mirar ese test.

[Señalar la diagonal de la matriz.] Si seguimos la diagonal, el bosque reconoce alrededor del 75% de los casos reales de creación, el 71% de desplazamiento y el 55% de neutral. Ahí se ve qué clase le cuesta más. El promedio por sí solo escondería esa diferencia.”

9. Evaluación temporal y pronóstico · 1 minuto y 10 segundos

“Para acercarnos a un escenario de pronóstico, entrenamos con 2023 y 2024, usamos 2025 para validar y dejamos 2026 para el test. Comparamos dos escenarios. En el primero conocemos las variables del mismo trimestre. En el segundo queremos anticipar el resultado usando solo información del trimestre inmediatamente anterior. Por ejemplo, para predecir el segundo trimestre usamos el primero. Si el primero falta, ese caso queda fuera de la evaluación con rezago.

[Señalar el gráfico de productividad.] Con información del mismo trimestre, Ridge tiene un error de 3,45 puntos. Con un trimestre de anticipación sube a 4,32.

[Señalar el gráfico de empleo.] En empleo, el macro-F1 del logit pasa de 0,676 a 0,529. Los modelos con rezago superan sus respectivas referencias, aunque el desempeño es menor que cuando disponemos de información contemporánea. Las dos evaluaciones tienen muestras distintas porque el rezago exige trimestres consecutivos. Por eso leemos cada resultado junto con su referencia.”

10. Conclusiones · 40 segundos

“En productividad, la inversión mostró una asociación positiva, cuya magnitud se reduce al controlar por adopción y cambia al revisar las observaciones influyentes. En empleo, la adopción se asoció con mayor creación frente a neutral, mientras que la automatización se asoció con mayor desplazamiento frente a neutral.

Cuando intentamos anticipar el trimestre siguiente, encontramos señal en las dos tareas, con un desempeño menor que en la estimación del mismo trimestre. Como trabajamos con un panel sintético, el siguiente paso sería entender mejor cómo se generaron los datos y probar si estos patrones se sostienen en un panel real, con información sobre los usos de IA y las tareas que cambian dentro de cada empresa. Gracias.”