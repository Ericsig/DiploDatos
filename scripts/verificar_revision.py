"""Verificación de integridad, respuestas observadas y ausencia de fuga básica."""
from pathlib import Path
import sys,json,hashlib,ast
import numpy as np
import pandas as pd
import nbformat
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'notebook'))
import revision_analisis as rev

raw=pd.read_csv(root/'data/raw/ai_company_adoption.csv')
observed=pd.read_csv(root/'data/data_panel_observado.csv')
assert observed.response_id.is_unique and raw.response_id.is_unique
raw_by_id=raw.set_index('response_id')
for c in ['productivity_change_percent','ai_adoption_rate','jobs_created','jobs_displaced']:
    actual=observed.set_index('response_id')[c].dropna()
    expected=raw_by_id.loc[actual.index,c]
    np.testing.assert_allclose(actual,expected,rtol=1e-12,atol=1e-12)
print('OK: respuestas no fabricadas, verificadas contra el crudo')

# Un salto de dos trimestres no genera rezago y no se cruzan empresas.
toy=pd.DataFrame({'company_id':['a','a','b','b'],'period_index':[0,2,0,1],'x':[1,2,3,4]})
lag=rev.make_exact_lags(toy,['x'])
assert lag.company_id.tolist()==['b'] and lag.x_lag1.tolist()==[3]
print('OK: rezagos exactos con huecos y empresas distintas')

train=pd.DataFrame({'industry':['A','A','B'],'company_size':['SME']*3,'x':[1.,3.,100.]})
test=pd.DataFrame({'industry':['A','C'],'company_size':['SME']*2,'x':[np.nan,np.nan]})
imputer=rev.StratumImputer().fit(train)
np.testing.assert_allclose(imputer.transform(test).x,[2.,3.])
assert imputer.global_.x==3.
print('OK: medianas de estrato y respaldo aprendidos únicamente con train')

for name in ['curacion','modelado']:
    nb=nbformat.read(root/'notebook'/f'{name}.ipynb',as_version=4)
    nbformat.validate(nb)
    for c in nb.cells:
        if c.cell_type=='code':
            ast.parse(c.source)
            assert c.execution_count is not None
            assert not any(o.output_type=='error' for o in c.outputs)
print('OK: notebooks válidos y todas las celdas de código ejecutadas sin errores')

manifest=json.loads((root/'revision/resultados/manifest.json').read_text(encoding='utf8'))
for rel,expected in manifest['sha256'].items():
    # También acepta manifiestos previos escritos con separadores de Windows.
    content = (root/rel.replace('\\','/')).read_bytes()
    if manifest.get('sha256_normalizacion') == 'lf':
        content = content.replace(b'\r\n', b'\n')
    assert hashlib.sha256(content).hexdigest()==expected
print('OK: huellas de los CSV fuente coinciden')

part=pd.read_csv(root/'revision/resultados/particiones_temporales.csv')
for _,a in part.groupby(['hipotesis','horizonte']):
    a=a.set_index('conjunto')
    assert a.loc['train','periodo_max']<a.loc['validacion','periodo_min']
    assert a.loc['validacion','periodo_max']<a.loc['test','periodo_min']
print('OK: todas las particiones temporales respetan orden estricto')

twfe=pd.read_csv(root/'revision/resultados/h1_twfe.csv')
assert twfe.n.nunique()==1
cv=pd.read_csv(root/'revision/resultados/h3_modelos_cv.csv')
assert cv.elegido_familia.sum()==4
print('OK: TWFE usa muestra común y las cuatro familias tienen una configuración elegida')

from valores_presentacion import construir_valores, verificar_pptx
audit = verificar_pptx(construir_valores())
print(f"OK: presentación v2, {audit['graficos_verificados']} gráficos y "
      f"{audit['valores_graficos_verificados']} cifras verificadas, más métricas y matriz")

modelado = nbformat.read(root/'notebook/modelado.ipynb',as_version=4)
figuras = sum('image/png' in o.get('data',{}) for c in modelado.cells
              if c.cell_type=='code' for o in c.outputs)
assert figuras >= 14, 'Se perdieron figuras de la revisión visual'
print(f'OK: {figuras} figuras conservadas en el notebook de modelado')
