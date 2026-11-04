Guion para la presentación — IA, productividad y empleo

Duración total: unos 9 minutos y 45 segundos a ritmo tranquilo. Va en las notas de cada diapositiva de la v3.

1. Portada · 40 segundos

“Somos Eric Sigwald, Gonzalo Marengo y Sebastian Rigo. Partimos de una pregunta simple: cuando una empresa incorpora inteligencia artificial, ¿qué vemos en su productividad y en su empleo?

Del primer práctico retomamos dos hipótesis. H1: ¿más inversión en IA por empleado se asocia con una mayor mejora de productividad? H3: ¿cómo se relacionan la adopción y la automatización con el balance entre puestos creados y desplazados? Trabajamos con datos sintéticos, es decir simulados, que siguen a las mismas empresas durante varios trimestres. Por eso vamos a hablar de asociaciones, no de causas.”

2. Primer vistazo · 1 minuto

“Tenemos más de 150 mil respuestas de unas 10 mil empresas, a lo largo de 16 trimestres.

Para un primer vistazo tomamos un solo trimestre, el segundo de 2026, con 9.231 empresas. Las ordenamos dos veces, una por adopción de IA y otra por inversión por empleado, y cada vez las partimos en cuatro grupos iguales.

[Señalar el eje vertical.] La altura de cada barra responde una pregunta: de las empresas de ese grupo, ¿qué porcentaje mejoró su productividad más de un 20%?

[Señalar el último grupo.] Ordenadas por adopción, el porcentaje va de 0,13% en el grupo más bajo a casi 15% en el más alto. Ordenadas por inversión también sube, pero menos: de 2,2% a 7,5%. Como son dos órdenes distintos, una misma empresa puede estar en grupos diferentes. Esto muestra el patrón, pero compara empresas distintas. Ahora queremos ver qué pasa cuando seguimos a la misma empresa en el tiempo.”

3. Preparación y evaluación · 50 segundos

“Antes de modelar, recuperamos lo que estaba en otra parte. Si a una empresa le faltaba la industria en un trimestre, pero la tenía registrada en otros, la completamos. Así recuperamos 2.250 datos de industria y 2.250 de tamaño, en lugar de borrar esas filas.

Los otros números faltantes los rellenamos con medianas calculadas solo con los datos de entrenamiento. Lo que nunca rellenamos es el resultado que queremos estudiar: si falta, esa fila queda fuera de ese modelo.

[Señalar la tabla.] También separamos dos preguntas distintas. Para saber si el modelo sirve en empresas que nunca vio, reservamos empresas enteras. Para saber si sirve hacia adelante, entrenamos con años anteriores y probamos con 2026.”

4. H1 — Inversión y productividad · 1 minuto y 25 segundos

“Empezamos por explicar. Lo que queremos entender es el cambio porcentual de productividad, y usamos un modelo llamado TWFE, de efectos fijos. En palabras simples: compara a cada empresa consigo misma en el tiempo y descuenta lo que le pasó a todas en ese trimestre.

[Señalar el gráfico de la izquierda.] Para comparar variables en una misma vara, miramos un aumento típico de cada una dentro de la empresa. Un aumento típico de inversión se asocia con 1,05 puntos más de productividad cuando el modelo no incluye adopción. Si incluimos adopción, baja a 0,24. Y un aumento típico de adopción se asocia con 2,34 puntos. Inversión y adopción se mueven juntas, por eso comparten parte de la asociación. Con estos datos no podemos decir que la inversión actúa a través de la adopción.

[Pasar al gráfico de la derecha.] Acá miramos la pendiente del modelo, por eso los números son otros. Probamos sacar 2.187 filas muy alejadas del resto en sus variables, lo que se llama leverage alto: son apenas el 1,5%. La pendiente de inversión sube de 0,29 a 1,60. En cambio, sacar los casos con errores muy grandes casi no la mueve. Conclusión: el signo se mantiene positivo, pero el tamaño depende mucho de pocos casos.”

5. H1 — Estimar en empresas nuevas · 45 segundos

“Ahora cambiamos de objetivo: de explicar a predecir. Si llega una empresa que el modelo no vio, ¿qué tan cerca podemos estimar su productividad con datos de ese mismo trimestre?

Comparamos dos modelos. Ridge es una regresión lineal que frena los coeficientes para no sobreajustar. Boosting combina muchos árboles de decisión y puede captar curvas.

[Señalar primero la barra de referencia.] Si siempre respondemos el promedio, nos equivocamos 4,67 puntos en promedio. Ridge baja a 3,36 y boosting a 3,34. Los dos explican alrededor del 43% de la variación en empresas nuevas. El modelo más complejo casi no mejora: la diferencia es de unas dos centésimas de punto.”

