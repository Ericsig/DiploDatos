"""Análisis reproducible de la devolución docente (TP2/TP3).

No contiene resultados precalculados. Las tablas se exportan desde las mediciones.
"""
from pathlib import Path
import json, sys, platform, hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
from linearmodels import PanelOLS
from linearmodels.panel.data import PanelData
from sklearn.base import BaseEstimator, TransformerMixin, clone
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, SplineTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingRegressor
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.metrics import (f1_score, classification_report, accuracy_score,
    balanced_accuracy_score, log_loss, confusion_matrix, roc_auc_score,
    r2_score, mean_absolute_error, mean_squared_error)
from sklearn.model_selection import GroupShuffleSplit, GroupKFold, GridSearchCV
from statsmodels.stats.outliers_influence import variance_inflation_factor
from threadpoolctl import threadpool_limits

SEED=42
CLASSES=['neutral','net_creation','net_displacement']
FEATURES_H3=['ai_adoption_rate','task_automation_rate','ai_maturity_score',
             'industry','company_size','num_employees','survey_year','quarter']
FEATURES_H1=['ai_investment_per_employee','ai_adoption_rate','industry',
             'company_size','num_employees','annual_revenue_usd_millions',
             'company_age','survey_year','quarter','gdp_per_capita']
CAT=['industry','company_size','survey_year','quarter']
ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'revision/resultados'
RESULTS.mkdir(parents=True,exist_ok=True)

def save_table(name,table):
    table.to_csv(RESULTS/f'{name}.csv',index=False)
    return table

def period(df):
    q=df.quarter.astype('string').str.extract(r'^Q([1-4])$',expand=False).astype('Int64')
    return ((df.survey_year-2023)*4+q-1).astype('Int64')

def targets(df):
    d=df.copy()
    d['net_job_change']=d.jobs_created-d.jobs_displaced
    den=d.num_employees.where(d.num_employees.gt(0))
    d['creation_rate']=d.jobs_created/den
    d['displacement_rate']=d.jobs_displaced/den
    d['net_rate']=d.net_job_change/den
    d['employment_effect']=pd.Series(np.select([d.net_job_change.gt(0),d.net_job_change.lt(0)],
        ['net_creation','net_displacement'],default='neutral'),index=d.index)
    d.loc[d.net_job_change.isna(),'employment_effect']=np.nan
    d['employment_band']=pd.Series(np.select([d.net_rate.gt(.005),d.net_rate.lt(-.005)],
        ['net_creation','net_displacement'],default='neutral'),index=d.index)
    d.loc[d.net_rate.isna(),'employment_band']=np.nan
    return d

def load_panel():
    d=pd.read_csv(ROOT/'data/data_panel_observado.csv')
    d['period_index']=period(d)
    bad=d.period_index.isna() | d.company_id.isna()
    print('Sin fecha/identificador, excluidas:',int(bad.sum()))
    d=d.loc[~bad].copy()
    d.period_index=d.period_index.astype(int)
    d=d.sort_values(['company_id','period_index'])
    assert not d.duplicated(['company_id','period_index']).any()
    d=targets(d)
    return d.set_index(['company_id','period_index'],drop=False,verify_integrity=True)

class StratumImputer(BaseEstimator,TransformerMixin):
    """Medianas por industria×tamaño aprendidas SOLO en fit; respaldo global."""
    def fit(self,X,y=None):
        self.numeric_=[c for c in X if c not in CAT]
        self.global_=X[self.numeric_].median()
        self.by_=X.groupby(['industry','company_size'],dropna=False)[self.numeric_].median()
        assert self.global_.notna().all(), 'Predictor sin observaciones de entrenamiento'
        return self
    def transform(self,X):
        z=X.copy()
        keys=pd.MultiIndex.from_frame(z[['industry','company_size']])
        fill=self.by_.reindex(keys).set_axis(z.index)
        for c in self.numeric_:
            z[c]=z[c].fillna(fill[c]).fillna(self.global_[c])
        for c in CAT:
            if c in z: z[c]=z[c].astype('string').fillna('Sin dato').astype(str)
        for c in ['num_employees','ai_investment_per_employee','annual_revenue_usd_millions']:
            if c in z:
                assert z[c].ge(0).all()
                z[c]=np.log1p(z[c])
        return z

