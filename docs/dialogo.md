# Guion general — IA, productividad y empleo

Versión del 12/11/2026, adaptada a la devolución de Caro y a las diapositivas observadas en el video. El audio del video no fue transcripto: este texto propone qué decir en la nueva exposición y no reproduce literalmente la grabación.

Las indicaciones y los títulos no se leen. El límite del video completo es de 15 minutos, confirmado por Sebastian. La grabación revisada dura 12:52 y entra en ese límite, con 2:08 de margen. Ensayar con cronómetro después de los cambios: el tiempo final depende de las pausas y del ritmo de cada integrante.

Sebastian presenta la introducción (diapositiva 1) y las diapositivas 2, 3, 4, 11 y 12. Las diapositivas 5 a 10 corresponden al resto del equipo.

## 1. Introducción

Buenas tardes. Somos Eric Sigwald, Gonzalo Marengo y Sebastian Rigo. Analizamos cómo se relaciona la incorporación de inteligencia artificial con la productividad y el empleo de las empresas.

Nos enfocamos en dos preguntas: si una mayor inversión en IA por empleado se asocia con una mayor mejora de productividad, y cómo se relacionan la adopción y la automatización con el balance de puestos creados y desplazados.

Buscamos asociaciones estadísticas; estos análisis no permiten afirmar causalidad.

## 2. Estructura de los datos

Antes de hablar de la limpieza, veamos qué información tenemos. La tabla principal contiene 150.025 registros de 10.025 empresas, con 43 variables y observaciones entre 2023 y 2026.

Cada fila representa una empresa en un trimestre. La misma empresa aparece en distintos períodos, lo que permite seguir sus cambios a lo largo del tiempo.

Agrupamos la información en cuatro ejes: contexto empresarial, como país, industria y tamaño; uso e inversión en IA, incluyendo adopción y automatización; gobernanza, como privacidad y gestión de riesgos; y resultados, como productividad y puestos creados o desplazados.

Además, hay identificadores, períodos y metadatos. Otros dos archivos aportan contexto por industria y por país. Para las preguntas que presentamos, la unidad de análisis sigue siendo la empresa en cada trimestre.

Con esta estructura clara, pasamos a los problemas que encontramos y cómo los tratamos.

## 3. Limpieza y muestra de análisis

Con esa estructura, revisamos la calidad de los datos antes de modelar.

En la limpieza recuperamos 2.250 datos de industria y otros tantos de tamaño usando información consistente de la misma empresa. Excluimos 2.253 filas por adopción faltante o categorías irrecuperables, y otras 301 por adopción fuera de rango.

En otras variables, los valores imposibles o aislados se trataron en la celda. Para modelar usamos las mediciones observadas y aprendimos los valores de relleno únicamente con entrenamiento, como explicamos a continuación. No encontramos duplicados de empresa y trimestre.

Quedaron 147.471 registros de 10.019 empresas. El número utilizado después depende de qué datos necesita cada análisis.

## 4. Entrenamiento, validación y prueba

Usamos dos evaluaciones porque responden preguntas distintas.

Para evaluar empresas nuevas, reservamos el 20% de las empresas completas para prueba. En el 80% restante ajustamos los parámetros con validación cruzada de tres pliegues, también separados por empresa.

Para evaluar períodos futuros, entrenamos con 2023 y 2024, elegimos los parámetros con 2025 y probamos con 2026.

Las medianas se calculan solamente con entrenamiento. Esos valores también completan predictoras faltantes de validación y prueba, sin recalcularlos con esos conjuntos. Productividad y empleo no se imputan: si falta la respuesta, esa fila no participa de ese modelo.

## 5. Selección de rangos: cuartiles

Para esta comparación tomamos el segundo trimestre de 2026, con 9.231 empresas.

Las ordenamos por adopción y, por separado, por inversión por empleado. En cada caso formamos cuatro cuartiles, con aproximadamente el 25% de las empresas en cada uno. Son grupos por posición; sus intervalos numéricos pueden tener distinto ancho.

