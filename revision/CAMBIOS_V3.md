# Por qué la presentación cambió de la v2 a la v3

Les dejo qué cambié en `deck/IA_en_las_empresas_presentation_v3.pptx` y por qué. La idea fue responder lo que todavía faltaba de la devolución y hacer que alguien que no hizo el trabajo entienda cada gráfico.

**No cambió ningún resultado.** No volví a correr modelos. Comparé los valores de los 8 gráficos y los números de las tablas de la diapositiva 8 contra la v2, y son idénticos. Cambiaron los textos, los rótulos y los ejes.

## Tres criterios que apliqué en todo el deck

1. **Todos los gráficos tienen ejes con nombre.** La v2 mostraba números sin decir qué medían. Por ejemplo, la devolución ya pedía aclarar qué es “mejora”: ahora lo dice el eje.
2. **Cada resultado se lee como una frase.** La devolución pide escribirlos así (“acierta 7 de cada 10, frente a 4 de cada 10…”). El término técnico queda entre paréntesis o al pie, para quien corrige.
3. **Cada modelo arranca diciendo “para explicar” o “para predecir”.** La devolución pide decir qué se modela, con qué y para qué antes de mostrar resultados.

## Cambios por diapositiva

| # | Qué cambió | Por qué |
|---|---|---|
| 1 | Las hipótesis pasaron a ser preguntas. El pie aclara que son datos simulados y asociaciones. | “El público tiene que saber qué se está poniendo a prueba antes de ver los datos.” |
| 2 | El subtítulo dice la conclusión (casi 15% contra 0,13%, y 7,5% contra 2,2%). “Q1…Q4” pasó a “Grupo 1 (25% más bajo)…”. | “Un número solo no dice nada.” Hay que entender los cuartiles sin saber qué es un cuartil. |
| 3 | La tabla se lee como preguntas (“¿Sirve en empresas que nunca vio?”). Salieron “GroupKFold”, “X de t−1” y “train”. | Es una diapositiva de contexto. La devolución sobre curación se responde mostrando los 2.250 + 2.250 datos recuperados. |
| 4 | Se aclara qué explica TWFE. “1 desvío within” pasó a “aumento típico”. El mensaje dice que sacar 2.187 filas (1,5%) mueve la pendiente de 0,29 a 1,60. | Responde a la devolución sobre leverage y sobre comparar con un desvío. El pie avisa que los dos gráficos usan escalas distintas, porque alguien podría preguntar por qué 0,24 y 0,29 no coinciden. |
| 5 | Se explica Ridge y boosting en una frase. “Media train” pasó a “Siempre el promedio (referencia)”. R² pasó a “variación que explican”. | Es el ejemplo que da la devolución: “explica el 43%… y uno más complejo no mejora”. |
| 6 | Las tres clases se definen en palabras, con el ejemplo “2 y 2”. Las alternativas quedan en una línea. | “Neutral” tiene que estar definido antes de usarse. Responde a la devolución sobre el empate y la banda de ±0,5%. |
| 7 | **El mensaje pasó de “VIF máximo: 19,9” a “la chance se multiplica por 2,2 y por 4,9”.** El pie explica que adopción y automatización suben juntas. | Un log(RRR) no se puede leer al vuelo. Y la devolución marca que “acompaña / reemplaza” es una lectura de los nombres de las variables, no algo que los datos prueben. |
| 8 | Se explica F1 en una frase. La fila elegida va en negrita. El mensaje usa “7 de cada 10 contra 4 de cada 10”. | La devolución pidió mostrar la métrica en tabla y contarla como fijada de antemano. |
| 9 | Los títulos dicen si conviene más o menos. “t−1 exacto” pasó a “Trimestre anterior”. Junté dos líneas en una sola conclusión. | Responde a “¿qué significa predecir?”. Los dos gráficos van en sentido contrario, y eso se presta a confusión. |
| 10 | Reescribí H1 y H3 y agregué una línea sobre anticipación. | **Es la corrección de fondo más importante:** la v2 decía “mediada vía control de adopción”, y no podemos afirmar mediación. También decía que la adopción se relaciona “directamente” con la creación, que suena causal. |

## El guion (`docs/dialogo.md`)

- Lo reescribí con frases más cortas y explico cada término la primera vez que aparece. El anterior quedó en `docs/dialogo_anterior.md`.
- Dura unos 9 minutos y 45 segundos a ritmo tranquilo (1.345 palabras a 140 por minuto), así que está justo para los 10 minutos. Si se pasan, lo primero que se puede recortar es el último párrafo de la sección 7.
- Agregué 2,34 puntos de adopción en H1, que el guion anterior no mencionaba y el gráfico sí.
- También está cargado en las notas de cada diapositiva de la v3, junto con su fuente.

## Lo que conviene que revisemos juntos

1. **“Fijamos la métrica de antemano.”** La diapositiva 8 y el guion lo dicen porque la devolución pidió contarlo así. Pero las notas de la v2 aclaraban que el test ya se había consultado en el trabajo original. Por eso saqué del guion la frase “la elección se hizo antes de mirar ese test”. Si nos preguntan, hay que responder lo que pasó: en la revisión se fijó macro-F1 y se eligió por validación cruzada, después de un primer intento que sí había visto el test.
2. **Hay cifras nuevas que no estaban en la v2.** Las que salen de archivos del repo quedaron en `revision/VALORES_PRESENTACION.md`, salvo los datos de empates, que se calcularon aparte.
   - Multiplicadores 2,2 y 4,9: columna RRR de `h3_contrastes.csv`.
   - r ≈ 0,7 entre adopción y automatización: todo `data/raw/company_limpio.csv` da 0,70. La devolución menciona 0,66, probablemente sobre otro subconjunto.
   - “La mitad de los empates son de dos puestos o menos” y “también puede ser ninguno”: sobre `data/ai_company_adoption.csv`, la mediana de los empates es 2 y cerca del 10% son 0 y 0.
3. **El VIF salió de la diapositiva 7 y quedó solo en el guion**, sin el número. Si prefieren mostrarlo, entra en el pie. El resultado es que sacar la categoría de tamaño casi no cambia el macro-F1 (0,673 contra 0,672). En cambio, sacar la cantidad de empleados lo baja a 0,646.
4. **Los resultados de las etiquetas alternativas no están en el deck.** Sin neutral da 0,786 de macro-F1 y con banda 0,615, y no son comparables entre sí. Conviene tenerlos a mano para las preguntas.
5. **La v3 quedó como entrega en toda la documentación.** `scripts/calcular_valores_presentacion.py` ahora la verifica con sus rótulos nuevos, y también chequea las cifras redondeadas de las frases. El cambio de rótulos implica que el script ya no sirve para verificar la v2. `deck/Valores_diapositiva.md` es una copia de `revision/VALORES_PRESENTACION.md`, y hay que volver a copiarla si se regenera.

## Preguntas que nos pueden hacer

- **¿Por qué 0,24 a la izquierda y 0,29 a la derecha?** Son el mismo modelo en dos escalas: la izquierda es el efecto de un aumento típico, y la derecha la pendiente.
- **¿Por qué elegir RF si el logit con curvas da 0,676?** Porque elegimos por validación cruzada, no por el test, y la diferencia es de menos de una milésima.
- **¿Por qué no hay H2?** Porque esta entrega retoma solo H1 y H3.
- **¿La inversión no sirve, entonces?** No se puede concluir eso: la asociación es positiva, pero parte se comparte con adopción y el tamaño depende de pocos casos.