def pipeline(features,model,spline=False):
    cat=[c for c in CAT if c in features]
    num=[c for c in features if c not in cat]
    numsteps=[]
    if spline:numsteps.append(('spline',SplineTransformer(n_knots=4,degree=3,include_bias=False)))
    numsteps.append(('scale',StandardScaler()))
    prep=ColumnTransformer([('num',Pipeline(numsteps),num),
        ('cat',OneHotEncoder(drop='first',handle_unknown='ignore',sparse_output=False),cat)],
        sparse_threshold=0)
    return Pipeline([('imputar',StratumImputer()),('codificar',prep),('modelo',model)])

def grouped_split(d,target,features):
    a=d.loc[d[target].notna()].copy()
    tr,te=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=SEED).split(a,groups=a.company_id))
    train,test=a.iloc[tr],a.iloc[te]
    assert set(train.company_id).isdisjoint(test.company_id)
    return train,test

def fit_twfe(d,with_adoption=True):
    z=pd.DataFrame(index=d.index)
    z['log_inversion']=np.log1p(d.ai_investment_per_employee)
    z['log_ingresos']=np.log1p(d.annual_revenue_usd_millions)
    if with_adoption:z['adopcion']=d.ai_adoption_rate
    fit=PanelOLS(d.productivity_change_percent,z,entity_effects=True,time_effects=True,drop_absorbed=True).fit(
        cov_type='clustered',cluster_entity=True)
    return fit

