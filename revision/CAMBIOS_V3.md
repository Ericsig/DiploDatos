# Por qué la presentación cambió de la v2 a la v3

Les dejo qué cambié en `deck/IA_en_las_empresas_presentation_v3.pptx` y por qué. Hubo dos rondas: la primera respondió a la devolución del TP3 y la segunda, a las correcciones sobre la presentación. La idea en las dos fue que alguien que no hizo el trabajo entienda cada diapositiva.

**No volví a correr ningún modelo.** Todos los números salen de los CSV de `revision/resultados/`. `scripts/calcular_valores_presentacion.py` comprueba los 8 gráficos, las dos tablas de la diapositiva 9 y 24 cifras redondeadas que aparecen en frases. Falla si alguna deja de coincidir.

## Segunda ronda: correcciones sobre la presentación

Ahora son **11 diapositivas**: agregué la de los datos (2) y respeté el orden que armó Eric.

| # | Corrección | Qué hice |
|---|---|---|
| Estilo, 5 a 9 | La frase bajo el título era telegráfica (“Para explicar.”) y pegaba definiciones. | Cada diapositiva abre con la pregunta que responde, en una oración, y después dice con qué modelo. Las definiciones pasaron al pie o al guion. |
| 1 | Si mostramos dos hipótesis, son H1 y H2. | H3 pasó a llamarse **H2** en el deck y en el guion. El guion ya no dice “del primer práctico retomamos dos hipótesis”. |
| 2 (nueva) | Falta contar el tratamiento de los datos. | Tabla con qué encontramos, qué hicimos y cuántas filas se fueron: categorías recuperadas, 2.253 filas sin adopción, 301 con adopción fuera de rango, valores imposibles corregidos en la celda y cero duplicados. Cierra con **147.471 respuestas de 10.019 empresas**. |
| 2 y 3 | La numeración estaba cruzada. | Ahora va de 1/11 a 11/11. |
| 3 y 4 → 2 y 5 | No coinciden los N (150.025 contra 144.743). | La diapositiva 2 muestra cómo se pasa de 150.025 a 147.471. La del TWFE aclara que usa 144.743 de esas 147.471, las que tienen productividad, inversión e ingresos. |
| 4 | Llamar “cuartiles” a los grupos. | Subtítulo, categorías y eje dicen “cuartil” y aclaran que cada uno es el 25% de las empresas. |
| 5 | ¿Por qué uno está en puntos y el otro en pendiente? | **Los dos gráficos están ahora en la misma unidad:** puntos de productividad por un aumento típico de inversión. Multipliqué cada pendiente por el mismo desvío within de la muestra completa (0,82), así que las proporciones no cambian. La pendiente con adopción pasa de 0,29 a 1,60, que en puntos es de 0,24 a 1,32. |
| 6 | Poner el nombre de la métrica junto al valor. | El eje dice “MAE” y cada barra lleva su R² debajo. Saqué el panel aparte de R². |
| 7 | Cerrar lo que probaron con neutral o sacarlo. | Un recuadro dice qué pasó con cada alternativa: sin neutral el modelo acierta 79%, y con la banda de ±0,5% neutral pasa de 18% a 28% de los casos. También dice por qué nos quedamos con el empate exacto: las alternativas cambian la pregunta. |
| 8 | Nombrar los cocientes y explicar el RRR. | Las categorías son P(creación)/P(neutral) y P(desplazamiento)/P(neutral). **El gráfico muestra la RRR directamente, en escala logarítmica con 1 = sin cambio**, así que las barras son los mismos factores del texto (2,20 y 4,94). El pie da la relación con el coeficiente (e^0,79 = 2,20) y el guion define RRR. |
| 9 | Explicar las cuatro versiones en la diapositiva. | La tabla tiene una columna “Qué es” para cada modelo. |
| 9 | La validación cruzada no decide entre empatados. | **Cambió el modelo elegido: ahora es el logit lineal.** En validación cruzada, logit lineal, logit con curvas y RF ampliado quedan a menos de 0,002, por debajo del desvío entre pliegues (0,003). Ante el empate elegimos el más simple, que además es el mismo tipo de modelo que usamos para explicar. La matriz del RF pasó a ser una tabla de precisión y recall por clase del logit lineal. |
| 10 | Definir la referencia. | Cada leyenda dice cuál es (“siempre el promedio” y “siempre la clase más frecuente”), y el pie lo repite. |

