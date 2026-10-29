import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath,pathToFileURL } from 'node:url';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const workspaceDir=path.resolve(process.env.DIPLO_WORKSPACE ?? ROOT);
const BUILD=path.resolve(process.env.DIPLO_BUILD ?? path.join(ROOT,'revision','build'));
const OUT=path.resolve(process.env.DIPLO_OUTPUT ?? path.join(ROOT,'deck'));
const SKILL=process.env.DIPLO_PRESENTATION_SKILL;
const PYTHON=process.env.DIPLO_RUNTIME_PYTHON;
const {Presentation,PresentationFile}=await import(process.env.DIPLO_ARTIFACT_MODULE ?? '@oai/artifact-tool');
if(!SKILL||!PYTHON)throw Error('Definir DIPLO_PRESENTATION_SKILL y DIPLO_RUNTIME_PYTHON para validar las presentaciones');
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
await fs.mkdir(BUILD,{recursive:true});await fs.mkdir(OUT,{recursive:true});
const R=path.join(ROOT,'revision/resultados');
const C=JSON.parse(await fs.readFile(path.join(R,'curacion_resumen.json'),'utf8'));
const BG='#F2F2F3',INK='#1D1F20',BLUE='#5980A6',MUTED='#525D66',WHITE='#FFFFFF';
const FONT='Arial',W=1920,H=1080;
const fmt=(x,n=2)=>Number(x).toLocaleString('es-AR',{minimumFractionDigits:n,maximumFractionDigits:n});
const integer=x=>Number(x).toLocaleString('es-AR');
function text(s,str,x,y,w,h,size=40,bold=false,color=INK){
 const t=s.shapes.add({geometry:'textbox',name:str.slice(0,60),position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 t.text=str;t.text.style={typeface:FONT,fontSize:size,bold,color};return t;
}
function slide(p,title,number,total,source,time,notes=''){
 const s=p.slides.add();s.background.fill=BG;
 text(s,title,96,74,1728,125,64,true);
 text(s,`${number}/${total}`,1740,994,85,35,25,false,MUTED);
 s.speakerNotes.text=`Tiempo sugerido: ${time} segundos.\n${notes}\nFuente: ${source}.\nProyecto: DiploDatos. Resultados sintéticos y asociaciones sin identificación causal.`;
 return s;
}
function caption(s,str,y=917){text(s,str,96,y,1630,72,28,false,MUTED);}
function table(s,values,{top=280,height=500,width=1728,left=96,widths,size=34}={}){
 const t=s.tables.add({rows:values.length,columns:values[0].length,left,top,width,height,values,
  columnWidths:widths??Array(values[0].length).fill(width/values[0].length)});
 for(let i=0;i<values.length;i++){
  t.rows[i].height=height/values.length;
  for(let j=0;j<values[0].length;j++){
   const c=t.getCell(i,j);c.fill=i===0?BLUE:(i%2===0?'#E6EBEF':WHITE);
   c.text.style={typeface:FONT,fontSize:size,color:i===0?WHITE:INK,bold:i===0};
  }
 }
 t.borders.assign({fill:BG,width:2,style:'solid'});
 return t;
}
function parseCSV(s){
 const rows=[];let row=[],word='',quote=false;
 for(let i=0;i<s.length;i++){const ch=s[i];if(ch==='"'){if(quote&&s[i+1]==='"'){word+='"';i++;}else quote=!quote;}
 else if(ch===','&&!quote){row.push(word);word='';}
 else if(ch==='\n'&&!quote){row.push(word.replace(/\r$/,''));rows.push(row);row=[];word='';}
 else word+=ch;}
 if(word.length||row.length){row.push(word);rows.push(row);}
 const header=rows.shift();return rows.filter(r=>r.length===header.length).map(r=>Object.fromEntries(header.map((h,i)=>[h,r[i]])));
}
const csv=async name=>parseCSV(await fs.readFile(path.join(R,name+'.csv'),'utf8'));

function barChart(s,categories,series,{left=96,top=365,width=1728,height=490,max,min=0,format='0.00',direction='column',legend=true,labelPosition='outEnd',labelColor=MUTED}={}){
 const c=s.charts.add('bar',{position:{left,top,width,height},categories,
  series:series.map((r,i)=>({name:r.name,values:r.values.map(v=>Math.round(Number(v)*1e10)/1e10),fill:r.fill??[BLUE,'#D98B39','#368579'][i]})),
  barOptions:{direction,grouping:'clustered',gapWidth:95},hasLegend:legend,
  legend:{position:'bottom',overlay:false,textStyle:{fontSize:27}},
  xAxis:{tickLabelPosition:'low',textStyle:{fontSize:27}},yAxis:{min,max,numberFormatCode:format,textStyle:{fontSize:25},majorGridlines:{fill:'#D3DAE0',width:1}},
  dataLabels:{showValue:true,position:labelPosition,numberFormatCode:format,textStyle:{fontSize:26,fill:labelColor}},chartFill:BG,plotAreaFill:BG});
 applyPresentationChartFont(c,{fontFamily:FONT});return c;
}

async function finish(p,name,count,nativeTables,nativeCharts=[]){
 const privateDir=path.join(BUILD,name);await fs.mkdir(privateDir,{recursive:true});
 const candidatePath=path.join(privateDir,'candidate.pptx');
 await (await PresentationFile.exportPptx(p)).save(candidatePath);
 const finalPath=path.join(OUT,name+'.pptx');
 const result=await finalizePresentation({workspaceDir,candidatePath,finalPath,pythonExecutable:PYTHON,
  integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','18288000,10287000','--validate-heading-fit',...nativeTables.flatMap(n=>['--require-native-table-slide',String(n)])],
  explicitTotalSlideCount:count,requiredNativeTableOwnerSlides:nativeTables,requiredNativeChartOwnerSlides:nativeCharts,
  fontPolicy:{basis:'design',families:[FONT]},verifyArtifactToolImport:true,
  materializeLiteralChartWorkbooks:true,receiptPath:path.join(privateDir,'validation.json')});
 for(let i=0;i<p.slides.items.length;i++){
  const blob=await p.export({slide:p.slides.items[i],format:'png',scale:.7});
  await fs.writeFile(path.join(privateDir,`slide-${i+1}.png`),new Uint8Array(await blob.arrayBuffer()));
 }
 await fs.writeFile(path.join(privateDir,'layout.json'),JSON.stringify(p.toProto(),null,2));
 console.log('TERMINADO',name,finalPath,JSON.stringify(result).slice(0,300));
}

async function tp2(){
 const p=Presentation.create({slideSize:{width:W,height:H}});let s;
 s=slide(p,'IA en las empresas',1,8,'README.md y EDA',30,'Presentar al equipo y el propósito. Esta entrega resume curación y recupera el contexto de TP1.');
 text(s,'TP2 · Datos y curación',96,240,1728,90,52,true,BLUE);
 text(s,'¿Qué datos permiten estudiar productividad y empleo?',96,400,1728,155,58,true);
 text(s,'Eric Sigwald\nGonzalo Marengo\nSebastian Rigo',96,675,1500,190,38);
 caption(s,'Diplomatura en Ciencia de Datos · Octubre de 2026');

 s=slide(p,'Pregunta e hipótesis del proyecto',2,8,'eda_notebook.ipynb, hipótesis TP1',65,'H1 y H3 son las dos hipótesis priorizadas. Plantearlas antes de mostrar datos. El saldo de empleo no mide por sí mismo la transformación de tareas.');
 text(s,'H1 · Inversión y productividad',96,255,1728,70,46,true,BLUE);
 text(s,'¿Más inversión por empleado se asocia con mayor mejora de productividad, controlando industria y tamaño?',96,340,1728,160,44);
 text(s,'H3 · Adopción y balance de empleo',96,575,1728,70,46,true,BLUE);
 text(s,'¿La adopción y la automatización se asocian con creación o desplazamiento neto de puestos?',96,660,1728,150,44);
 caption(s,'Trabajamos asociaciones en datos sintéticos. El saldo de puestos no prueba transformación de tareas.');

 s=slide(p,'Dataset y unidad de análisis',3,8,'data/raw/*.csv; curacion_resumen.json',65,'Cada fila es una respuesta de una empresa en un trimestre. Advertir que el CSV contiene 2026 Q4 y no representa observaciones reales disponibles al día de hoy. La tabla industry contiene promedios del propio panel.');
 table(s,[['Fuente','Contenido','Rol'],['company',`${integer(C.filas_crudas)} respuestas · ${C.columnas_crudas} variables`,'Empresa y trimestre'],['country','30 países','Contexto del país'],['industry','9 industrias','Agregados del propio panel']],{height:460,widths:[350,790,588],size:38});
 text(s,`${integer(C.empresas_crudas)} identificadores de empresa · 16 trimestres`,96,815,1728,70,42,true,BLUE);
 caption(s,'Cobertura del archivo: 2023 Q1 a 2026 Q4. Panel sintético, incompleto y con errores de calidad.');

 s=slide(p,'Faltantes: recuperar antes de eliminar',4,8,'curacion.ipynb, secciones 4 y 10',95,'La recuperación usa otra respuesta de la misma empresa únicamente cuando los valores observados coinciden. En este panel no hay cambios de industria ni tamaño. En un panel real se debe respetar la fecha del cambio. Esta recuperación es retrospectiva y la validación futura se prepara aparte.');
 table(s,[['Variable','Decisión','Resultado'],['Industria','Recuperar de la misma empresa',`${integer(C.recuperacion[0].recuperadas)} recuperadas`],['Tamaño','Verificar estabilidad y recuperar',`${integer(C.recuperacion[1].recuperadas)} recuperadas`],['Respuesta objetivo','Conservar observada o excluir de su modelo','Nunca imputar'],['Predictoras numéricas','Mediana industria × tamaño','Respaldo global'],['Ética y privacidad','Moda del estrato + indicador','Preservar ausencia']],{height:590,widths:[390,870,468],size:34});
 caption(s,`Quedan ${C.recuperacion[0].sin_resolver} registros sin industria y ${C.recuperacion[1].sin_resolver} sin tamaño. TP3 aprende las imputaciones dentro de entrenamiento.`);

 s=slide(p,'Outliers y caso testigo: ingresos anuales',5,8,'curacion.ipynb, secciones 5.1–5.6; caso_testigo',110,'Comparar franjas de LA MISMA variable antes de tratarla, en millones de USD. La facturación no es beneficio neto. El hueco y la separación son indicios de anomalía, no una prueba general de que todos los extremos sean errores. La comparación por tamaño del notebook es una composición observada frente a la composición proporcional, no ingresos frente a pérdidas.');
 text(s,'Imposibles: tratar. Grupos aislados: revisar. Colas continuas: conservar.',96,228,1728,100,38,true,BLUE);
 const bands=C.caso_testigo;
 table(s,[['Ingresos anuales (millones USD)','Casos antes del tratamiento','Lectura'],
 ['Menos de −13.000',integer(bands[0].n),'Grupo negativo'],['−13.000 a 0',integer(bands[1].n),'Intervalo vacío'],
 ['0 a 10.000',integer(bands[2].n),'Cuerpo central'],['10.000 a 13.221',integer(bands[3].n),'Intervalo vacío'],
 ['Más de 13.221',integer(bands[4].n),'Grupo positivo aislado']],{top:360,height:480,widths:[740,510,478],size:32});
 caption(s,'Se comparan rangos de una misma medición. Una magnitud grande, por sí sola, no demuestra error.');

 s=slide(p,'Redundancia: cuatro decisiones distintas',6,8,'curacion.ipynb, sección 8',90,'Distinguir escala, contexto país, proximidad al target y composición de un índice. Correlación no demuestra fuga ni garantiza que eliminar una variable sea correcto. La decisión depende de la respuesta que se modela.');
 table(s,[['Familia','Qué se compara','Tratamiento'],['Escala de empresa','Empleados y conteos de puestos','Conservar resultados y calcular tasas'],['Desarrollo del país','PBI e índices de desarrollo','Reducir o revisar colinealidad'],['Cercanía a adopción','Adopción, etapa y madurez','Evitar etapa/madurez al predecir adopción'],['Índice compuesto','Madurez y sus posibles componentes','Verificar construcción y redundancia']],{height:580,widths:[430,660,638],size:34});
 caption(s,'Las correlaciones orientan el diagnóstico. El significado y la disponibilidad deciden qué variables usar.');

 s=slide(p,'Tamaño, tiempo y asimetría',7,8,'curacion.ipynb, secciones 6 y 9',80,'El orden empírico existe en este dataset, no se infiere del nombre Startup. La codificación nominal evita imponer distancias. El log reduce asimetría absoluta pero inversión sigue muy asimétrica y cambia de signo; no decir que normaliza.');
 text(s,'Tamaño nominal, con evidencia empírica',96,235,1728,70,42,true,BLUE);
 const sizes=['Startup','SME','Enterprise'].map(k=>C.tamano.find(r=>r.company_size===k));
 table(s,[['Categoría','Rango observado de empleados'],...sizes.map(r=>[r.company_size,`${integer(r.min)} a ${integer(r.max)}`])],{top:325,height:300,widths:[650,1078],size:34});
 text(s,'Tiempo continuo: 2023 Q4 = 3 · 2024 Q1 = 4',96,670,1728,70,40,true);
 text(s,`Skew de ingresos: ${fmt(C.skew[0].skew_antes)} a ${fmt(C.skew[0].skew_despues_log1p)} con log1p`,96,770,1728,65,38);
 text(s,`Skew de inversión: ${fmt(C.skew[1].skew_antes)} a ${fmt(C.skew[1].skew_despues_log1p)}. Persiste asimetría.`,96,845,1728,65,38);
 caption(s,'El skew compara forma. Las medias en dólares y en log-dólares no son comparables.',947);

 s=slide(p,'Datos preparados para H1 y H3',8,8,'curacion_resumen.json; modelado.ipynb',65,'Concluir con la entrega reproducible y las decisiones que condicionan los modelos. No presentar resultados de TP3 como si fueran parte de curación. Las asociaciones y los modelos futuros requieren respetar el panel y el momento de disponibilidad.');
 text(s,`${integer(C.panel_observado[0])} respuestas en el panel observado`,96,265,1728,100,56,true,BLUE);
 text(s,'Respuestas válidas conservadas. Faltantes predictivos disponibles para imputar dentro de cada entrenamiento.',96,390,1728,135,42);
 text(s,'H1: comparar inversión con y sin adopción como control',96,600,1728,80,42,true);
 text(s,'H3: definir neutral y evaluar precisión/recall por clase',96,715,1728,80,42,true);
 caption(s,'Separar empresas evalúa empresas nuevas. Para anticipar se necesitan fecha de corte y rezagos calendario.');
 await finish(p,'TP2_reentrega_final',8,[3,4,5,6,7]);
}

async function tp3(){
 const [twfe,sens,pred,neutral,components,auc,contrasts,vif,performance,models,cv,temp,quart]=await Promise.all(
  ['h1_twfe','h1_sensibilidad','h1_prediccion','h3_neutral','h3_componentes','h3_auc_componentes','h3_contrastes','h3_vif','h3_colinealidad_performance','h3_modelos','h3_modelos_cv','validacion_temporal','eda_cuartiles'].map(csv));
 const p=Presentation.create({slideSize:{width:W,height:H}});let s;
 const t=twfe.find(r=>r.especificacion==='Con adopción'&&r.variable==='adopcion');
 const invNo=twfe.find(r=>r.especificacion==='Sin adopción'&&r.variable==='log_inversion');
 const invYes=twfe.find(r=>r.especificacion==='Con adopción'&&r.variable==='log_inversion');
 s=slide(p,'IA, productividad y empleo',1,10,'README.md; hipótesis TP1',35,'Presentar pregunta e hipótesis juntas antes de los datos. El alcance se limita a H1 y H3.');
 text(s,'¿Cómo se relaciona el uso de IA con los resultados de las empresas?',96,230,1728,155,54,true,BLUE);
 text(s,'H1 · Inversión por empleado y cambio de productividad',96,445,1728,90,42,true);
 text(s,'H3 · Adopción, automatización y balance de puestos',96,575,1728,90,42,true);
 text(s,'Eric Sigwald · Gonzalo Marengo · Sebastian Rigo',96,800,1728,70,36);
 caption(s,'Panel sintético. Asociaciones contemporáneas y evaluación de anticipación a un trimestre.');

 s=slide(p,'Productividad: adopción e inversión en contexto',2,10,'eda_cuartiles.csv; data/raw/company_limpio.csv',50,'Corte fijo 2026 Q2 y muestra común completa. El resultado es superar 20% de mejora de productividad. Mostrar los cuatro cuartiles de adopción y de inversión, sin comparar muestras distintas. No extrapolar a causalidad.');
 text(s,`${integer(C.filas_crudas)} respuestas · ${integer(C.empresas_crudas)} empresas · 16 trimestres`,96,223,1728,70,38);
 const chart=s.charts.add('bar',{position:{left:96,top:325,width:1728,height:550},categories:['Q1 bajo','Q2','Q3','Q4 alto'],
  series:[['ai_adoption_rate','Adopción',BLUE],['ai_investment_per_employee','Inversión','#A3B6C7']].map(([v,name,color])=>({name,values:quart.filter(r=>r.variable===v).map(r=>Math.round(Number(r.pct_productividad_mayor_20)*1e8)/1e10),fill:color})),
  barOptions:{direction:'column',grouping:'clustered',gapWidth:100},hasLegend:true,legend:{position:'bottom',overlay:false,textStyle:{typeface:FONT,fontSize:30}},
  xAxis:{textStyle:{typeface:FONT,fontSize:30}},yAxis:{min:0,max:.18,majorUnit:.06,numberFormatCode:'0%',textStyle:{typeface:FONT,fontSize:28},majorGridlines:{fill:'#D3DAE0',width:1}},
  dataLabels:{showValue:true,position:'outEnd',numberFormatCode:'0.00%',textStyle:{typeface:FONT,fontSize:26}},chartFill:BG,plotAreaFill:BG});
 applyPresentationChartFont(chart,{fontFamily:FONT});
 caption(s,`Porcentaje de empresas con mejora de productividad >20%. Corte 2026 Q2, n=${integer(quart.filter(r=>r.variable==='ai_adoption_rate').reduce((sum,r)=>sum+Number(r.n),0))}, misma muestra.`);

 s=slide(p,'Curación y evaluación según la pregunta',3,10,'curacion_resumen.json; modelado.ipynb, preparación',45,'Dar el contexto mínimo del panel y la prevención de fuga. Separar qué se evalúa en empresa nueva y en futuro. Los targets no se imputan. Cada mediana y cada escala se aprende con train.');
 text(s,'2.250 datos de industria y 2.250 de tamaño recuperados de otras respuestas',96,230,1728,100,42,true,BLUE);
 table(s,[['Pregunta de evaluación','Partición','Información utilizada'],['Empresa nueva','80/20 por empresa + GroupKFold','Variables del mismo trimestre'],['Período posterior','Train 2023–24 · validar 2025 · test 2026','X del trimestre o X de t−1'],['Respuestas faltantes','Excluir del modelo correspondiente','No fabricar productividad o empleo']],{top:380,height:420,widths:[500,710,518],size:33});
 caption(s,'Medianas, categorías y escalas se aprenden dentro de train. La evaluación temporal recupera categorías solo hacia adelante.');

 s=slide(p,'H1: inversión con y sin controlar adopción',4,10,'h1_twfe.csv; h1_sensibilidad.csv',90,'TWFE compara una empresa consigo misma y descuenta shocks comunes. Respuesta: cambio porcentual de productividad. Predictores identificados: log1p inversión, opcional adopción. Ingresos, industria y tamaño constantes quedan absorbidos. La muestra es idéntica para los dos modelos. Los errores son agrupados por empresa. No interpretar la diferencia como mediación causal demostrada.');
 text(s,'TWFE explica el cambio de productividad comparando cada empresa consigo misma',96,220,1728,110,38);
 text(s,'Cambios por 1 desvío within (pp)',96,345,800,65,35,true,BLUE);
 barChart(s,['Inversión\nsin adopción','Inversión\ncon adopción','Adopción\ncon inversión'],[{name:'Cambio de productividad',values:[invNo.cambio_por_sd_within,invYes.cambio_por_sd_within,t.cambio_por_sd_within]}],{left:96,top:425,width:800,height:365,max:2.8,legend:false});
 text(s,'Pendiente de inversión y observaciones influyentes',995,345,829,80,32,true,BLUE);
 const samples=['Completa','Sin leverage alto','Sin residuos |z|>3.5'];
 barChart(s,['Completa','Sin leverage\nalto','Sin residuos\nextremos'],['Sin adopción','Con adopción'].map(name=>({name,values:samples.map(m=>sens.find(r=>r.especificacion===name&&r.muestra===m&&r.variable==='log_inversion').beta)})),{left:995,top:425,width:829,height:365,max:5});
 const cut=sens.find(r=>r.muestra==='Sin leverage alto'&&r.especificacion==='Con adopción'&&r.variable==='log_inversion');
 text(s,`Sensibilidad: β de inversión pasa de ${fmt(invYes.beta,3)} a ${fmt(cut.beta,3)} al retirar leverage alto`,96,800,1728,115,38,true,BLUE);
 caption(s,`Misma muestra base: n=${integer(invNo.n)}. Una asociación positiva con magnitud sensible a observaciones influyentes.`,935);

 s=slide(p,'H1: la complejidad mejora poco el error',5,10,'h1_prediccion.csv; h1_prediccion_cv.csv',45,'Antes de mostrar métricas: respuesta cambio porcentual de productividad. Ridge regulariza pendientes; boosting combina árboles para curvas e interacciones. Ambos usan la misma información. Se elige por MAE de CV por empresa. R² de test no es el R² dentro de empresa de TWFE.');
 text(s,'Ridge regulariza pendientes. Boosting combina árboles. Ambos estiman productividad con datos del mismo trimestre.',96,225,1728,130,38);
 text(s,'MAE de test, en puntos de productividad',96,365,1050,65,36,true,BLUE);
 const predTest=pred.filter(r=>r.conjunto==='test');
 barChart(s,predTest.map(r=>r.modelo),[{name:'MAE en empresas nuevas',values:predTest.map(r=>r.MAE)}],{left:96,top:445,width:1050,height:395,max:5.5,legend:false});
 text(s,'R² en test',1230,410,560,80,43,true,BLUE);
 text(s,`Ridge: ${fmt(predTest.find(r=>r.modelo==='Ridge').R2,3)}\nBoosting: ${fmt(predTest.find(r=>r.modelo==='Gradient boosting').R2,3)}`,1230,530,560,170,44);
 text(s,'Las diferencias son pequeñas en estas configuraciones',1230,745,560,130,34);
 caption(s,'Selección por MAE de validación agrupada. El desempeño mide estimación contemporánea en empresas nuevas.');

 s=slide(p,'H3: qué significa neutral',6,10,'h3_neutral.csv; h3_componentes.csv; h3_etiquetas.csv',55,'Definir las tres clases antes de hablar de logit y RF. Neutral es un empate exacto, no ausencia de cambios. Las clases alternativas se ejecutan aparte y sus F1 no son comparables directamente.');
 text(s,'Creación: creados > desplazados. Desplazamiento: creados < desplazados. Neutral: empate exacto.',96,225,1728,145,40);
 text(s,'Frecuencia de neutral según dotación',96,390,1090,65,36,true,BLUE);
 barChart(s,neutral.map(r=>r.grupo_dotacion+' empleados'),[{name:'Observaciones neutrales',values:neutral.map(r=>Number(r.neutral_pct)/100),fill:'#D98B39'}],{left:96,top:475,width:1090,height:310,max:.5,format:'0.0%',legend:false});
 text(s,'Un saldo cero puede incluir creación y desplazamiento a la vez',1280,470,510,210,42,true);
 text(s,'Alternativas evaluadas: excluir neutral o usar una banda de ±0,5% de la plantilla',96,815,1728,100,38,true,BLUE);
 caption(s,'El empate de conteos pequeños depende de la resolución de medición. Un saldo cero puede incluir creación y desplazamiento.');

 s=slide(p,'H3: asociaciones del logit y sus componentes',7,10,'h3_contrastes.csv; h3_componentes.csv; h3_vif.csv; h3_colinealidad_performance.csv',60,'Logit multinomial sobre tres clases, con neutral como referencia. Coeficientes de adopción y automatización por +10 puntos. Modelo para asociaciones con errores agrupados, no panel within. La tasa de creación se relaciona con adopción y la de desplazamiento con automatización, y su resta produce el saldo. No atribuir el resultado a casos de uso sin observarlos.');
 text(s,'Logit multinomial: compara creación y desplazamiento con neutral, ajustando por características de la empresa y tiempo',96,222,1728,125,37);
 const con=contrasts.filter(r=>r.especificacion==='Completo'&&['ai_adoption_rate','task_automation_rate'].includes(r.variable));
 const rrr=(v,c)=>fmt(con.find(r=>r.variable===v&&r.contraste.startsWith(c)).RRR,2)+'×';
 barChart(s,['Creación / neutral','Desplazamiento / neutral'],[
  {name:'Adopción (+10 puntos)',values:['net_creation','net_displacement'].map(c=>con.find(r=>r.variable==='ai_adoption_rate'&&r.contraste.startsWith(c)).coef),fill:'#368579'},
  {name:'Automatización (+10 puntos)',values:['net_creation','net_displacement'].map(c=>con.find(r=>r.variable==='task_automation_rate'&&r.contraste.startsWith(c)).coef),fill:'#B75C66'}],{top:400,height:320,min:-2,max:2,format:'0.00',labelPosition:'center',labelColor:WHITE});
 const vifFull=vif.filter(r=>r.especificacion==='Completo').reduce((a,b)=>Number(a.VIF)>Number(b.VIF)?a:b);
 text(s,`VIF máximo: ${fmt(vifFull.VIF,1)}. Se probó retirar empleados o tamaño y comparar errores y desempeño.`,96,750,1728,110,36,true,BLUE);
 caption(s,'Eje vertical: coeficiente log(RRR). Cero equivale a RRR=1. Los signos no identifican un mecanismo causal.');

 s=slide(p,'H3: elección por macro-F1 de las tres clases',8,10,'h3_modelos.csv; h3_modelos_cv.csv; h3_bootstrap_empresas.csv',90,'Presentar RF como combinación de árboles y logit como clasificación por probabilidades de las tres clases. Se fija macro-F1 antes de esta revisión, aunque test ya había sido consultado en el trabajo original. La selección usa CV por empresa. F1 empleo es secundaria y promedia creación y desplazamiento. Precisiones y recalls completos están en el notebook.');
 text(s,'Logit estima probabilidades de las tres clases. Random Forest combina árboles. Ambos clasifican el saldo con los mismos ocho predictores.',96,220,1728,130,37);
 const rows=models.filter(r=>r.conjunto==='test'&&r.modelo!=='Mayoritaria');
 table(s,[['Modelo','Macro-F1','F1 creación','F1 desplaz.'],...rows.map(r=>[r.modelo,fmt(r.macro_F1,3),fmt(r['net_creation_f1-score'],3),fmt(r['net_displacement_f1-score'],3)])],{top:420,height:370,width:1060,widths:[370,230,230,230],size:30});
 const chosenMatrix=(await csv('h3_matrices')).filter(r=>r.modelo==='RF ampliado');
 const codes=['neutral','net_creation','net_displacement'];
 const fractions=codes.map(real=>{const n=chosenMatrix.filter(r=>r.real===real).reduce((sum,r)=>sum+Number(r.n),0);return codes.map(predicted=>Number(chosenMatrix.find(r=>r.real===real&&r.predicha===predicted).n)/n);});
 text(s,'RF ampliado: errores por clase',1210,365,614,55,32,true,BLUE);
 const matrix=table(s,[['Real / pred.','Neutral','Creación','Desplaz.'],...fractions.map((v,i)=>[['Neutral','Creación','Desplaz.'][i],...v.map(x=>fmt(x*100,1)+'%')])],{left:1210,top:445,width:614,height:330,widths:[170,148,148,148],size:25});
 for(let i=0;i<3;i++)for(let j=0;j<3;j++){const v=fractions[i][j];const c=matrix.getCell(i+1,j+1);c.fill=v>.55?'#5980A6':v>.2?'#B4C8D9':'#E5EDF3';c.text.style={typeface:FONT,fontSize:26,color:v>.55?WHITE:INK};}
 text(s,'Porcentajes por fila observada',1210,795,614,50,27,false,MUTED);
 const winner=cv.filter(r=>r.elegido_familia==='True').sort((a,b)=>Number(b.macro_F1_CV)-Number(a.macro_F1_CV))[0];
 const base=models.find(r=>r.conjunto==='test'&&r.modelo==='Mayoritaria');
 text(s,`Elegido por CV: ${winner.modelo}. Referencia mayoritaria: ${fmt(Number(base.accuracy)*100,1)}% de acierto.`,96,850,1728,90,36,true,BLUE);
 caption(s,'Se mantienen las tres clases en la métrica principal. No se cambia el criterio para favorecer otro modelo.',950);

 s=slide(p,'Evaluación temporal y anticipación a un trimestre',9,10,'validacion_temporal.csv; particiones_temporales.csv',90,'Entrenar 2023–24, seleccionar penalización en 2025 y test 2026, sin reajustar con test. La evaluación con X contemporánea no anticipa Y. Para anticipar usar X del trimestre exacto anterior. El join exige diferencia de un trimestre; si falta t−1 se excluye el par. Modelos Ridge H1 y logit H3. Esta muestra se reconstruye del crudo con reglas de dominio y difiere de la evaluación agrupada, sin búsqueda de bandas futuras.');
 text(s,'Train 2023–2024 · Validación 2025 · Test 2026',96,225,1728,75,42,true,BLUE);
 const temps=temp.filter(r=>r.conjunto==='test'&&r.modelo==='Modelo');
 text(s,'Productividad · Ridge · MAE (pp)',96,335,810,70,35,true,BLUE);
 text(s,'Empleo · Logit · macro-F1',1015,335,810,70,35,true,BLUE);
 for(const [hyp,metric,left,max] of [['H1','MAE',96,6],['H3','macro_F1',1015,.85]]){
  barChart(s,['Mismo trimestre','t−1 exacto'],['Modelo','Referencia train'].map((name,i)=>({name,fill:i===0?BLUE:'#9CA7AF',values:['Mismo trimestre','Rezago exacto t-1'].map(h=>temp.find(r=>r.hipotesis===hyp&&r.horizonte===h&&r.conjunto==='test'&&r.modelo===name)[metric])})),{left,top:420,width:810,height:300,max,format:'0.00'});
 }
 text(s,'Muestras distintas: 37.544 filas contemporáneas y 35.233 pares consecutivos',96,745,1728,60,32,false,MUTED);
 text(s,'Un hueco del panel no se salta: t−1 debe ser el trimestre calendario inmediatamente anterior',96,825,1728,90,36,true);
 caption(s,'Solo X de t−1 mide anticipación secuencial. Permite observar trimestres previos de test a medida que transcurre el año.');

 s=slide(p,'Conclusiones y alcance de la evidencia',10,10,'modelado.ipynb, tablas ejecutadas',40,'Sintetizar sin repetir historias causales ni presentar H2 como resuelta. La revisión histórica y el dataset sintético impiden validación externa o confirmatoria.');
 text(s,'H1 · La magnitud de inversión depende del control de adopción y de observaciones influyentes',96,250,1728,145,45,true,BLUE);
 text(s,'H3 · El saldo combina creación y desplazamiento. Neutral y los costos por clase condicionan la evaluación',96,455,1728,145,43,true);
 text(s,'El panel permite evaluar rezagos, pero estos resultados sintéticos no prueban causalidad ni validez en empresas reales',96,680,1728,145,42);
 caption(s,'Pendientes: documentación del generador, casos de uso, transformación de tareas y validación prospectiva independiente.');
 await finish(p,'TP3_graficos_final',10,[3,8],[2,4,5,6,7,9]);
}
const target=process.argv[2]??'all';
try{if(target==='all'||target==='tp2')await tp2();if(target==='all'||target==='tp3')await tp3();}
catch(e){console.error(e?.stack??e);process.exitCode=1;}