def h1_panel(d):
    cols=['productivity_change_percent','ai_investment_per_employee',
          'annual_revenue_usd_millions','ai_adoption_rate']
    a=d.dropna(subset=cols).copy()
    assert a.ai_investment_per_employee.ge(0).all()
    fits={'Sin adopción':fit_twfe(a,False),'Con adopción':fit_twfe(a,True)}
    rows=[]
    for name,f in fits.items():
        X=PanelData(f.model.exog.dataframe).demean('both').dataframe
        for c,b in f.params.items():
            rows.append({'especificacion':name,'variable':c,'n':f.nobs,'beta':b,
                'error_estandar_cluster':f.std_errors[c],'ci_bajo':f.conf_int().loc[c,'lower'],
                'ci_alto':f.conf_int().loc[c,'upper'],'p':f.pvalues[c],
                'sd_within':X[c].std(),'cambio_por_sd_within':b*X[c].std(),
                'cambio_por_IQR_within':b*(X[c].quantile(.75)-X[c].quantile(.25)),
                'r2_within':f.rsquared_within,'r2_proyeccion_twfe':f.rsquared})
    table=save_table('h1_twfe',pd.DataFrame(rows))
    f=fits['Con adopción']
    X=PanelData(f.model.exog.dataframe).demean('both').dataframe
    y=PanelData(f.model.dependent.dataframe).demean('both').dataframe.iloc[:,0]
    np.testing.assert_allclose(y-X@f.params,f.resids,atol=1e-7)
    mat=X.to_numpy(); hat=np.einsum('ij,jk,ik->i',mat,np.linalg.pinv(mat.T@mat),mat)
    # Leverage de pendientes tras absorber FE: no incluye el leverage de las dummies.
    cutoff=4*X.shape[1]/len(X)
    high=pd.Series(hat>cutoff,index=X.index)
    z=(f.resids-f.resids.mean())/f.resids.std()
    extreme=z.abs().gt(3.5)
    sensitivity=[]
    samples={'Completa':a,'Sin leverage alto':a.loc[~high],
        'Sin residuos |z|>3.5':a.loc[~extreme],
        'Sin empresas con leverage alto':a.loc[~a.company_id.isin(a.loc[high,'company_id'])]}
    for label,sample in samples.items():
        for name,ad in [('Sin adopción',False),('Con adopción',True)]:
            m=fits[name] if label=='Completa' else fit_twfe(sample,ad)
            for c,b in m.params.items():
                base=fits[name].params[c]
                sensitivity.append({'muestra':label,'especificacion':name,'variable':c,
                    'n':len(sample),'empresas':sample.company_id.nunique(),
                    'beta':b,'se_cluster':m.std_errors[c],
                    'delta_beta':b-base,'delta_relativo_pct':100*(b-base)/abs(base) if abs(base)>1e-8 else np.nan})
    sensitivity=save_table('h1_sensibilidad',pd.DataFrame(sensitivity))
    Z=(X-X.mean())/X.std()
    v=sm.add_constant(Z)
    vif=save_table('h1_vif',pd.DataFrame({'variable':X.columns,
        'vif_within':[variance_inflation_factor(v.values,i+1) for i in range(len(X.columns))]}))
    normal=save_table('h1_residuos',pd.DataFrame([{'n':len(z),'skew':stats.skew(z),
        'curtosis_Pearson':stats.kurtosis(z,fisher=False),'leverage_umbral':cutoff,
        'n_leverage_alto':int(high.sum()),'n_residuo_extremo':int(extreme.sum())}]))
    fig,axes=plt.subplots(1,3,figsize=(15,4),constrained_layout=True)
    for ax,c in zip(axes[:2],[c for c in ['log_inversion','log_ingresos','adopcion'] if c in X][:2]):
        take=np.random.default_rng(SEED).choice(len(X),size=min(5000,len(X)),replace=False)
        ax.scatter(X[c].iloc[take],f.resids.iloc[take]+f.params[c]*X[c].iloc[take],s=4,alpha=.15)
        ax.scatter(X.loc[high,c],(f.resids+f.params[c]*X[c]).loc[high],s=7,color='darkorange',alpha=.3,label='Leverage alto')
        ax.set(xlabel=c+' within',ylabel='Residuo parcial (pp)');ax.legend()
    stats.probplot(z,plot=axes[2]);axes[2].set_title('Q–Q de residuos TWFE')
    fig.savefig(RESULTS/'h1_diagnostico.png',dpi=150);plt.show()
    return {'muestra':a,'fits':fits,'tabla':table,'sensibilidad':sensitivity,'vif':vif,'residuos':normal}

def h1_predict(d):
    train,test=grouped_split(d,'productivity_change_percent',FEATURES_H1)
    cv=list(GroupKFold(n_splits=3).split(train,groups=train.company_id))
    candidates={
        'Ridge':(Ridge(),{'modelo__alpha':[1.,10.,100.]}),
        'Gradient boosting':(HistGradientBoostingRegressor(max_iter=180,random_state=SEED),
             {'modelo__max_leaf_nodes':[7,15],'modelo__l2_regularization':[1.,10.]})}
    models={'Media train':DummyRegressor().fit(train[FEATURES_H1],train.productivity_change_percent)}
    cvrows=[]
    for name,(est,grid) in candidates.items():
        search=GridSearchCV(pipeline(FEATURES_H1,est),grid,cv=cv,scoring='neg_mean_absolute_error',n_jobs=1,error_score='raise')
        with threadpool_limits(2):search.fit(train[FEATURES_H1],train.productivity_change_percent)
        models[name]=search.best_estimator_
        cvrows.append({'modelo':name,'MAE_CV':-search.best_score_,'parametros':json.dumps(search.best_params_)})
        print(name,'CV MAE',-search.best_score_,flush=True)
    cvtable=save_table('h1_prediccion_cv',pd.DataFrame(cvrows))
    chosen=cvtable.sort_values(['MAE_CV','modelo']).iloc[0].modelo
    rows=[]
    for name,m in models.items():
        for part,a in [('train',train),('test',test)]:
            with threadpool_limits(2):pred=m.predict(a[FEATURES_H1])
            rows.append({'modelo':name,'conjunto':part,'n':len(a),'empresas':a.company_id.nunique(),
                'R2':r2_score(a.productivity_change_percent,pred),'MAE':mean_absolute_error(a.productivity_change_percent,pred),
                'RMSE':np.sqrt(mean_squared_error(a.productivity_change_percent,pred)), 'elegido_CV':name==chosen})
    return {'cv':cvtable,'tabla':save_table('h1_prediccion',pd.DataFrame(rows)),'elegido':chosen}

