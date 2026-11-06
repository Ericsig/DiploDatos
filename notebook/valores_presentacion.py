"""Trazabilidad de las cifras de TP3, sin volver a ajustar ni elegir modelos.

Los valores se leen de los CSV producidos por revision_analisis/revision_graficos.
La comprobación del PPTX es de solo lectura y respeta las ediciones del equipo.
"""
from pathlib import Path
import json
import hashlib
import posixpath
import re
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / 'revision' / 'resultados'
DECK = ROOT / 'deck' / 'IA_en_las_empresas_presentation_v3.pptx'
NS = {
    'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def _read(name):
    return pd.read_csv(RESULTS / f'{name}.csv')


def construir_valores():
    """Cada registro identifica cifra, unidad, cálculo y fuente de la slide."""
    rows = []

    def add(slide, element, series, category, value, unit, source, calculation):
        rows.append({'slide': slide, 'elemento': element, 'serie': series,
                     'categoria': category, 'valor': float(value), 'unidad': unit,
                     'fuente': source, 'calculo': calculation})

    def mensaje(slide, value, decimals, suffix, unit, source, calculation, shown=None):
        """Cifra redondeada que aparece en una frase de la diapositiva."""
        shown = shown or f'{value:.{decimals}f}'.replace('.', ',') + suffix
        add(slide, 'texto_redondeado', 'Mensaje', shown, value, unit, source, calculation)

    cur = json.loads((RESULTS / 'curacion_resumen.json').read_text(encoding='utf8'))
    # Diapositiva 2: datos y curación
    for field, label in [('filas_crudas', 'Respuestas'), ('empresas_crudas', 'Empresas'), ('periodos', 'Trimestres')]:
        add(2, 'texto_entero', 'Dataset', label, cur[field], 'conteo', 'curacion_resumen.json',
            'Recuento del archivo company, antes de la curación')
    for item in cur['recuperacion']:
        if item['variable'] in ['industry', 'company_size']:
            add(2, 'texto_entero', 'Categorías recuperadas', item['variable'], item['recuperadas'],
                'celdas', 'curacion_resumen.json', 'Categoría faltante completada con atributo único observado por empresa')
    add(2, 'texto_entero', 'Curación', 'Filas sin adopción o categoría irrecuperable', cur['filas_crudas'] - cur['tras_faltantes'],
        'conteo', 'curacion_resumen.json', 'filas_crudas − tras_faltantes')
    add(2, 'texto_entero', 'Curación', 'Filas con adopción fuera de rango', cur['adopcion_invalida'], 'conteo',
        'curacion_resumen.json', 'adopcion_invalida')
    assert cur['tras_faltantes'] - cur['adopcion_invalida'] == cur['panel_observado'][0]
    add(2, 'texto_entero', 'Curación', 'Respuestas finales', cur['panel_observado'][0], 'conteo',
        'curacion_resumen.json', 'panel_observado: filas tras la curación, antes de imputar predictoras')
    panel_obs = pd.read_csv(ROOT / 'data' / 'data_panel_observado.csv', usecols=['company_id', 'survey_year', 'quarter'])
    assert len(panel_obs) == cur['panel_observado'][0]
    assert not panel_obs.duplicated(['company_id', 'survey_year', 'quarter']).any(), 'Hay duplicados empresa-trimestre'
    add(2, 'texto_entero', 'Curación', 'Empresas finales', panel_obs.company_id.nunique(), 'conteo',
        'data/data_panel_observado.csv', 'nunique(company_id); sin duplicados empresa-trimestre')

    quart = _read('eda_cuartiles')
    add(4, 'texto_entero', 'Muestra común 2026 Q2', 'Empresas',
        quart.loc[quart.variable.eq('ai_adoption_rate'), 'n'].sum(), 'conteo', 'eda_cuartiles.csv',
        'Suma de los cuatro cuartiles; una observación por empresa y muestra común para ambos predictores')
    for variable, label in [('ai_adoption_rate', 'Empresas ordenadas por adopción'),
                            ('ai_investment_per_employee', 'Empresas ordenadas por inversión')]:
        a = quart.loc[quart.variable.eq(variable)].set_index('cuartil')
        for q, category in [('Q1', 'Cuartil 1 (25% más bajo)'), ('Q2', 'Cuartil 2'), ('Q3', 'Cuartil 3'),
                            ('Q4', 'Cuartil 4 (25% más alto)')]:
            add(4, 'grafico', label, category, a.loc[q, 'pct_productividad_mayor_20'] / 100,
                'proporción', 'eda_cuartiles.csv',
                'media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2')
    pct_q = quart.set_index(['variable', 'cuartil']).pct_productividad_mayor_20
    for key, decimals in [(('ai_adoption_rate', 'Q1'), 2), (('ai_investment_per_employee', 'Q4'), 1),
                          (('ai_investment_per_employee', 'Q1'), 1)]:
        mensaje(4, pct_q[key], decimals, '%', 'porcentaje', 'eda_cuartiles.csv',
                f'Subtítulo: {key[0]}, {key[1]}, % de empresas con mejora > 20')

    twfe = _read('h1_twfe').set_index(['especificacion', 'variable'])
    for slide in [2, 5]:
        add(slide, 'texto_entero', 'Muestra común TWFE', 'Observaciones', twfe.n.iloc[0], 'conteo',
            'h1_twfe.csv', 'Casos completos de productividad, inversión e ingresos para las dos especificaciones')
    add(5, 'texto_entero', 'Curación', 'Respuestas finales', cur['panel_observado'][0], 'conteo',
        'curacion_resumen.json', 'Total del que sale la muestra TWFE')
    for spec, var, category in [
        ('Sin adopción', 'log_inversion', 'Inversión sin adopción'),
        ('Con adopción', 'log_inversion', 'Inversión con adopción'),
        ('Con adopción', 'adopcion', 'Adopción con inversión')]:
        a = twfe.loc[(spec, var)]
        np.testing.assert_allclose(a.cambio_por_sd_within, a.beta * a.sd_within, rtol=1e-12)
        add(5, 'grafico', 'Cambio de productividad', category, a.cambio_por_sd_within,
            'puntos porcentuales', 'h1_twfe.csv', 'beta × sd(M_empresa,periodo X), ddof=1')
    sd_inv = twfe.xs('log_inversion', level='variable').sd_within
    assert sd_inv.nunique() == 1
    sd_inv = float(sd_inv.iloc[0])
    sens = _read('h1_sensibilidad')
    for spec in ['Sin adopción', 'Con adopción']:
        for sample, label in [('Completa', 'Todos los datos'),
                               ('Sin leverage alto', 'Sin puntos muy alejados (leverage alto)'),
                               ('Sin residuos |z|>3.5', 'Sin errores muy grandes (residuos)')]:
            a = sens.loc[sens.especificacion.eq(spec) & sens.variable.eq('log_inversion') & sens.muestra.eq(sample)].iloc[0]
            add(5, 'grafico', f'Modelo {spec.lower()}', label, a.beta * sd_inv, 'puntos porcentuales',
                'h1_sensibilidad.csv; h1_twfe.csv',
                f'beta de la muestra {sample} × sd within de inversión en la muestra completa (misma vara que el gráfico izquierdo)')
    con = sens.loc[sens.especificacion.eq('Con adopción') & sens.variable.eq('log_inversion')].set_index('muestra')
    retiradas = con.loc['Completa', 'n'] - con.loc['Sin leverage alto', 'n']
    add(5, 'texto_entero', 'Filas con leverage alto', 'Retiradas', retiradas, 'conteo', 'h1_sensibilidad.csv',
        'n(Completa) − n(Sin leverage alto), modelo con adopción')
    mensaje(5, 100 * retiradas / con.loc['Completa', 'n'], 1, '%', 'porcentaje', 'h1_sensibilidad.csv',
            'Filas retiradas / n(Completa)')
    for sample in ['Completa', 'Sin leverage alto']:
        mensaje(5, con.loc[sample, 'beta'] * sd_inv, 2, '', 'puntos porcentuales', 'h1_sensibilidad.csv; h1_twfe.csv',
                f'Mensaje: inversión con adopción, muestra {sample}, por un aumento típico')

    pred = _read('h1_prediccion').query("conjunto == 'test'").set_index('modelo')
    assert abs(pred.loc['Media train', 'R2']) < 0.005, 'La referencia ya no tiene R² ≈ 0'
    r2 = lambda m: f"{100 * pred.loc[m, 'R2']:.1f}".replace('.', ',')
    labels = {'Media train': 'Siempre el promedio (referencia) R² ≈ 0%',
              'Ridge': f'Ridge R² = {r2("Ridge")}%', 'Gradient boosting': f'Gradient boosting R² = {r2("Gradient boosting")}%'}
    for model, a in pred.iterrows():
        add(6, 'grafico', 'MAE en empresas nuevas', labels[model], a.MAE,
            'puntos porcentuales', 'h1_prediccion.csv', 'media(abs(y_test − pred_test)); el rótulo incluye el R² en test')
        mensaje(6, a.MAE, 2, '', 'puntos porcentuales', 'h1_prediccion.csv', f'Mensaje: MAE en test de {model}')
    for model in ['Ridge', 'Gradient boosting']:
        add(6, 'texto', 'R² en test', model, pred.loc[model, 'R2'], 'R²', 'h1_prediccion.csv',
            '1 − sum((y − pred)^2) / sum((y − media(y_test))^2); se muestra en el rótulo del gráfico')

    neutral = _read('h3_neutral')
    for _, a in neutral.iterrows():
        add(7, 'grafico', 'Observaciones neutrales', a.grupo_dotacion + ' empleados',
            a.neutral_pct / 100, 'proporción', 'h3_neutral.csv',
            'media(jobs_created == jobs_displaced), dentro de cada grupo de dotación')
    labels_h3 = _read('h3_etiquetas').set_index('clase')
    for column, text in [('empate_exacto', 'empate exacto'), ('banda_0_5_pct', 'banda ±0,5%')]:
        mensaje(7, 100 * labels_h3.loc['neutral', column] / labels_h3[column].sum(), 0, '%', 'porcentaje',
                'h3_etiquetas.csv', f'Recuadro: % de neutrales con {text}')
    alt = _read('h3_targets_alternativos').set_index('target')
    mensaje(7, 100 * alt.loc['Sin neutral', 'accuracy'], 0, '%', 'porcentaje', 'h3_targets_alternativos.csv',
            f"Recuadro: accuracy en test sin neutral ({alt.loc['Sin neutral', 'modelo']})")

    contrasts = _read('h3_contrastes').query("especificacion == 'Completo'")
    for var, label in [('ai_adoption_rate', 'Adopción (+10 puntos)'),
                        ('task_automation_rate', 'Automatización (+10 puntos)')]:
        for prefix, category in [('net_creation', 'P(creación) / P(neutral)'),
                                  ('net_displacement', 'P(desplazamiento) / P(neutral)')]:
            a = contrasts.loc[contrasts.variable.eq(var) & contrasts.contraste.str.startswith(prefix)].iloc[0]
            np.testing.assert_allclose(np.exp(a.coef), a.RRR, rtol=1e-12)
            add(8, 'grafico', label, category, a.RRR, 'RRR', 'h3_contrastes.csv',
                'exp(coeficiente MNLogit); adopción/automatización divididas por 10; neutral es referencia')
            if (var, prefix) in [('ai_adoption_rate', 'net_creation'), ('task_automation_rate', 'net_displacement')]:
                mensaje(8, a.RRR, 2, '', 'RRR', 'h3_contrastes.csv',
                        f'Mensaje: RRR de {var}, {prefix} frente a neutral, por +10 puntos')
            if (var, prefix) == ('ai_adoption_rate', 'net_creation'):
                mensaje(8, a.coef, 2, '', 'log(RRR)', 'h3_contrastes.csv', 'Pie: ejemplo e^coef')
    vif = _read('h3_vif').query("especificacion == 'Completo'")
    add(8, 'contexto', 'VIF máximo', vif.loc[vif.VIF.idxmax(), 'variable'], vif.VIF.max(),
        'VIF', 'h3_vif.csv', 'max(1/(1 − R² auxiliar)) del diseño de entrenamiento; no se muestra en la diapositiva')
    panel = pd.read_csv(ROOT / 'data' / 'raw' / 'company_limpio.csv', usecols=['ai_adoption_rate', 'task_automation_rate'])
    mensaje(8, panel.ai_adoption_rate.corr(panel.task_automation_rate), 1, '', 'correlación de Pearson',
            'data/raw/company_limpio.csv', 'Pie: r entre adopción y automatización, todas las filas con ambos datos')

    models = _read('h3_modelos').query("conjunto == 'test'").set_index('modelo')
    for model in ['Logit lineal', 'Logit spline', 'RF base', 'RF ampliado']:
        for metric, label in [('macro_F1', 'Macro-F1'), ('net_creation_f1-score', 'F1 creación'),
                               ('net_displacement_f1-score', 'F1 desplaz.')]:
            add(9, 'tabla_metricas', {'Logit spline': 'Logit con curvas'}.get(model, model), label,
                models.loc[model, metric], 'F1',
                'h3_modelos.csv', 'F1=2PR/(P+R); macro-F1=media de F1 de las tres clases')
    # Criterio de elección: el más simple entre los que empatan con el mejor dentro de un desvío entre pliegues.
    cv = _read('h3_modelos_cv').loc[lambda x: x.elegido_familia].set_index('modelo')
    simplicidad = ['Logit lineal', 'Logit spline', 'RF base', 'RF ampliado']
    best = cv.macro_F1_CV.idxmax()
    umbral = cv.loc[best, 'macro_F1_CV'] - cv.loc[best, 'sd_macro_F1_CV']
    empatados = [m for m in simplicidad if cv.loc[m, 'macro_F1_CV'] >= umbral]
    chosen = empatados[0]
    assert chosen == 'Logit lineal', 'La elección cambió; actualizar la diapositiva 9 y el guion'
    assert len(empatados) == 3, 'Cambió la cantidad de modelos empatados que dice la diapositiva 9'
    for m in simplicidad:
        add(9, 'contexto', 'Macro-F1 en validación cruzada', m, cv.loc[m, 'macro_F1_CV'], 'macro-F1 CV',
            'h3_modelos_cv.csv', 'Promedio en GroupKFold de la configuración elegida en cada familia' +
            (' (empatado con el mejor)' if m in empatados else ''))
    mensaje(9, cv.loc[best, 'macro_F1_CV'] - cv.loc[empatados, 'macro_F1_CV'].min(), 3, '', 'macro-F1 CV',
            'h3_modelos_cv.csv', 'Mensaje: mayor diferencia entre los modelos empatados')
    mensaje(9, cv.loc[best, 'sd_macro_F1_CV'], 3, '', 'macro-F1 CV', 'h3_modelos_cv.csv',
            f'Mensaje: desvío entre pliegues del mejor ({best}); umbral de empate = mejor − desvío')
    class_names = {'neutral': 'Neutral', 'net_creation': 'Creación', 'net_displacement': 'Desplaz.'}
    for key, name in class_names.items():
        for metric, label in [('precision', 'Cuando la predice, acierta'), ('recall', 'De los casos reales, detecta')]:
            add(9, 'tabla_clases', name, label, models.loc[chosen, f'{key}_{metric}'], 'proporción', 'h3_modelos.csv',
                f'{metric} en test de {chosen}')
    add(9, 'texto', 'Referencia mayoritaria', 'Accuracy', models.loc['Mayoritaria', 'accuracy'],
        'proporción', 'h3_modelos.csv', 'media(y_test == clase más frecuente de train)')
    for model in [chosen, 'Mayoritaria']:
        acc = models.loc[model, 'accuracy']
        mensaje(9, acc, 0, '', 'proporción', 'h3_modelos.csv', f'Pie: accuracy en test de {model}, redondeada a décimos',
                shown=f'{round(acc * 10)} de cada 10')

    temporal = _read('validacion_temporal').query("conjunto == 'test'")
    for horizon in ['Mismo trimestre', 'Rezago exacto t-1']:
        counts = temporal.loc[temporal.horizonte.eq(horizon), 'n'].unique()
        assert len(counts) == 1
        add(10, 'texto_entero', 'Muestra temporal de test', horizon, counts[0], 'conteo',
            'validacion_temporal.csv', 'Filas con respuesta disponible en 2026; pares calendario exactos para t−1')
    reference = {'H1': 'Referencia: siempre el promedio', 'H3': 'Referencia: siempre la clase más frecuente'}
    for hyp, metric, unit in [('H1', 'MAE', 'puntos porcentuales'), ('H3', 'macro_F1', 'F1')]:
        for model in ['Modelo', 'Referencia train']:
            for horizon, label in [('Mismo trimestre', 'Mismo trimestre'), ('Rezago exacto t-1', 'Trimestre anterior')]:
                a = temporal.loc[temporal.hipotesis.eq(hyp) & temporal.modelo.eq(model) & temporal.horizonte.eq(horizon)].iloc[0]
                add(10, 'grafico', reference[hyp] if model != 'Modelo' else model, label + ' · ' + hyp,
                    a[metric], unit,
                    'validacion_temporal.csv', f'{metric} en 2026; entrenar 2023–24, elegir penalización en 2025')
                if model == 'Modelo':
                    mensaje(10, a[metric], 2, '', unit, 'validacion_temporal.csv',
                            f'Mensaje: {metric} de {hyp} en 2026, {label}')
    return pd.DataFrame(rows)


def _norm(s):
    return re.sub(r'\s+', ' ', str(s)).strip()


def verificar_pptx(values, deck=DECK):
    """Comprueba datos cacheados de los ocho gráficos, las tablas de la diapositiva 9 y las cifras de las frases."""
    matched = 0
    chart_count = 0
    with zipfile.ZipFile(deck) as package:
        for row in values.loc[values.elemento.eq('texto_entero')].itertuples():
            text = ' '.join(ET.fromstring(package.read(f'ppt/slides/slide{row.slide}.xml')).itertext())
            shown = f'{int(row.valor):,}'.replace(',', '.')
            assert re.search(r'(?<![\d.])' + re.escape(shown) + r'(?!\d|\.\d)', text), f'Slide {row.slide}: falta {shown}'
        for row in values.loc[values.elemento.eq('texto_redondeado')].itertuples():
            text = ''.join(ET.fromstring(package.read(f'ppt/slides/slide{row.slide}.xml')).itertext())
            assert re.search(r'(?<![\d,])' + re.escape(row.categoria) + r'(?![\d])', text), f'Slide {row.slide}: falta {row.categoria}'
        for slide in [4, 5, 6, 7, 8, 10]:
            xml = ET.fromstring(package.read(f'ppt/slides/slide{slide}.xml'))
            rels = ET.fromstring(package.read(f'ppt/slides/_rels/slide{slide}.xml.rels'))
            targets = {r.attrib['Id']: r.attrib['Target'] for r in rels}
            for chart_ref in xml.findall('.//c:chart', NS):
                chart_count += 1
                target = targets[chart_ref.attrib['{' + NS['r'] + '}id']]
                part = posixpath.normpath('ppt/slides/' + target) if not target.startswith('/') else target.lstrip('/')
                chart = ET.fromstring(package.read(part))
                for ser in chart.findall('.//c:ser', NS):
                    name = _norm(''.join(x.text or '' for x in ser.findall('./c:tx//c:v', NS)))
                    cats = [x.text or '' for x in ser.findall('./c:cat//c:v', NS)]
                    nums = [float(x.text) for x in ser.findall('./c:val//c:v', NS)]
                    expected = values.loc[values.slide.eq(slide) & values.elemento.eq('grafico') & values.serie.eq(name)]
                    if slide == 10:
                        # La unidad/hipótesis distingue los dos gráficos con la serie «Modelo».
                        hyp = 'H1' if max(nums) > 1 else 'H3'
                        expected = expected.loc[expected.categoria.str.endswith(' · ' + hyp)].copy()
                        expected['categoria'] = expected.categoria.str.removesuffix(' · ' + hyp)
                    assert len(expected) == len(nums) == len(cats), f'Slide {slide}, serie {name}: cantidad distinta'
                    lookup = {_norm(r.categoria): r.valor for r in expected.itertuples()}
                    assert set(map(_norm, cats)) == set(lookup), f'Slide {slide}, categorías cambiadas: {cats}'
                    np.testing.assert_allclose(nums, [lookup[_norm(c)] for c in cats], rtol=0, atol=5.1e-11,
                                               err_msg=f'Slide {slide}, serie {name}: cifra desactualizada')
                    matched += len(nums)
        assert chart_count == 8 and matched == int(values.elemento.eq('grafico').sum())
        s9 = ET.fromstring(package.read('ppt/slides/slide9.xml'))
        tables = [[[''.join(c.itertext()) for c in row.findall('./a:tc', NS)]
                   for row in table.findall('./a:tr', NS)] for table in s9.findall('.//a:tbl', NS)]
        metric_table = next(t for t in tables if t[0][0] == 'Modelo')
        header = metric_table[0]
        assert header[1] == 'Qué es' and all(row[1].strip() for row in metric_table[1:]), 'Slide 9: falta explicar los modelos'
        metric_cells = 0
        for row in metric_table[1:]:
            expected = values.loc[values.elemento.eq('tabla_metricas') & values.serie.eq(row[0])]
            assert len(expected) == 3, f'Slide 9: modelo {row[0]}'
            for label, actual in zip(header, row):
                if label in set(expected.categoria):
                    val = expected.loc[expected.categoria.eq(label), 'valor'].iloc[0]
                    assert actual == f'{val:.3f}'.replace('.', ','), f'Slide 9: {row[0]}, {label}'
                    metric_cells += 1
        class_table = next(t for t in tables if t[0][0] == 'Clase')
        class_cells = 0
        for row in class_table[1:]:
            for label, actual in zip(class_table[0][1:], row[1:]):
                val = values.loc[values.elemento.eq('tabla_clases') & values.serie.eq(row[0]) & values.categoria.eq(label), 'valor'].iloc[0]
                assert actual == f'{100 * val:.0f}%', f'Slide 9: clases {row[0]}, {label}'
                class_cells += 1
        assert metric_cells == 12 and class_cells == 6
    return {'presentacion': deck.relative_to(ROOT).as_posix(),
            'sha256': hashlib.sha256(deck.read_bytes()).hexdigest(),
            'graficos_verificados': chart_count, 'valores_graficos_verificados': matched,
            'celdas_metricas_verificadas': metric_cells, 'celdas_clases_verificadas': class_cells,
            'conteos_texto_verificados': int(values.elemento.eq('texto_entero').sum()),
            'mensajes_redondeados_verificados': int(values.elemento.eq('texto_redondeado').sum()),
            'tolerancia_numerica_graficos': 5.1e-11, 'estado': 'OK'}


def exportar_valores():
    values = construir_valores()
    audit = verificar_pptx(values)
    values.to_csv(RESULTS / 'valores_presentacion.csv', index=False)
    (RESULTS / 'presentacion_v3_comprobacion.json').write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    lines = ['# Cifras de la presentación de TP3', '',
             'Este documento se genera con `python scripts/calcular_valores_presentacion.py` a partir de los CSV ejecutados.', '',
             'La presentación de entrega es `deck/IA_en_las_empresas_presentation_v3.pptx`. Se lee para verificarla, sin modificarla.', '',
             'Los porcentajes de los gráficos se guardan como proporciones (0,1478 se muestra como 14,78%). Las cifras se redondean solo al presentar.', '']
    for slide, part in values.groupby('slide', sort=True):
        lines.extend([f'## Diapositiva {slide}', '', '| Elemento | Serie / categoría | Valor sin redondear | Unidad | Fuente y cálculo |',
                      '|---|---|---:|---|---|'])
        for r in part.itertuples():
            calc = r.calculo.replace('|', '∣')
            lines.append(f'| {r.elemento} | {r.serie} / {r.categoria} | {r.valor:.12g} | {r.unidad} | `{r.fuente}`: {calc} |')
        lines.append('')
    lines.extend(['## Comprobación contra el PPTX', '',
                  f'Se verificaron {audit["graficos_verificados"]} gráficos, {audit["valores_graficos_verificados"]} valores, '
                  f'{audit["celdas_metricas_verificadas"]} celdas de métricas, {audit["celdas_clases_verificadas"]} celdas de aciertos por clase y {audit["mensajes_redondeados_verificados"]} cifras redondeadas en frases. '
                  'La comprobación falla si una cifra deja de coincidir.', '',
                  'El gráfico del logit muestra la RRR por +10 puntos de adopción o automatización: exp(coeficiente), el factor por el que se multiplica P(clase)/P(neutral). '
                  'El gráfico derecho de H1 lleva cada pendiente a puntos con el mismo desvío within de inversión que el izquierdo. '
                  'La diapositiva 9 elige el modelo más simple entre los que quedan a menos de un desvío entre pliegues del mejor en validación cruzada. '
                  'TWFE usa cambios de una misma empresa y no es intercambiable con el modelo predictivo entre empresas. '
                  'Las métricas temporales contemporáneas y rezagadas se calculan sobre muestras distintas.', ''])
    (ROOT / 'revision' / 'VALORES_PRESENTACION.md').write_text('\n'.join(lines), encoding='utf8')
    return values, audit