Las barras muestran qué porcentaje de cada cuartil supera el 20% de mejora de productividad. Por adopción, pasa de 0,13% a casi 15%; por inversión, de 2,2% a 7,5%.

El 20% es un umbral exploratorio para definir una mejora elevada. Este gráfico compara empresas distintas en un mismo trimestre.

## 6. H1: inversión y productividad dentro de cada empresa

Para seguir a cada empresa en el tiempo usamos TWFE: efectos fijos de empresa y de trimestre. Compara cada empresa consigo misma y descuenta cambios comunes de cada período, con errores estándar agrupados por empresa.

Usa 144.743 registros observados. Un aumento típico de inversión se asocia con 1,05 puntos de productividad. Al incluir adopción, baja a 0,24, mientras adopción se asocia con 2,34.

Al retirar 2.187 observaciones de leverage alto, el 1,5%, la asociación de inversión con adopción incluida sube de 0,24 a 1,32 puntos. El signo persiste, pero la magnitud es sensible. Este análisis explicativo no establece causalidad.

## 7. H1: estimar productividad en empresas nuevas

Para predecir productividad comparamos Ridge y boosting. Ajustamos sus parámetros por MAE con tres pliegues por empresa y evaluamos en el 20% de empresas reservado.

MAE es el error absoluto medio en puntos de productividad: menos es mejor. Predecir siempre el promedio de entrenamiento da 4,67. Ridge obtiene 3,36 y boosting, 3,34. Ambos mejoran la referencia; la diferencia entre ellos es pequeña.

## 8. H2: neutral y selección de la banda

En empleo distinguimos creación neta, desplazamiento neto y neutral, definido como empate exacto entre puestos creados y desplazados.

Ese empate aparece en el 41% de los registros de empresas de menos de 100 empleados y en menos del 1% de las de mil o más.

Probamos dos alternativas. Al quitar neutrales preguntamos: entre empresas con saldo distinto de cero, ¿cuáles crean y cuáles desplazan? El RF ampliado acierta 79%.

Con una banda de ±0,5% de la plantilla ampliamos la definición de neutral: pasa del 18% al 28%. Es una sensibilidad a un umbral alternativo. Conservamos el empate exacto como definición principal; las métricas de las alternativas no indican una mejora en la tarea original.

## 9. H2: adopción, automatización y empleo

Adopción representa cuánto incorpora o usa IA la empresa; automatización, cuánto de sus tareas pasa a realizarse automáticamente. Usar IA como asistencia puede aumentar adopción sin sustituir una tarea completa.

El logit multinomial compara creación y desplazamiento frente a neutral. Con diez puntos más de adopción, el cociente P(creación)/P(neutral) se multiplica por 2,20. Con diez puntos más de automatización, P(desplazamiento)/P(neutral) se multiplica por 4,94, manteniendo los demás predictores fijos.

El análisis de componentes también vincula creación con adopción y desplazamiento con automatización. La asistencia y la sustitución son mecanismos posibles, pero este trabajo no los demuestra.

## 10. H2: selección del clasificador

Los cuatro clasificadores usan la misma partición por empresa y los mismos tres pliegues internos. Elegimos configuraciones por macro-F1, que da igual peso a las tres clases.

Comparamos logit lineal, logit con curvas y dos Random Forest de 200 árboles. El RF base tiene profundidad máxima 18 y hojas de al menos 25 registros. En el ampliado fijamos profundidad 12 y probamos cuatro combinaciones: hojas de 5 o 25 registros, con pesos iguales o menor peso para neutral. Ganó hojas de 25, sin ponderación especial.

Tres modelos quedan muy próximos en validación cruzada. Elegimos el logit lineal por simplicidad. La tabla muestra test: acierta 7 de cada 10 y detecta peor neutral, con recall del 53%.

## 11. Anticipar el trimestre siguiente

Hasta acá vimos relaciones y predicciones con información del mismo trimestre. Ahora preguntamos si podemos anticipar la productividad y el balance de empleo del trimestre siguiente usando los datos del trimestre anterior.