def h3_diagnostics(d):
    a=d.dropna(subset=['employment_effect','num_employees','ai_adoption_rate','task_automation_rate']).copy()
    a['grupo_dotacion']=pd.cut(a.num_employees,[0,99,999,np.inf],labels=['10–99','100–999','1000+'])
    neutral=save_table('h3_neutral',a.groupby('grupo_dotacion',observed=True).agg(
        n=('employment_effect','size'),neutral_pct=('employment_effect',lambda s:100*s.eq('neutral').mean())).reset_index())
    exact=a.employment_effect.eq('neutral')
    small=(a.jobs_created.le(5)&a.jobs_displaced.le(5))
    print('Neutral con ambos conteos <=5 (%):',100*small[exact].mean())
    labels=save_table('h3_etiquetas',pd.DataFrame({
        'clase':CLASSES,'empate_exacto':a.employment_effect.value_counts().reindex(CLASSES,fill_value=0).values,
        'banda_0_5_pct':a.employment_band.value_counts().reindex(CLASSES,fill_value=0).values}))
    large=a.loc[a.num_employees.ge(100)]
    rows=[]
    for y,x in [('creation_rate','ai_adoption_rate'),('displacement_rate','task_automation_rate')]:
        fit=sm.OLS(large[y],sm.add_constant(large[[x]])).fit(cov_type='cluster',cov_kwds={'groups':large.company_id})
        rows.append({'respuesta':y,'predictor':x,'n':len(large),'R2':fit.rsquared,'beta':fit.params[x]})
    rates=save_table('h3_componentes',pd.DataFrame(rows))
    train,test=grouped_split(a.loc[~exact],'employment_effect',FEATURES_H3)
    aucrows=[]
    for features in [['ai_adoption_rate'],['task_automation_rate'],['ai_adoption_rate','task_automation_rate']]:
        m=Pipeline([('scale',StandardScaler()),('modelo',LogisticRegression(max_iter=1000))])
        m.fit(train[features],train.employment_effect.eq('net_creation'))
        aucrows.append({'variables':'+'.join(features),'AUC_creacion_test':roc_auc_score(test.employment_effect.eq('net_creation'),m.predict_proba(test[features])[:,1]),'n_test':len(test)})
    auc=save_table('h3_auc_componentes',pd.DataFrame(aucrows))
    corr=a[['ai_adoption_rate','task_automation_rate']].corr().iloc[0,1]
    print('Correlación adopción-automatización:',corr)
    return {'neutral':neutral,'etiquetas':labels,'componentes':rates,'auc':auc,
        'correlacion':corr,'neutral_conteos_pequenos_pct':100*small[exact].mean()}

def mnl_design(a,drop=None):
    num=['ai_adoption_rate','task_automation_rate','ai_maturity_score','num_employees']
    if drop=='num_employees':num.remove(drop)
    cats=['industry','company_size','survey_year','quarter']
    if drop=='company_size':cats.remove(drop)
    z=a[num].copy()
    for c in ['ai_adoption_rate','task_automation_rate']:z[c]/=10
    if 'num_employees' in z:z['num_employees']=np.log1p(z.num_employees)
    z=pd.concat([z,pd.get_dummies(a[cats].astype(str),drop_first=True,dtype=float)],axis=1)
    return sm.add_constant(z).astype(float)

