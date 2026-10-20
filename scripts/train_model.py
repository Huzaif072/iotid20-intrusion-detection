"""Reproducible *deployable baseline*, NOT the paper CNN-GRU-attention model.
Run on the downloaded IoTID20 raw CSV(s). Retains train-fitted imputation,
encoding, ANOVA selection (up to 70), scaling, and classifier in one pipeline.
"""
import argparse
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
ROOT=Path(__file__).resolve().parents[1]
TARGETS={'label','cat','sub_cat'}
# Columns unsuitable as predictors. Prefer original numeric/categorical features.
# Source CSV column names preserved for input schema and Angular form.

def load_csvs(folder):
 paths=sorted(folder.rglob('*.csv'))
 if not paths: raise FileNotFoundError(f'No CSV in {folder}; run scripts/download_dataset.py first')
 frames=[]
 for path in paths:
  df=pd.read_csv(path,low_memory=False)
  df.columns=[str(c).strip() for c in df.columns]
  if any(c.casefold()=='label' for c in df.columns):
   frames.append(df)
 if not frames: raise ValueError('No IoTID20 CSV with Label column detected')
 # Avoid joining unrelated / duplicate CSV copies (multiple versions).
 if len(frames)>1: print('NOTICE: multiple labelled files detected, using largest:',max(len(x) for x in frames))
 return max(frames,key=len)

def clean(df):
 targets=[c for c in df if c.casefold() in TARGETS]
 target=next((c for c in df if c.casefold()=='label'),None)
 if target is None: raise ValueError('Missing Label')
 df=df.replace([np.inf,-np.inf],np.nan).dropna(subset=[target]).copy()
 features=[c for c in df if c not in targets]
 X=df[features].copy()
 # Remove obvious completely-null columns, preserving valid input columns.
 X=X.dropna(axis=1,how='all')
 for col in X:
  if X[col].dtype=='object':
   parsed=pd.to_numeric(X[col],errors='coerce')
   if parsed.notna().mean()>.98: X[col]=parsed
 y=df[target].astype(str).str.strip()
 return X,y

def main():
 p=argparse.ArgumentParser();p.add_argument('--data-dir',default=str(ROOT/'data'/'raw'))
 p.add_argument('--max-rows',type=int,default=None,help='Debug only: do NOT use for paper comparisons')
 a=p.parse_args();df=load_csvs(Path(a.data_dir))
 if a.max_rows: df=df.sample(n=min(len(df),a.max_rows),random_state=42)
 X,y=clean(df); enc=LabelEncoder(); y_enc=enc.fit_transform(y)
 if len(enc.classes_)!=2: raise ValueError(f'Expected binary label; labels found: {list(enc.classes_)}')
 numeric=X.select_dtypes(include='number').columns.tolist()
 categorical=[c for c in X if c not in numeric]
 num=Pipeline([('imputer',SimpleImputer(strategy='median')),('scale',StandardScaler())])
 cat=Pipeline([('imputer',SimpleImputer(strategy='most_frequent')),('onehot',OneHotEncoder(handle_unknown='ignore',sparse_output=True))])
 preprocess=ColumnTransformer([('numeric',num,numeric),('categorical',cat,categorical)],sparse_threshold=1.0)
 Xtr,Xte,ytr,yte=train_test_split(X,y_enc,test_size=.2,stratify=y_enc,random_state=42)
 # ANOVA k=70 on encoded fields; differs from any undisclosed paper encoding.
 pipe=Pipeline([('preprocess',preprocess),('select',SelectKBest(f_classif,k=70)),
                ('model',RandomForestClassifier(n_estimators=50,max_depth=15,min_samples_leaf=4,max_features="sqrt",n_jobs=2,random_state=42))])
 encoded=preprocess.fit_transform(Xtr)
 k=min(70,encoded.shape[1]); pipe.set_params(select__k=k)
 pipe.fit(Xtr,ytr)
 pred=pipe.predict(Xte)
 metrics={'accuracy':float(accuracy_score(yte,pred)), 'weighted_f1':float(f1_score(yte,pred,average='weighted')),
          'macro_f1':float(f1_score(yte,pred,average='macro')), 'confusion_matrix':confusion_matrix(yte,pred).tolist(),
          'classification_report':classification_report(yte,pred,target_names=[str(c) for c in enc.classes_],output_dict=True),
          'train_size':len(ytr),'test_size':len(yte),'feature_count':len(X.columns),
          'encoded_selected_features':k,'label_classes':enc.classes_.tolist(),
          'model_kind':'RandomForest deployable baseline; NOT reproduced paper CNN-GRU-attention'}
 kinds={c:('number' if c in numeric else 'category') for c in X}
 categories={c:sorted(map(str,X[c].dropna().unique()))[:100] for c in categorical}
 metadata={'pipeline':pipe,'features':list(X.columns),'kinds':kinds,'categories':categories,
           'label_classes':enc.classes_.tolist(),'task':'classification','model_version':'baseline-1.0'}
 (ROOT/'backend'/'models').mkdir(parents=True,exist_ok=True)
 joblib.dump(metadata,ROOT/'backend/models/model_bundle.joblib',compress=3)
 (ROOT/'docs').mkdir(exist_ok=True)
 (ROOT/'docs'/'actual_metrics.json').write_text(json.dumps(metrics,indent=2))
 payload={c:(float(Xte.iloc[0][c]) if c in numeric and pd.notna(Xte.iloc[0][c]) else str(Xte.iloc[0][c]) if pd.notna(Xte.iloc[0][c]) else None) for c in X}
 (ROOT/'backend'/'test_payload.json').write_text(json.dumps(payload,indent=2))
 pd.DataFrame([payload]).to_csv(ROOT/'data'/'sample_inputs.csv',index=False)
 frontend_schema=[{'name':c,'label':c.replace('_',' '),'kind':kinds[c], 'required':True, **({'options':categories[c]} if c in categorical else {})} for c in X]
 (ROOT/'frontend/src/app/feature-schema.json').write_text(json.dumps(frontend_schema,indent=2))
 print(json.dumps({k:v for k,v in metrics.items() if k in ['accuracy','weighted_f1','macro_f1','train_size','test_size','feature_count']},indent=2))
 print('Saved baseline model and exact schema. This DOES NOT reproduce the CNN-GRU paper.')
if __name__=='__main__':main()