Para respetar el orden temporal, entrenamos con 2023 y 2024, seleccionamos los parámetros con 2025 y dejamos 2026 para la prueba final.

En productividad usamos Ridge. El error absoluto medio pasa de 3,45 puntos con información del mismo trimestre a 4,32 al anticipar. Cuanto menor es este error, mejor. Todavía mejora la referencia de predecir siempre el promedio de entrenamiento, que tiene un error de 4,79.

En empleo usamos el logit lineal. El macro-F1, que da el mismo peso a las tres clases y mejora cuanto más alto es, baja de 0,68 a 0,53. Aun así, supera el 0,20 de la referencia de predecir siempre la clase más frecuente del entrenamiento.

Las muestras difieren porque para anticipar necesitamos contar con el trimestre anterior exacto. Por eso, la comparación no aísla solamente el efecto de anticipar. Evaluamos un trimestre por vez, suponiendo que ya conocemos el anterior; no pronosticamos todo 2026 de una sola vez.

Estos resultados muestran señal predictiva en esta evaluación, aunque con menor precisión al anticipar.

## 12. Conclusiones

Encontramos una asociación positiva entre inversión en IA y productividad dentro de cada empresa. Su magnitud disminuye al incluir adopción y es sensible a pocas observaciones extremas.

En empleo, adopción se asocia con creación neta y automatización con desplazamiento neto, frente a neutral. Esa diferencia no demuestra por sí sola cómo se usa la IA ni qué causa los cambios laborales.

Para anticipar un trimestre, ambos modelos superan sus referencias simples, aunque pierden precisión respecto de usar información del mismo período.

Como próximos pasos proponemos estudiar los usos concretos de IA y comprobar si estos patrones se mantienen en otras muestras y períodos. Muchas gracias.

## Coordinación con las diapositivas

- Diapositiva 3: agregar una síntesis temática de las variables; evitar que la introducción al dataset quede limitada a la limpieza. Distinguir la exportación descriptiva imputada de los datos observados usados para TP3.
- Diapositiva 4 del video: reemplazar el pie por «Las medianas se calculan solo con entrenamiento y se aplican a predictoras faltantes de validación y prueba. No se imputan las respuestas ni se utiliza información futura». El PPTX local ya contiene una formulación más correcta que la grabación.
- Diapositiva 6: presentar TWFE como una regresión con efectos fijos de empresa y de trimestre. Su revisión se apoya en diagnósticos y sensibilidad, no en elegirlo por validación cruzada predictiva.
- Diapositiva 7: recordar la validación por empresa al presentar Ridge y boosting.
- Diapositiva 8: cambiar «las alternativas responden otra pregunta» por «Excluir neutral restringe la población; la banda modifica la definición de neutral». Atribuir el 79% al RF ampliado.
- Diapositiva 9: definir adopción y automatización. Reemplazar «suben juntas, por eso sus efectos se compensan» por «Están correlacionadas y presentan asociaciones condicionales de signo opuesto». La correlación no demuestra compensación.
- Diapositiva 10: reemplazar «configuración estándar» por «configuración base fijada»; precisar la búsqueda del RF ampliado y rotular las métricas de la tabla como test por empresa. Recordar que la selección usa CV, no el puntaje de test. El criterio se fijó en la revisión, después de que el test ya se había consultado en entregas anteriores.
- Diapositiva 11: conservar la advertencia de muestras distintas y la disponibilidad secuencial del trimestre anterior.
- Diapositiva 12: mantener conclusiones de asociación y sensibilidad, sin afirmar causalidad ni generalizar a empresas reales.

## Alcance de la fuente

El proyecto local y las diapositivas de la grabación califican los datos como sintéticos. El origen y el generador deben acreditarse con una fuente antes de presentarlo como hecho verificado. El guion oral utiliza «registros» y no afirma que se trate de encuestas reales. Las limitaciones causales se justifican por el diseño del análisis.

No se modificaron los modelos ni sus resultados. La presentación v4 incorpora la diapositiva de estructura, adapta la introducción a la limpieza y renumera las posteriores. Los demás ajustes de diapositivas indicados arriba siguen pendientes.