def h3_collinearity(d):
    a=d.dropna(subset=FEATURES_H3+['employment_effect'])
    train,test=grouped_split(a,'employment_effect',FEATURES_H3)
    tables=[];metrics=[];vifs=[]
    for drop in [None,'num_employees','company_size']:
        name='Completo' if drop is None else 'Sin '+drop
        X=mnl_design(train,drop);T=mnl_design(test,drop).reindex(columns=X.columns,fill_value=0)
        y=train.employment_effect.map({c:i for i,c in enumerate(CLASSES)})
        model=sm.MNLogit(y,X)
        with threadpool_limits(2):fit=model.fit(method='newton',maxiter=150,disp=False,cov_type='cluster',cov_kwds={'groups':train.company_id})
        assert fit.mle_retvals['converged']
        prob=np.asarray(fit.predict(T));pred=np.array(CLASSES)[prob.argmax(axis=1)]
        metrics.append({'especificacion':name,'n_train':len(train),'n_test':len(test),
            'macro_F1_test':f1_score(test.employment_effect,pred,labels=CLASSES,average='macro'),
            'log_loss':log_loss(test.employment_effect,prob[:,np.argsort(CLASSES)],labels=sorted(CLASSES)),
            'rango':np.linalg.matrix_rank(X),'columnas':X.shape[1]})
        for j in fit.params.columns:
            for c in X:
                tables.append({'especificacion':name,'contraste':CLASSES[int(j)+1]+' / neutral',
                    'variable':c,'coef':fit.params.loc[c,j],'se_cluster':fit.bse.loc[c,j],
                    'RRR':np.exp(np.clip(fit.params.loc[c,j],-700,700))})
        scaled=X.copy()
        for c in scaled:
            if c!='const':scaled[c]=(scaled[c]-scaled[c].mean())/scaled[c].std()
        with threadpool_limits(2):
            for i,c in enumerate(X):
                if c!='const':vifs.append({'especificacion':name,'variable':c,'VIF':variance_inflation_factor(scaled.to_numpy(),i)})
        print('Logit inferencial:',name,'convergió',flush=True)
    return {'contrastes':save_table('h3_contrastes',pd.DataFrame(tables)),
        'sensibilidad':save_table('h3_colinealidad_performance',pd.DataFrame(metrics)),
        'vif':save_table('h3_vif',pd.DataFrame(vifs))}

def class_metrics(name,part,y,pred,prob=None,classes=None):
    report=classification_report(y,pred,labels=CLASSES,output_dict=True,zero_division=0)
    row={'modelo':name,'conjunto':part,'n':len(y),'macro_F1':f1_score(y,pred,labels=CLASSES,average='macro',zero_division=0),
        'F1_empleo':f1_score(y,pred,labels=CLASSES[1:],average='macro',zero_division=0),
        'accuracy':accuracy_score(y,pred),'balanced_accuracy':balanced_accuracy_score(y,pred)}
    for c in CLASSES:
        for metric in ['precision','recall','f1-score']:row[c+'_'+metric]=report[c][metric]
    if prob is not None:row['log_loss']=log_loss(y,prob[:,np.argsort(classes)],labels=sorted(classes))
    return row

