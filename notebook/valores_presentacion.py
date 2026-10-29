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
DECK = ROOT / 'deck' / 'IA_en_las_empresas_presentation_v2.pptx'
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

    cur = json.loads((RESULTS / 'curacion_resumen.json').read_text(encoding='utf8'))
    for field, label in [('filas_crudas', 'Respuestas'), ('empresas_crudas', 'Empresas'), ('periodos', 'Trimestres')]:
        add(2, 'texto_entero', 'Dataset', label, cur[field], 'conteo', 'curacion_resumen.json',
            'Recuento del archivo company, antes de la curación')
    for item in cur['recuperacion']:
        if item['variable'] in ['industry', 'company_size']:
            add(3, 'texto_entero', 'Categorías recuperadas', item['variable'], item['recuperadas'],
                'celdas', 'curacion_resumen.json', 'Categoría faltante completada con atributo único observado por empresa')

    quart = _read('eda_cuartiles')
    add(2, 'texto_entero', 'Muestra común 2026 Q2', 'Empresas',
        quart.loc[quart.variable.eq('ai_adoption_rate'), 'n'].sum(), 'conteo', 'eda_cuartiles.csv',
        'Suma de los cuatro cuartiles; una observación por empresa y muestra común para ambos predictores')
    for variable, label in [('ai_adoption_rate', 'Adopción'),
                            ('ai_investment_per_employee', 'Inversión')]:
        a = quart.loc[quart.variable.eq(variable)].set_index('cuartil')
        for q, category in [('Q1', 'Q1 bajo'), ('Q2', 'Q2'), ('Q3', 'Q3'), ('Q4', 'Q4 alto')]:
            add(2, 'grafico', label, category, a.loc[q, 'pct_productividad_mayor_20'] / 100,
                'proporción', 'eda_cuartiles.csv',
                'media(productivity_change_percent > 20), cuartil del predictor en muestra común 2026 Q2')

    twfe = _read('h1_twfe').set_index(['especificacion', 'variable'])
    add(4, 'texto_entero', 'Muestra común TWFE', 'Observaciones', twfe.n.iloc[0], 'conteo',
        'h1_twfe.csv', 'Casos completos de respuesta y controles para las dos especificaciones')
    for spec, var, category in [
        ('Sin adopción', 'log_inversion', 'Inversión sin adopción'),
        ('Con adopción', 'log_inversion', 'Inversión con adopción'),
        ('Con adopción', 'adopcion', 'Adopción con inversión')]:
        a = twfe.loc[(spec, var)]
        np.testing.assert_allclose(a.cambio_por_sd_within, a.beta * a.sd_within, rtol=1e-12)
        add(4, 'grafico', 'Cambio de productividad', category, a.cambio_por_sd_within,
            'puntos porcentuales', 'h1_twfe.csv', 'beta × sd(M_empresa,periodo X), ddof=1')

    sens = _read('h1_sensibilidad')
    for spec in ['Sin adopción', 'Con adopción']:
        for sample, label in [('Completa', 'Completa'), ('Sin leverage alto', 'Sin leverage alto'),
                               ('Sin residuos |z|>3.5', 'Sin residuos extremos')]:
            a = sens.loc[sens.especificacion.eq(spec) & sens.variable.eq('log_inversion') & sens.muestra.eq(sample)].iloc[0]
            add(4, 'grafico', spec, label, a.beta, 'coeficiente de log1p(inversión)',
                'h1_sensibilidad.csv', f'Reajuste TWFE en muestra: {sample}; EE agrupados por empresa')

    pred = _read('h1_prediccion').query("conjunto == 'test'")
    for _, a in pred.iterrows():
        add(5, 'grafico', 'MAE en empresas nuevas', a.modelo, a.MAE,
            'puntos porcentuales', 'h1_prediccion.csv', 'media(abs(y_test − pred_test))')
    for model in ['Ridge', 'Gradient boosting']:
        a = pred.set_index('modelo').loc[model]
        add(5, 'texto', 'R² en test', model, a.R2, 'R²', 'h1_prediccion.csv',
            '1 − sum((y − pred)^2) / sum((y − media(y_test))^2)')

    neutral = _read('h3_neutral')
    for _, a in neutral.iterrows():
        add(6, 'grafico', 'Observaciones neutrales', a.grupo_dotacion + ' empleados',
            a.neutral_pct / 100, 'proporción', 'h3_neutral.csv',
            'media(jobs_created == jobs_displaced), dentro de cada grupo de dotación')

    contrasts = _read('h3_contrastes').query("especificacion == 'Completo'")
    for var, label in [('ai_adoption_rate', 'Adopción (+10 puntos)'),
                        ('task_automation_rate', 'Automatización (+10 puntos)')]:
        for prefix, category in [('net_creation', 'Creación / neutral'),
                                  ('net_displacement', 'Desplazamiento / neutral')]:
            a = contrasts.loc[contrasts.variable.eq(var) & contrasts.contraste.str.startswith(prefix)].iloc[0]
            np.testing.assert_allclose(np.exp(a.coef), a.RRR, rtol=1e-12)
            add(7, 'grafico', label, category, a.coef, 'log(RRR)', 'h3_contrastes.csv',
                'Coeficiente MNLogit; adopción/automatización divididas por 10; neutral es referencia')
    vif = _read('h3_vif').query("especificacion == 'Completo'")
    add(7, 'texto', 'VIF máximo', vif.loc[vif.VIF.idxmax(), 'variable'], vif.VIF.max(),
        'VIF', 'h3_vif.csv', 'max(1/(1 − R² auxiliar)) del diseño de entrenamiento')

    models = _read('h3_modelos').query("conjunto == 'test'").set_index('modelo')
    for model in ['Logit lineal', 'Logit spline', 'RF base', 'RF ampliado']:
        for metric, label in [('macro_F1', 'Macro-F1'), ('net_creation_f1-score', 'F1 creación'),
                               ('net_displacement_f1-score', 'F1 desplaz.')]:
            add(8, 'tabla_metricas', model, label, models.loc[model, metric], 'F1',
                'h3_modelos.csv', 'F1=2PR/(P+R); macro-F1=media de F1 de las tres clases')
    matrices = _read('h3_matrices').query("modelo == 'RF ampliado'")
    class_names = {'neutral': 'Neutral', 'net_creation': 'Creación', 'net_displacement': 'Desplaz.'}
    for true in class_names:
        part = matrices.loc[matrices.real.eq(true)]
        total = part.n.sum()
        assert total > 0
        for guess in class_names:
            value = part.loc[part.predicha.eq(guess), 'n'].iloc[0] / total
            add(8, 'matriz', class_names[true], class_names[guess], value, 'proporción por fila',
                'h3_matrices.csv', 'conteo(real, predicha) / sum_predicha conteo(real, predicha)')
            if true == guess:
                np.testing.assert_allclose(value, models.loc['RF ampliado', true + '_recall'], atol=1e-12)
    cv = _read('h3_modelos_cv')
    chosen = cv.loc[cv.elegido_familia].sort_values(['macro_F1_CV', 'modelo'], ascending=[False, True]).iloc[0]
    assert chosen.modelo == 'RF ampliado', 'La elección de CV cambió; actualizar el nombre en la presentación'
    add(8, 'contexto', 'Selección por CV', chosen.modelo, chosen.macro_F1_CV, 'macro-F1 CV',
        'h3_modelos_cv.csv', 'max de macro-F1 promedio en GroupKFold, sin elegir con test')
    add(8, 'texto', 'Referencia mayoritaria', 'Accuracy', models.loc['Mayoritaria', 'accuracy'],
        'proporción', 'h3_modelos.csv', 'media(y_test == clase más frecuente de train)')

    temporal = _read('validacion_temporal').query("conjunto == 'test'")
    for horizon in ['Mismo trimestre', 'Rezago exacto t-1']:
        counts = temporal.loc[temporal.horizonte.eq(horizon), 'n'].unique()
        assert len(counts) == 1
        add(9, 'texto_entero', 'Muestra temporal de test', horizon, counts[0], 'conteo',
            'validacion_temporal.csv', 'Filas con respuesta disponible en 2026; pares calendario exactos para t−1')
    for hyp, metric, unit in [('H1', 'MAE', 'puntos porcentuales'), ('H3', 'macro_F1', 'F1')]:
        for model in ['Modelo', 'Referencia train']:
            for horizon, label in [('Mismo trimestre', 'Mismo trimestre'), ('Rezago exacto t-1', 't−1 exacto')]:
                a = temporal.loc[temporal.hipotesis.eq(hyp) & temporal.modelo.eq(model) & temporal.horizonte.eq(horizon)].iloc[0]
                add(9, 'grafico', model, label + ' · ' + hyp, a[metric], unit,
                    'validacion_temporal.csv', f'{metric} en 2026; entrenar 2023–24, elegir penalización en 2025')
    return pd.DataFrame(rows)


