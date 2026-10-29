"""Gráficos de TP3 desde resultados ejecutados y diagnósticos reproducibles."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy import stats
import statsmodels.api as sm
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import SplineTransformer
from linearmodels import PanelOLS
from linearmodels.panel.data import PanelData
from threadpoolctl import threadpool_limits
import revision_analisis as rev

R=rev.RESULTS
G=R/'graficos'
G.mkdir(exist_ok=True)
BLUE='#5980A6';ORANGE='#D98B39';GREEN='#368579';RED='#B75C66';GRAY='#8D98A0'
plt.rcParams.update({'figure.dpi':110,'font.size':11,'axes.titlesize':13,
                     'axes.spines.top':False,'axes.spines.right':False})
def read(name):return pd.read_csv(R/(name+'.csv'))
def finish(fig,name):
    fig.savefig(G/(name+'.png'),dpi=160,bbox_inches='tight')
    plt.show()
    return str(G/(name+'.png'))

def cobertura():
    d=rev.load_panel().reset_index(drop=True)
    fig,ax=plt.subplots(1,2,figsize=(13,4.4),layout='constrained')
    count=d.groupby(['survey_year','quarter']).size()
    ax[0].plot(range(len(count)),count.values,marker='o',color=BLUE)
    ax[0].set_xticks(range(len(count)),[f'{int(y)} {q}' for y,q in count.index],rotation=55,ha='right')
    ax[0].set(title='Cobertura del panel a lo largo del tiempo',ylabel='Respuestas por trimestre',xlabel='Trimestre calendario')
    ax[0].set_ylim(0,count.max()*1.12)
    # Una observación por empresa para no ponderar la dotación por sus respuestas.
    companies=d.drop_duplicates('company_id')
    for size,color in [('Startup',GREEN),('SME',BLUE),('Enterprise',ORANGE)]:
        x=companies.loc[companies.company_size.eq(size),'num_employees'].dropna()
        ax[1].hist(x,bins=np.geomspace(10,20000,35),alpha=.65,label=size,color=color)
    ax[1].set_xscale('log');ax[1].legend()
    ax[1].set(title='Las categorías separan dotaciones en estos datos',xlabel='Empleados (escala log)',ylabel='Empresas, contadas una vez')
    return finish(fig,'01_cobertura_y_escala')

def h1_comparacion():
    d=read('h1_twfe');fig,ax=plt.subplots(1,2,figsize=(13,4.5),layout='constrained')
    inv=d.loc[d.variable.eq('log_inversion')].reset_index(drop=True)
    for i,row in inv.iterrows():
        ax[0].errorbar(row.beta,i,xerr=[[row.beta-row.ci_bajo],[row.ci_alto-row.beta]],fmt='o',capsize=5,color=[BLUE,ORANGE][i],markersize=8)
    ax[0].set_yticks([0,1],inv.especificacion);ax[0].invert_yaxis();ax[0].axvline(0,color=GRAY,lw=1)
    ax[0].set(title='Controlar adopción cambia la pendiente',xlabel='β de log1p(inversión), IC 95% agrupado por empresa')
    labels=['Inversión, sin adopción','Inversión, con adopción','Adopción, con inversión']
    ax[1].barh(labels,d.cambio_por_sd_within,color=[BLUE,ORANGE,GREEN]);ax[1].invert_yaxis()
    for i,v in enumerate(d.cambio_por_sd_within):ax[1].text(v+.035,i,f'{v:.2f}',va='center')
    ax[1].set_xlim(0,d.cambio_por_sd_within.max()*1.2)
    ax[1].set(title='Comparación con cambios de escala equivalente',xlabel='Puntos de productividad por 1 desvío within')
    return finish(fig,'02_h1_especificaciones')

def h1_diagnosticos_y_curva():
    d=rev.load_panel().dropna(subset=['productivity_change_percent','ai_investment_per_employee','annual_revenue_usd_millions','ai_adoption_rate'])
    with threadpool_limits(2):f=rev.fit_twfe(d,True)
    X=PanelData(f.model.exog.dataframe).demean('both').dataframe
    residue=f.resids; fitted=X@f.params
    z=(residue-residue.mean())/residue.std()
    fig,ax=plt.subplots(1,3,figsize=(15,4.1),layout='constrained')
    ax[0].hist(z,bins=90,density=True,color=BLUE,alpha=.8)
    grid=np.linspace(z.min(),z.max(),500);ax[0].plot(grid,stats.norm.pdf(grid),color=ORANGE,label='Normal estándar')
    ax[0].legend();ax[0].set(title='Centro concentrado y colas pesadas',xlabel='Residuo estandarizado',ylabel='Densidad')
    sm.qqplot(z.to_numpy(),line='45',ax=ax[1],marker='.',markersize=2,alpha=.4)
    ax[1].set(title='Q–Q con todas las observaciones',xlabel='Cuantil normal',ylabel='Cuantil observado')
    ax[1].set_xlim(-4.5,4.5)
    sample=np.random.default_rng(rev.SEED).choice(len(X),min(6000,len(X)),replace=False)
    ax[2].scatter(fitted.iloc[sample],residue.iloc[sample],s=5,alpha=.15,color=BLUE)
    bins=pd.qcut(fitted,20,duplicates='drop');means=pd.DataFrame({'x':fitted,'y':residue}).groupby(bins,observed=True).mean()
    ax[2].plot(means.x,means.y,'o-',color=ORANGE,label='Promedios por 20 cuantiles')
    ax[2].axhline(0,color=GRAY,ls='--');ax[2].legend(fontsize=9)
    ax[2].set(title='Residuos y ajuste dentro de empresa',xlabel='Ajuste within (pp)',ylabel='Residuo (pp)')
    finish(fig,'03_h1_residuos')

    sens=read('h1_sensibilidad');fig,ax=plt.subplots(figsize=(10,4.6),layout='constrained')
    labels=sens.muestra.drop_duplicates().tolist()
    for j,(spec,color) in enumerate([('Sin adopción',BLUE),('Con adopción',ORANGE)]):
        s=sens.loc[sens.variable.eq('log_inversion')&sens.especificacion.eq(spec)].set_index('muestra').reindex(labels)
        ax.errorbar(s.beta,np.arange(len(s))+(j-.5)*.16,xerr=1.96*s.se_cluster,fmt='o',capsize=4,label=spec,color=color)
    ax.set_yticks(range(len(labels)),[x.replace('Sin empresas con leverage alto','Sin empresas con leverage alto\n(cambia también la composición)') for x in labels]);ax.invert_yaxis()
    ax.set(title='La inversión es sensible al leverage, no solo a residuos extremos',xlabel='β de log1p(inversión), IC asintótico 95% agrupado');ax.legend()
    finish(fig,'04_h1_sensibilidad')

    # Recuperar la exploración de curvatura usando el modelo y las mediciones corregidas.
    x=np.log1p(d.ai_investment_per_employee)
    transformer=SplineTransformer(n_knots=5,degree=3,include_bias=False)
    basis=transformer.fit_transform(x.to_numpy().reshape(-1,1))
    names=[f'spline_{i}' for i in range(basis.shape[1])]
    design=pd.DataFrame(basis,index=d.index,columns=names);design['adopcion']=d.ai_adoption_rate
    with threadpool_limits(2):
        spline=PanelOLS(d.productivity_change_percent,design,entity_effects=True,time_effects=True,drop_absorbed=True).fit(cov_type='clustered',cluster_entity=True)
    grid=np.linspace(*x.quantile([.01,.99]),140);median=float(x.median())
    contrasts=transformer.transform(grid[:,None])-transformer.transform([[median]])
    beta=spline.params.reindex(names).to_numpy();cov=spline.cov.loc[names,names].to_numpy()
    curve=contrasts@beta;se=np.sqrt(np.maximum(np.einsum('ij,jk,ik->i',contrasts,cov,contrasts),0))
    line=(grid-median)*f.params.log_inversion
    curve_data=pd.DataFrame({'log1p_inversion':grid,'spline_pp':curve,'ci_bajo':curve-1.96*se,'ci_alto':curve+1.96*se,'lineal_pp':line})
    curve_data.to_csv(R/'h1_curva_spline.csv',index=False)
    pd.DataFrame([{'modelo':'Lineal','r2_proyeccion_TWFE':f.rsquared},{'modelo':'Spline','r2_proyeccion_TWFE':spline.rsquared}]).to_csv(R/'h1_curvatura_ajuste.csv',index=False)
    fig,ax=plt.subplots(2,1,figsize=(10,6.5),height_ratios=[3,1],sharex=True,layout='constrained')
    ax[0].plot(grid,curve,color=BLUE,label='TWFE spline, con adopción')
    ax[0].fill_between(grid,curve-1.96*se,curve+1.96*se,color=BLUE,alpha=.18,label='IC puntual 95% agrupado')
    ax[0].plot(grid,line,'--',color=ORANGE,label='TWFE lineal, con adopción');ax[0].axhline(0,color=GRAY,lw=1)
    ax[0].set(title='Exploración de la forma de la asociación con inversión',ylabel='Diferencia de productividad (pp)\nrespecto de la inversión mediana');ax[0].legend(fontsize=9)
    ax[1].hist(x,bins=70,color=GRAY);ax[1].set(xlabel='log1p(inversión por empleado), rango central 1–99%',ylabel='Respuestas');ax[1].set_xlim(grid.min(),grid.max())
    return finish(fig,'05_h1_curvatura')

def h1_prediccion():
    scores=read('h1_prediccion');fig,ax=plt.subplots(1,2,figsize=(12,4.4),layout='constrained')
    for j,part in enumerate(['train','test']):
        a=scores.loc[scores.conjunto.eq(part)]
        ax[0].bar(np.arange(len(a))+(j-.5)*.32,a.MAE,width=.32,color=[GRAY,BLUE][j],label=part)
    ax[0].set_xticks(range(3),a.modelo);ax[0].set(title='La complejidad mejora poco el error de test',ylabel='MAE (puntos de productividad)');ax[0].legend()
    best=read('h1_prediccion_cv').sort_values('MAE_CV').iloc[0]
    d=rev.load_panel();tr,te=rev.grouped_split(d,'productivity_change_percent',rev.FEATURES_H1)
    est=HistGradientBoostingRegressor(max_iter=180,random_state=rev.SEED) if best.modelo=='Gradient boosting' else Ridge()
    model=rev.pipeline(rev.FEATURES_H1,est).set_params(**json.loads(best.parametros))
    with threadpool_limits(2):model.fit(tr[rev.FEATURES_H1],tr.productivity_change_percent);pred=model.predict(te[rev.FEATURES_H1])
    expected=scores.loc[scores.modelo.eq(best.modelo)&scores.conjunto.eq('test')].iloc[0]
    np.testing.assert_allclose(rev.mean_absolute_error(te.productivity_change_percent,pred),expected.MAE,rtol=1e-9)
    np.testing.assert_allclose(rev.r2_score(te.productivity_change_percent,pred),expected.R2,rtol=1e-9)
    cloud=ax[1].hexbin(te.productivity_change_percent,pred,gridsize=50,mincnt=1,bins='log',cmap='Blues')
    lo=min(te.productivity_change_percent.min(),pred.min());hi=max(te.productivity_change_percent.max(),pred.max())
    ax[1].plot([lo,hi],[lo,hi],'--',color=ORANGE,label='Predicción perfecta');ax[1].legend(fontsize=9)
    ax[1].set(title=f'{best.modelo}: lo observado frente a lo estimado',xlabel='Productividad observada (pp)',ylabel='Productividad estimada (pp)');fig.colorbar(cloud,ax=ax[1],label='Conteo (escala log)')
    return finish(fig,'06_h1_prediccion')

def h3_neutral_componentes():
    d=rev.load_panel().reset_index(drop=True)
    neutral=read('h3_neutral');labels=read('h3_etiquetas')
    fig,ax=plt.subplots(1,2,figsize=(13,4.5),layout='constrained')
    bars=ax[0].bar(neutral.grupo_dotacion,neutral.neutral_pct,color=[ORANGE,BLUE,GRAY])
    ax[0].bar_label(bars,fmt='%.1f%%',padding=3);ax[0].set_ylim(0,50)
    ax[0].set(title='El empate exacto se concentra en empresas chicas',xlabel='Empleados',ylabel='Observaciones neutrales (%)')
    x=np.arange(3)
    for j,(col,color,name) in enumerate([('empate_exacto',BLUE,'Empate exacto'),('banda_0_5_pct',ORANGE,'Banda ±0,5%')]):
        ax[1].bar(x+(j-.5)*.34,100*labels[col]/labels[col].sum(),width=.34,label=name,color=color)
    ax[1].set_xticks(x,['Neutral','Creación','Desplazamiento']);ax[1].legend()
    ax[1].set(title='Cambiar neutral cambia la tarea',ylabel='Composición de las clases (%)')
    finish(fig,'07_h3_neutral')
    a=d.loc[d.num_employees.ge(100)].dropna(subset=['ai_adoption_rate','task_automation_rate','creation_rate','displacement_rate'])
    fig,ax=plt.subplots(1,2,figsize=(13,4.5),layout='constrained')
    for pane,x,y,color,title in [(ax[0],'ai_adoption_rate','creation_rate',GREEN,'Adopción y creación de puestos'),(ax[1],'task_automation_rate','displacement_rate',RED,'Automatización y desplazamiento')]:
        pane.hexbin(a[x],100*a[y],gridsize=45,mincnt=1,bins='log',cmap='Blues')
        m=sm.OLS(100*a[y],sm.add_constant(a[[x]])).fit();grid=np.linspace(a[x].min(),a[x].max(),100)
        pane.plot(grid,m.params['const']+m.params[x]*grid,color=color,lw=2,label='Asociación lineal descriptiva')
        pane.set(title=title,xlabel=x.replace('_',' ')+' (%)',ylabel='Puestos / empleados (%)');pane.legend(fontsize=9)
    return finish(fig,'08_h3_componentes')

def h3_logit_colinealidad():
    a=read('h3_contrastes');a=a.loc[a.especificacion.eq('Completo')&a.variable.isin(['ai_adoption_rate','task_automation_rate'])].copy()
    fig,ax=plt.subplots(1,2,figsize=(13,4.8),layout='constrained')
    labels=[]
    for i,(_,row) in enumerate(a.iterrows()):
        lo=np.exp(row.coef-1.96*row.se_cluster);hi=np.exp(row.coef+1.96*row.se_cluster)
        ax[0].errorbar(row.RRR,i,xerr=[[row.RRR-lo],[hi-row.RRR]],fmt='o',capsize=4,color=GREEN if row.variable=='ai_adoption_rate' else RED)
        labels.append(('Adopción' if row.variable=='ai_adoption_rate' else 'Automatización')+' · '+('creación' if row.contraste.startswith('net_creation') else 'desplazamiento'))
    ax[0].set_yticks(range(len(a)),labels);ax[0].invert_yaxis();ax[0].set_xscale('log');ax[0].axvline(1,color=GRAY,ls='--')
    ax[0].set(title='Signos opuestos, sin mecanismo causal identificado',xlabel='RRR por +10 puntos, referencia neutral, IC 95%')
    vif=read('h3_vif');vif=vif.loc[vif.especificacion.eq('Completo')].nlargest(6,'VIF').sort_values('VIF')
    ax[1].barh(vif.variable,vif.VIF,color=BLUE);ax[1].axvline(10,color=ORANGE,ls='--',label='Referencia orientativa: 10');ax[1].legend(fontsize=9)
    ax[1].set(title='Tamaño y dotación comparten información',xlabel='VIF del diseño de entrenamiento')
    return finish(fig,'09_h3_logit_y_colinealidad')

def h3_clasificadores():
    a=read('h3_modelos');a=a.loc[a.conjunto.eq('test')&a.modelo.ne('Mayoritaria')]
    cv=read('h3_modelos_cv');chosen=cv.loc[cv.elegido_familia].sort_values('macro_F1_CV',ascending=False).iloc[0].modelo
    fig,ax=plt.subplots(1,2,figsize=(13,4.8),layout='constrained')
    for j,(metric,color,label) in enumerate([('macro_F1',BLUE,'Macro-F1 (principal)'),('F1_empleo',ORANGE,'F1 empleo (secundaria)')]):
        ax[0].bar(np.arange(len(a))+(j-.5)*.34,a[metric],width=.34,color=color,label=label)
    ax[0].set_xticks(range(len(a)),a.modelo,rotation=18);ax[0].set_ylim(0,.85);ax[0].legend(fontsize=9)
    ax[0].set(title='La métrica principal conserva las tres clases',ylabel='F1 en test')
    for j,(metric,color) in enumerate([('precision',BLUE),('recall',ORANGE)]):
        row=a.set_index('modelo').loc[chosen]
        ax[1].bar(np.arange(3)+(j-.5)*.34,[row[c+'_'+metric] for c in rev.CLASSES],width=.34,label=metric,color=color)
    ax[1].set_xticks(range(3),['Neutral','Creación','Desplazamiento']);ax[1].set_ylim(0,1);ax[1].legend()
    ax[1].set(title=f'{chosen}, elegido por CV: costo por clase',ylabel='Proporción de casos')
    finish(fig,'10_h3_metricas_y_clases')
    matrices=read('h3_matrices');fig,axes=plt.subplots(1,2,figsize=(11,4.8),layout='constrained')
    for axis,name in zip(axes,['Logit spline',chosen]):
        matrix=matrices.loc[matrices.modelo.eq(name)].pivot(index='real',columns='predicha',values='n').reindex(index=rev.CLASSES,columns=rev.CLASSES)
        fractions=matrix.div(matrix.sum(axis=1),axis=0)
        axis.imshow(fractions,vmin=0,vmax=1,cmap='Blues')
        for i in range(3):
            for j in range(3):axis.text(j,i,f'{fractions.iloc[i,j]:.1%}',ha='center',va='center',color='white' if fractions.iloc[i,j]>.55 else '#243746')
        axis.set_xticks(range(3),['Neutral','Creación','Desplaz.']);axis.set_yticks(range(3),['Neutral','Creación','Desplaz.'])
        axis.set(title=name,xlabel='Clase predicha',ylabel='Clase observada')
    return finish(fig,'11_h3_matrices')

def temporal():
    a=read('validacion_temporal').query("conjunto=='test'")
    fig,axes=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    for axis,hyp,metric,title in [(axes[0],'H1','MAE','Productividad · menor MAE es mejor'),(axes[1],'H3','macro_F1','Empleo · mayor macro-F1 es mejor')]:
        for j,(model,color,label) in enumerate([('Modelo',BLUE,'Modelo'),('Referencia train',GRAY,'Referencia train')]):
            sub=a.loc[a.hipotesis.eq(hyp)&a.modelo.eq(model)].set_index('horizonte').reindex(['Mismo trimestre','Rezago exacto t-1'])
            bars=axis.bar(np.arange(2)+(j-.5)*.34,sub[metric],width=.34,color=color,label=label)
            axis.bar_label(bars,fmt='%.2f',padding=3)
        axis.set_xticks(range(2),['X del mismo trimestre','X de t−1 exacto']);axis.legend(fontsize=9)
        axis.set(title=title,ylabel='MAE (pp)' if hyp=='H1' else 'Macro-F1 (3 clases)')
        axis.set_ylim(0,6 if hyp=='H1' else .85)
    return finish(fig,'12_validacion_temporal')

def cuartiles():
    a=read('eda_cuartiles');fig,axis=plt.subplots(figsize=(10,4.8),layout='constrained')
    for j,(variable,color,label) in enumerate([('ai_adoption_rate',BLUE,'Adopción'),('ai_investment_per_employee',ORANGE,'Inversión')]):
        sub=a.loc[a.variable.eq(variable)]
        bars=axis.bar(np.arange(4)+(j-.5)*.36,sub.pct_productividad_mayor_20,width=.36,color=color,label=label)
        axis.bar_label(bars,fmt='%.2f%%',padding=3)
    axis.set_xticks(range(4),['Q1 bajo','Q2','Q3','Q4 alto']);axis.set_ylim(0,18);axis.legend()
    axis.set(title='El hallazgo del EDA, con su comparación completa',xlabel='Cuartil de cada predictor, muestra común de 2026 Q2',ylabel='Empresas con mejora de productividad >20% (%)')
    return finish(fig,'13_eda_cuartiles')