def h3_predict(d):
    train,test=grouped_split(d,'employment_effect',FEATURES_H3)
    folds=list(GroupKFold(3).split(train,groups=train.company_id))
    for tr,va in folds:assert set(train.iloc[tr].company_id).isdisjoint(train.iloc[va].company_id)
    scoring={'macro_F1':__import__('sklearn.metrics',fromlist=['make_scorer']).make_scorer(f1_score,labels=CLASSES,average='macro',zero_division=0,pos_label=None),
        'F1_empleo':__import__('sklearn.metrics',fromlist=['make_scorer']).make_scorer(f1_score,labels=CLASSES[1:],average='macro',zero_division=0,pos_label=None)}
    candidates={
        'Logit lineal':(LogisticRegression(max_iter=1500),{'modelo__C':[.1,1.]},False),
        'Logit spline':(LogisticRegression(max_iter=1500),{'modelo__C':[.1,1.]},True),
        'RF base':(RandomForestClassifier(n_estimators=200,max_depth=18,min_samples_leaf=25,random_state=SEED,n_jobs=2),{'modelo__max_features':['sqrt']},False),
        'RF ampliado':(RandomForestClassifier(n_estimators=200,max_depth=12,min_samples_leaf=5,max_features=.5,random_state=SEED,n_jobs=2),
            {'modelo__min_samples_leaf':[5,25],'modelo__class_weight':[None,{'neutral':.5,'net_creation':1.,'net_displacement':1.}]},False)}
    models={};cvrows=[]
    for name,(est,grid,spl) in candidates.items():
        search=GridSearchCV(pipeline(FEATURES_H3,est,spl),grid,cv=folds,scoring=scoring,refit='macro_F1',n_jobs=1,error_score='raise')
        with threadpool_limits(2):search.fit(train[FEATURES_H3],train.employment_effect)
        models[name]=search.best_estimator_
        for i,params in enumerate(search.cv_results_['params']):
            cvrows.append({'modelo':name,'parametros':json.dumps(params),'macro_F1_CV':search.cv_results_['mean_test_macro_F1'][i],
                'sd_macro_F1_CV':search.cv_results_['std_test_macro_F1'][i],
                'F1_empleo_CV':search.cv_results_['mean_test_F1_empleo'][i], 'elegido_familia':i==search.best_index_})
        print(name,'macro-F1 CV',search.best_score_,flush=True)
    cvtable=save_table('h3_modelos_cv',pd.DataFrame(cvrows))
    chosen=cvtable.loc[cvtable.elegido_familia].sort_values(['macro_F1_CV','modelo'],ascending=[False,True]).iloc[0].modelo
    models['Mayoritaria']=DummyClassifier(strategy='most_frequent').fit(train[FEATURES_H3],train.employment_effect)
    rows=[];preds={}
    for name,m in models.items():
        for part,a in [('train',train),('test',test)]:
            with threadpool_limits(2):
                pr=m.predict_proba(a[FEATURES_H3]);pred=m.classes_[pr.argmax(axis=1)]
            rows.append(class_metrics(name,part,a.employment_effect,pred,pr,m.classes_))
            if part=='test':preds[name]=pred
    table=save_table('h3_modelos',pd.DataFrame(rows))
    mats=[]
    for name,pred in preds.items():
        cm=confusion_matrix(test.employment_effect,pred,labels=CLASSES)
        for i,true in enumerate(CLASSES):
            for j,guess in enumerate(CLASSES):mats.append({'modelo':name,'real':true,'predicha':guess,'n':int(cm[i,j])})
    save_table('h3_matrices',pd.DataFrame(mats))
    # Incertidumbre descriptiva con remuestreo por empresa en el mismo test.
    groups=test.company_id.to_numpy();ids=np.unique(groups);rng=np.random.default_rng(SEED)
    other='RF base' if chosen!='RF base' else 'Logit lineal'
    deltas=[]
    for _ in range(200):
        counts=pd.Series(rng.choice(ids,len(ids),replace=True)).value_counts()
        weights=pd.Series(groups).map(counts).fillna(0).to_numpy()
        deltas.append(f1_score(test.employment_effect,preds[chosen],labels=CLASSES,average='macro',sample_weight=weights,zero_division=0)
            -f1_score(test.employment_effect,preds[other],labels=CLASSES,average='macro',sample_weight=weights,zero_division=0))
    ci=save_table('h3_bootstrap_empresas',pd.DataFrame([{'modelo':chosen,'comparador':other,'replicas':200,
        'delta_macro_F1':table.query('conjunto=="test"').set_index('modelo').loc[chosen,'macro_F1']-table.query('conjunto=="test"').set_index('modelo').loc[other,'macro_F1'],
        'ci_2_5':np.quantile(deltas,.025),'ci_97_5':np.quantile(deltas,.975)}]))
    # Alternativas de target: reentrenar la misma especificación elegida, sin volver a seleccionar con test.
    alt=[]
    for label,target,binary in [('Banda ±0.5%', 'employment_band',False),('Sin neutral','employment_effect',True)]:
        tr=train.loc[train[target].notna()].copy();te=test.loc[test[target].notna()].copy()
        if binary:tr=tr.loc[tr[target].ne('neutral')];te=te.loc[te[target].ne('neutral')]
        m=clone(models[chosen])
        with threadpool_limits(2):m.fit(tr[FEATURES_H3],tr[target]);pred=m.predict(te[FEATURES_H3])
        labels=CLASSES[1:] if binary else CLASSES
        alt.append({'target':label,'modelo':chosen,'n_train':len(tr),'n_test':len(te),
            'macro_F1':f1_score(te[target],pred,labels=labels,average='macro',zero_division=0),
            'accuracy':accuracy_score(te[target],pred), 'nota':'Tareas distintas, F1 no comparable directamente'})
    return {'tabla':table,'cv':cvtable,'elegido':chosen,'bootstrap':ci,
        'alternativas':save_table('h3_targets_alternativos',pd.DataFrame(alt))}