def _norm(s):
    return re.sub(r'\s+', ' ', str(s)).strip()


def verificar_pptx(values, deck=DECK):
    """Comprueba datos cacheados de los ocho gráficos y celdas de la slide 8."""
    matched = 0
    chart_count = 0
    with zipfile.ZipFile(deck) as package:
        for row in values.loc[values.elemento.eq('texto_entero')].itertuples():
            text = ' '.join(ET.fromstring(package.read(f'ppt/slides/slide{row.slide}.xml')).itertext())
            shown = f'{int(row.valor):,}'.replace(',', '.')
            assert re.search(r'(?<![\d.])' + re.escape(shown) + r'(?!\d|\.\d)', text), f'Slide {row.slide}: falta {shown}'
        for slide in [2, 4, 5, 6, 7, 9]:
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
                    if slide == 9:
                        # La unidad/hipótesis distingue los dos gráficos con nombres iguales.
                        hyp = 'H1' if max(nums) > 1 else 'H3'
                        expected = expected.loc[expected.categoria.str.endswith(' · ' + hyp)].copy()
                        expected['categoria'] = expected.categoria.str.removesuffix(' · ' + hyp)
                    assert len(expected) == len(nums) == len(cats), f'Slide {slide}, serie {name}: cantidad distinta'
                    lookup = {_norm(r.categoria): r.valor for r in expected.itertuples()}
                    assert set(map(_norm, cats)) == set(lookup), f'Slide {slide}, categorías cambiadas'
                    np.testing.assert_allclose(nums, [lookup[_norm(c)] for c in cats], rtol=0, atol=5.1e-11,
                                               err_msg=f'Slide {slide}, serie {name}: cifra desactualizada')
                    matched += len(nums)
        assert chart_count == 8 and matched == int(values.elemento.eq('grafico').sum())
        s8 = ET.fromstring(package.read('ppt/slides/slide8.xml'))
        tables = [[[''.join(c.itertext()) for c in row.findall('./a:tc', NS)]
                   for row in table.findall('./a:tr', NS)] for table in s8.findall('.//a:tbl', NS)]
        metric_table = next(t for t in tables if t[0][0] == 'Modelo')
        for row in metric_table[1:]:
            expected = values.loc[values.elemento.eq('tabla_metricas') & values.serie.eq(row[0])]
            assert len(expected) == 3
            for label, actual in zip(metric_table[0][1:], row[1:]):
                val = expected.loc[expected.categoria.eq(label), 'valor'].iloc[0]
                assert actual == f'{val:.3f}'.replace('.', ','), f'Slide 8: {row[0]}, {label}'
        matrix = next(t for t in tables if t[0][0] == 'Real / pred.')
        for row in matrix[1:]:
            for label, actual in zip(matrix[0][1:], row[1:]):
                val = values.loc[values.elemento.eq('matriz') & values.serie.eq(row[0]) & values.categoria.eq(label), 'valor'].iloc[0]
                assert actual == f'{100 * val:.1f}%'.replace('.', ','), f'Slide 8: matriz {row[0]}, {label}'
    return {'presentacion': deck.relative_to(ROOT).as_posix(),
            'sha256': hashlib.sha256(deck.read_bytes()).hexdigest(),
            'graficos_verificados': chart_count, 'valores_graficos_verificados': matched,
            'celdas_metricas_verificadas': 12, 'celdas_matriz_verificadas': 9,
            'conteos_texto_verificados': int(values.elemento.eq('texto_entero').sum()),
            'tolerancia_numerica_graficos': 5.1e-11, 'estado': 'OK'}


def exportar_valores():
    values = construir_valores()
    audit = verificar_pptx(values)
    values.to_csv(RESULTS / 'valores_presentacion.csv', index=False)
    (RESULTS / 'presentacion_v2_comprobacion.json').write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    lines = ['# Cifras de la presentación de TP3', '',
             'Este documento se genera con `python scripts/calcular_valores_presentacion.py` a partir de los CSV ejecutados.', '',
             'La presentación de entrega es `deck/IA_en_las_empresas_presentation_v2.pptx`. Se lee para verificarla, sin modificarla.', '',
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
                  '12 celdas de métricas y 9 celdas de la matriz de confusión. La comprobación falla si una cifra deja de coincidir.', '',
                  'El coeficiente de adopción/automatización del logit se expresa por +10 puntos y en log(RRR); exponenciarlo da la RRR frente a neutral. '
                  'TWFE usa cambios de una misma empresa y no es intercambiable con el modelo predictivo entre empresas. '
                  'Las métricas temporales contemporáneas y rezagadas se calculan sobre muestras distintas.', ''])
    (ROOT / 'revision' / 'VALORES_PRESENTACION.md').write_text('\n'.join(lines), encoding='utf8')
    return values, audit
