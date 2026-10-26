"""Recalculate retrospective metrics from the supplied model prediction export.

This does not retrain models or verify forecast-time availability of input features.
"""
from pathlib import Path
import json

def calculate(csv_path):
    import pandas as pd
    d=pd.read_csv(csv_path)
    target='ACTUAL_DEMAND_MWH'; external='ERCOT_DAY_AHEAD'
    models=['ERCOT_DAY_AHEAD','HYBRID_50_50','WEATHER_XGBOOST','XGBOOST','ROLLING_SARIMA','WEATHER_SARIMAX','SEASONAL_NAIVE','PROPHET']
    required=['TIMESTAMP',target]+models
    missing=[c for c in required if c not in d.columns]
    if missing:raise ValueError(f'Missing required columns: {missing}')
    times=pd.to_datetime(d['TIMESTAMP'],utc=True)
    if times.isna().any() or times.duplicated().any():raise ValueError('Invalid or duplicated test timestamps')
    d=d.copy()
    for col in [target]+models:d[col]=pd.to_numeric(d[col],errors='raise')
    shared=d.dropna(subset=[external]+models+[target]).copy()
    if not len(shared):raise ValueError('No matched rows')
    threshold=d[target].quantile(.99)
    peaks=shared[shared[target]>=threshold]
    def values(x):
        return {c:{'MAE_MWh':round(float((x[c]-x[target]).abs().mean()),3),
                   'MAPE_percent':round(float(((x[c]-x[target]).abs()/x[target]).mean()*100),4),
                   'signed_bias_MWh':round(float((x[c]-x[target]).mean()),3)} for c in models}
    model_values=values(shared); peak_values=values(peaks)
    hy_diff=((d['ROLLING_SARIMA']+d['WEATHER_XGBOOST'])/2-d['HYBRID_50_50']).abs().max()
    out={'source_file':Path(csv_path).name,'data_kind':'recalculated from hourly model predictions','units':'MWh; error calculated as forecast - actual',
         'test_hours':len(d),'matched_hours':len(shared),'missing_ercot_hours':int(d[external].isna().sum()),
         'top_1pct_threshold_all_test_hours_MWh':round(float(threshold),3),'top_1pct_matched_hours':len(peaks),
         'overall':model_values,'top_1pct':peak_values,
         'hybrid_max_abs_formula_difference_MWh':float(hy_diff),
         'hybrid_MAE_improvement_over_naive_percent':round(100*(1-model_values['HYBRID_50_50']['MAE_MWh']/model_values['SEASONAL_NAIVE']['MAE_MWh']),3),
         'top_1pct_xgboost_underforecast_counts':{c:int((peaks[c]<peaks[target]).sum()) for c in ['XGBOOST','WEATHER_XGBOOST']}}
    return out


def save(csv_path,outfile):
    result=calculate(csv_path)
    Path(outfile).write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    return result