def temporal_panel():
    """Preparación histórica: ninguna recuperación con respuestas del futuro."""
    raw=pd.read_csv(ROOT/'data/raw/ai_company_adoption.csv')
    raw['period_index']=period(raw)
    raw=raw.dropna(subset=['company_id','period_index']).copy()
    raw.period_index=raw.period_index.astype(int)
    raw=raw.sort_values(['company_id','period_index'])
    for c in ['industry','company_size','country']:
        raw[c]=raw.groupby('company_id')[c].ffill()
    # Reglas de dominio predefinidas; sin detectar bandas con información de test.
    for c in ['ai_investment_per_employee','annual_revenue_usd_millions']:
        raw.loc[raw[c].lt(0),c]=np.nan
    raw.loc[~raw.ai_adoption_rate.between(0,100),'ai_adoption_rate']=np.nan
    country=pd.read_csv(ROOT/'data/raw/country_ai_index.csv')
    raw=raw.drop(columns=[c for c in country if c!='country' and c in raw])
    raw=raw.merge(country,on='country',how='left',validate='many_to_one')
    assert not raw.duplicated(['company_id','period_index']).any()
    return targets(raw)

def make_exact_lags(d,features):
    past=d[['company_id','period_index']+features].copy()
    past['period_origen']=past.period_index
    past.period_index=past.period_index+1
    past=past.rename(columns={c:c+'_lag1' for c in features})
    out=d.merge(past,on=['company_id','period_index'],how='inner',validate='one_to_one')
    assert (out.period_index-out.period_origen).eq(1).all()
    return out