6. H3 — Creación, desplazamiento y neutral · 55 segundos

“Pasamos a empleo. Comparamos puestos creados y desplazados, y cada observación cae en una de tres clases: creación si se crearon más, desplazamiento si se desplazaron más, y neutral si hay empate exacto.

Neutral es una clase engañosa. Una empresa que creó cinco y desplazó cinco es neutral, y una que no movió ningún puesto también. La mitad de los empates son de dos puestos o menos.

[Señalar los extremos del gráfico.] Empatar es mucho más fácil cuando se cuentan pocos puestos: pasa en el 41% de las observaciones de empresas de 10 a 99 empleados y en menos del 1% de las de mil o más. Por eso probamos dos alternativas: sacar neutral, o llamar neutral a un saldo de hasta medio punto porcentual de la plantilla.”

7. H3 — Qué se asocia con crear o desplazar · 1 minuto y 15 segundos

“Para explicar usamos un logit multinomial, que sirve cuando hay más de dos resultados posibles. Cada barra compara creación o desplazamiento contra neutral, dejando fijas las demás variables. Barra hacia arriba significa que esa clase gana terreno frente a neutral; barra hacia abajo, que pierde.

[Señalar adopción y después automatización.] Con diez puntos más de adopción, la chance de creación frente a neutral se multiplica por 2,2. Con diez puntos más de automatización, la chance de desplazamiento se multiplica por 4,9. Y en cada caso, la otra clase retrocede.

¿Por qué efectos tan grandes y opuestos? Porque el saldo es una resta, creados menos desplazados, y porque adopción y automatización suben juntas. Sus efectos se compensan, y el modelo los separa manteniendo una fija mientras mueve la otra. Decir que la adopción “acompaña” y la automatización “reemplaza” sería leer los nombres de las variables: para afirmarlo necesitaríamos saber en qué se usa la IA.

También vimos que cantidad de empleados y categoría de tamaño dicen casi lo mismo. Sacar la categoría de tamaño casi no cambia el desempeño.”

8. H3 — Elegir el clasificador · 1 minuto y 10 segundos

“Ahora queremos predecir la clase en empresas nuevas. Comparamos logit con Random Forest, que son muchos árboles que votan. Cada uno tiene dos versiones: logit con curvas y Random Forest con más configuraciones probadas.

Fijamos de antemano la métrica: macro-F1. El F1 va de 0 a 1 y combina acertar cuando el modelo predice una clase con no dejar casos reales afuera. Macro significa que promediamos las tres clases con el mismo peso, incluida neutral.

[Señalar la tabla.] Elegimos por validación cruzada separando por empresa, sin usar el test, y ganó el Random Forest ampliado. En el test los cuatro quedan casi empatados: el logit con curvas queda apenas arriba, 0,676 contra 0,675, pero no cambiamos la elección por eso. El elegido acierta 7 de cada 10, frente a 4 de cada 10 si predijéramos siempre la clase más frecuente.

[Señalar la diagonal de la matriz.] La diagonal muestra los aciertos por clase: 75% en creación, 71% en desplazamiento y 55% en neutral. Neutral es la que más le cuesta, y el promedio solo lo escondería.”

9. Anticipar el trimestre siguiente · 1 minuto

“Hasta acá explicamos resultados con datos del mismo trimestre. Eso no es anticipar. Para acercarnos a un pronóstico, entrenamos con 2023 y 2024, ajustamos con 2025 y probamos con 2026, de dos maneras: con datos del mismo trimestre y solo con datos del trimestre anterior. Si el trimestre anterior falta, ese caso queda afuera: no saltamos huecos.

[Señalar el gráfico de productividad.] Acá menos es mejor. Con datos del mismo trimestre, el error de Ridge es de 3,45 puntos. Con el trimestre anterior sube a 4,32. La referencia, sin modelo, está en 4,79.

[Señalar el gráfico de empleo.] Acá más es mejor. El macro-F1 del logit pasa de 0,68 a 0,53, contra 0,20 de la referencia.

Anticipar cuesta, pero queda señal: los dos modelos le ganan a su referencia. Las muestras no son exactamente iguales, porque usar el trimestre anterior exige que exista.”

10. Conclusiones · 45 segundos

“En productividad, dentro de una misma empresa, más inversión se asocia con más productividad. Pero ese tamaño baja cuando controlamos por adopción y cambia mucho con pocos casos extremos.

En empleo, más adopción se asocia con más creación y más automatización con más desplazamiento, siempre frente a neutral. Los datos no alcanzan para decir por qué.

Anticipar un trimestre es posible, pero se predice peor que con datos del mismo trimestre. Y como son datos sintéticos, los pasos siguientes son entender cómo se generaron, mirar en qué se usa la IA en cada empresa y probar estos patrones en datos reales. Gracias.”