### Ojo con esto

- **El notebook ya explica la elección del logit lineal.** Actualicé solo los textos de `notebook/modelado.ipynb` (secciones 1, 7 y 10), sin volver a correr celdas. La salida de la celda de la sección 7 sigue diciendo “Familia elegida por macro-F1 de CV: RF ampliado”, porque informa el mejor puntaje; el texto de arriba aclara que la elección final aplica el criterio de empate. En la sección 1 agregué que en la presentación H3 se expone como H2.
- **El 79% sin neutral es del RF ampliado.** Las etiquetas alternativas se reentrenaron con el modelo que estaba elegido en ese momento. Si nos preguntan, hay que decirlo.
- **El criterio de empate está escrito en el verificador:** gana el más simple entre los que quedan a menos de un desvío entre pliegues del mejor. Si cambian los resultados de validación cruzada, la verificación falla y avisa.

## Primera ronda: devolución del TP3

### Tres criterios que apliqué en todo el deck

1. **Todos los gráficos tienen ejes con nombre.** La v2 mostraba números sin decir qué medían.
2. **Cada resultado se lee como una frase.** La devolución pide escribirlos así (“acierta 7 de cada 10, frente a 4 de cada 10…”). El término técnico queda entre paréntesis o al pie, para quien corrige.
3. **Cada modelo dice si es para explicar o para predecir.** La devolución pide decir qué se modela, con qué y para qué antes de mostrar resultados.

### Lo más importante de esa ronda

- **Conclusiones:** la v2 decía “mediada vía control de adopción”, y no podemos afirmar mediación. También decía que la adopción se relaciona “directamente” con la creación, que suena causal.
- **Logit:** el mensaje dejó de ser “VIF máximo: 19,9”. El VIF quedó solo en el guion: sacar la categoría de tamaño casi no cambia el macro-F1 (0,673 contra 0,672), y sacar la cantidad de empleados lo baja a 0,646.
- **Métrica:** la devolución pidió contar macro-F1 como fijada de antemano. Pero las notas de la v2 aclaraban que el test ya se había consultado en el trabajo original. Si nos preguntan, hay que responder lo que pasó: en la revisión se fijó macro-F1 y se eligió por validación cruzada, después de un primer intento que sí había visto el test.

## El guion (`docs/dialogo.md`)

- Tiene 11 secciones, una por diapositiva, y está cargado en las notas de cada una junto con su fuente. El de la v2 quedó en `docs/dialogo_anterior.md`.
- Dura unos 9 minutos y 35 segundos a ritmo tranquilo (1.343 palabras a 140 por minuto). Si se pasan, lo primero que se puede recortar es el último párrafo de la sección 8.
- Dos cifras se calcularon fuera de los CSV y el verificador no las controla: r ≈ 0,7 entre adopción y automatización (todo `data/raw/company_limpio.csv`; la devolución menciona 0,66, probablemente sobre otro subconjunto) y “5 creados y 5 desplazados, o ninguno” (cerca del 10% de los empates son 0 y 0). Sí está controlada la r ≈ 0,7 que aparece en el pie de la diapositiva 8.

## Preguntas que nos pueden hacer

- **¿Por qué el gráfico derecho de H1 no muestra la pendiente?** Porque la pasamos a la misma unidad que el izquierdo. La pendiente con adopción va de 0,29 a 1,60 sin los casos de leverage alto, y en puntos es de 0,24 a 1,32.
- **¿Por qué el logit lineal, si el logit con curvas da 0,676 en el test?** Porque elegimos por validación cruzada, donde tres modelos empatan, y entre empatados elegimos el más simple. El test no se usa para elegir.
- **¿Qué ganaríamos con el RF ampliado?** En validación cruzada, 0,002 de macro-F1, que es menos de lo que varía el resultado entre pliegues. A cambio perdemos interpretación.
- **¿La inversión no sirve, entonces?** No se puede concluir eso: la asociación es positiva, pero parte se comparte con adopción y el tamaño depende de pocos casos.
- **¿Cómo se pasa del coeficiente a la RRR?** Elevando e al coeficiente: e^0,79 = 2,20. Una RRR de 2,20 significa que el cociente P(creación)/P(neutral) se multiplica por 2,2 con diez puntos más de adopción.