def temporal_validation():
    d=temporal_panel(); rows=[];counts=[]
    # Test fijado por año del RESULTADO, no por posición de fila ni por origen del rezago.
    for horizon in ['Mismo trimestre','Rezago exacto t-1']:
        for hypothesis,target,features in [('H1','productivity_change_percent',FEATURES_H1),('H3','employment_effect',FEATURES_H3)]:
            if horizon.startswith('Rezago'):
                work=make_exact_lags(d,features)
                X=work[[c+'_lag1' for c in features]].copy();X.columns=features
            else:work=d.copy();X=work[features]
            good=work[target].notna()
            work=work.loc[good];X=X.loc[good]
            masks={'train':work.survey_year.isin([2023,2024]),'validacion':work.survey_year.eq(2025),'test':work.survey_year.eq(2026)}
            parts={k:(X.loc[m],work.loc[m,target]) for k,m in masks.items()}
            assert work.loc[masks['train'],'period_index'].max()<work.loc[masks['validacion'],'period_index'].min()
            assert work.loc[masks['validacion'],'period_index'].max()<work.loc[masks['test'],'period_index'].min()
            for k,m in masks.items():
                counts.append({'hipotesis':hypothesis,'horizonte':horizon,'conjunto':k,'n':int(m.sum()),
                    'empresas':work.loc[m,'company_id'].nunique(),'periodo_min':work.loc[m,'period_index'].min(),
                    'periodo_max':work.loc[m,'period_index'].max()})
            if hypothesis=='H1':
                estimators=[Ridge(alpha=v) for v in [1.,10.,100.]]
                loss=lambda y,p:mean_absolute_error(y,p)
                baseline=DummyRegressor()
            else:
                estimators=[LogisticRegression(C=v,max_iter=1500) for v in [.1,1.,10.]]
                loss=lambda y,p:-f1_score(y,p,labels=CLASSES,average='macro',zero_division=0)
                baseline=DummyClassifier(strategy='most_frequent')
            fits=[]
            for estimator in estimators:
                m=pipeline(features,estimator)
                with threadpool_limits(2):m.fit(*parts['train']);pred=m.predict(parts['validacion'][0])
                fits.append((loss(parts['validacion'][1],pred),m))
            _,chosen=min(fits,key=lambda v:v[0])
            # Se conserva train 2023–24; 2025 solo selecciona. No se reajusta con test.
            baseline.fit(*parts['train'])
            for name,m in [('Modelo',chosen),('Referencia train',baseline)]:
                for part in ['validacion','test']:
                    x,y=parts[part]
                    with threadpool_limits(2):pred=m.predict(x)
                    row={'hipotesis':hypothesis,'horizonte':horizon,'modelo':name,'conjunto':part,'n':len(y)}
                    if hypothesis=='H1':row.update(R2=r2_score(y,pred),MAE=mean_absolute_error(y,pred),RMSE=np.sqrt(mean_squared_error(y,pred)))
                    else:row.update(class_metrics(name,part,y,pred))
                    rows.append(row)
            print('Temporal',hypothesis,horizon,'completo',flush=True)
    # Demostración determinista del hueco: t=0 y t=2 no son consecutivos.
    toy=pd.DataFrame({'company_id':['a','a','b','b'],'period_index':[0,2,0,1],'x':[1,2,3,4]})
    toy_lag=make_exact_lags(toy,['x'])
    assert toy_lag.company_id.tolist()==['b']
    return {'tabla':save_table('validacion_temporal',pd.DataFrame(rows)),
        'particiones':save_table('particiones_temporales',pd.DataFrame(counts)),
        'total_filas_panel':len(d),'pares_consecutivos':len(make_exact_lags(d,FEATURES_H3))}

def eda_quartiles():
    d=pd.read_csv(ROOT/'data/raw/company_limpio.csv')
    # Corte fijo del EDA, explícito. Mismo conjunto para adopción e inversión.
    a=d.loc[d.survey_year.eq(2026)&d.quarter.eq('Q2')].dropna(subset=[
        'ai_adoption_rate','ai_investment_per_employee','productivity_change_percent']).copy()
    assert not a.company_id.duplicated().any()
    rows=[]
    for col in ['ai_adoption_rate','ai_investment_per_employee']:
        q=pd.qcut(a[col],4,labels=['Q1','Q2','Q3','Q4'])
        for quart,idx in a.groupby(q,observed=True).groups.items():
            values=a.loc[idx,'productivity_change_percent']
            rows.append({'variable':col,'cuartil':quart,'n':len(values),
                'pct_productividad_mayor_20':100*values.gt(20).mean(),'periodo':'2026 Q2'})
    return save_table('eda_cuartiles',pd.DataFrame(rows))

def manifest():
    import sklearn,linearmodels,statsmodels
    versions={x.__name__:x.__version__ for x in [np,pd,sklearn,linearmodels,statsmodels]}
    # Git puede cambiar CRLF/LF al clonar en otro sistema; normalizar no altera los valores CSV.
    files={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in (ROOT/'data/raw').glob('*.csv')}
    data={'python':sys.version,'platform':platform.platform(),'versiones':versions,'sha256':files,'sha256_normalizacion':'lf','seed':SEED,
        'alcance':'Reanálisis exploratorio tras feedback; los datos de test históricos ya fueron consultados. No es una confirmación independiente.'}
    (RESULTS/'manifest.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf8')
    return data
