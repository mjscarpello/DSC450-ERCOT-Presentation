"""Deterministic local research calculations and asset provenance. No model fitting or network."""

from pathlib import Path

import json, hashlib, shutil, re, sys, textwrap

import numpy as np

import pandas as pd

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

import matplotlib.dates as mdates

from matplotlib.patches import Rectangle

from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]

OUT=ROOT/'figures/storyboard'

TOK=json.loads((ROOT/'design/tokens.json').read_text())

MODELS=['ERCOT_DAY_AHEAD','SEASONAL_NAIVE','ROLLING_SARIMA','PROPHET','XGBOOST','WEATHER_SARIMAX','WEATHER_XGBOOST','HYBRID_50_50']

NAMES={'ACTUAL_DEMAND_MWH':'Observed demand','ERCOT_DAY_AHEAD':'ERCOT day-ahead','SEASONAL_NAIVE':'Seasonal naive','ROLLING_SARIMA':'Rolling SARIMA','PROPHET':'Prophet','XGBOOST':'Original XGBoost','WEATHER_SARIMAX':'Weather SARIMAX','WEATHER_XGBOOST':'Weather XGBoost','HYBRID_50_50':'50/50 hybrid'}

LIMIT='Retrospective supplied predictions. Equal target hours do not establish equal forecast issue times, horizons or advance-available inputs. Observed weather is not an operational weather forecast. Observed-load groups are selected afterward. No costs, reserves or outages were measured. No independent raw-EIA snapshot authentication or model leakage audit is available.'

def write(p,d):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def initialize():
 np.random.seed(0)
 for n in ['figures','generated','highlights']: (OUT/n).mkdir(parents=True,exist_ok=True)
 (ROOT/'outputs/evidence/tables').mkdir(parents=True,exist_ok=True)
 plt.rcParams.update({'font.family':TOK['font'],'font.size':14,'axes.titlesize':18,'axes.titleweight':'bold','axes.labelsize':15,'legend.fontsize':13,'axes.spines.top':False,'axes.spines.right':False,'axes.axisbelow':True,'svg.hashsalt':'ERCOT-M2','savefig.facecolor':'white'})
 return {'purpose':'Before the Load Arrives, Milestone 2','seed':0,'limitations':LIMIT,'environment':{'python':sys.version.split()[0],'numpy':np.__version__,'pandas':pd.__version__,'matplotlib':matplotlib.__version__},'asset_id_policy':'Original F/D/W/MAP immutable; regenerated R11P/R12P retain editorial IDs with new hashes and archived prior versions; G_ IDs are conceptual.'}

def load_inputs():
 base=ROOT/'data'
 a=pd.read_csv(base/'eia930_erco_cleaned.csv'); p=pd.read_csv(base/'ercot_model_predicitons_comparison_with_hybrid.csv')
 assert set(['period_utc','demand_mwh','hour','season','demand_lag_24','demand_lag_168']).issubset(a), 'Historical input schema changed'
 assert set(['TIMESTAMP','ACTUAL_DEMAND_MWH']+MODELS).issubset(p), 'Prediction input schema changed'
 a['utc']=pd.to_datetime(a.period_utc,utc=True,errors='raise');p['utc']=pd.to_datetime(p.TIMESTAMP,utc=True,errors='raise')
 for d in [a,p]:
  assert d.utc.is_unique,'Duplicate UTC key'; assert d.utc.is_monotonic_increasing,'Input must be chronological';d['local']=d.utc.dt.tz_convert('America/Chicago')
 schema={'historical':{'original_columns':[c for c in a if c not in ['utc','local']],'key':'period_utc','demand':'demand_mwh'},'predictions':{'original_columns':[c for c in p if c not in ['utc','local']],'key':'TIMESTAMP','demand':'ACTUAL_DEMAND_MWH'},'derived':{'signed_error':'forecast − ACTUAL_DEMAND_MWH','absolute_error':'abs(signed_error)','MAE':'mean(absolute_error) on exact matched rows','bias':'mean(signed_error)','hybrid':'(ROLLING_SARIMA + WEATHER_XGBOOST)/2','load_groups':'pd.cut(actual, [-inf,q50,q90,q95,q99,inf], right=True); percentiles from ALL 8760 actuals','highest_1pct':'actual >= quantile(.99) from all holdout actuals','UTC':'pd.to_datetime(..., utc=True)','Central':'utc.dt.tz_convert(America/Chicago)'}}
 write(ROOT/'outputs/evidence/INPUT_SCHEMA.json',schema)
 return a,p

def reconcile(a,p):
 assert len(a)==41616 and len(p)==8760,'Unexpected source spans'
 assert a.utc.min()==pd.Timestamp('2022-01-01',tz='UTC') and a.utc.max()==pd.Timestamp('2026-09-30 23:00',tz='UTC')
 assert p.utc.min()==pd.Timestamp('2025-10-01',tz='UTC') and p.utc.max()==pd.Timestamp('2026-09-30 23:00',tz='UTC')
 assert (a.utc.diff().dropna()==pd.Timedelta(hours=1)).all() and (p.utc.diff().dropna()==pd.Timedelta(hours=1)).all()
 assert a.demand_mwh.notna().all() and (a.demand_mwh>0).all()
 assert a.was_missing_hour.sum()==0 and a.demand_imputed.sum()==0
 np.testing.assert_allclose(a.set_index('utc').loc[p.utc].demand_mwh,p.ACTUAL_DEMAND_MWH,atol=0,rtol=0)
 np.testing.assert_allclose(a.set_index('utc').loc[p.utc].demand_forecast_mwh,p.ERCOT_DAY_AHEAD,atol=0,rtol=0,equal_nan=True)
 np.testing.assert_allclose(p.HYBRID_50_50,(p.ROLLING_SARIMA+p.WEATHER_XGBOOST)/2,atol=1e-8,rtol=0)
 m=p.dropna(subset=['ACTUAL_DEMAND_MWH']+MODELS).copy();assert len(m)==8640 and p.ERCOT_DAY_AHEAD.isna().sum()==120
 err=m[MODELS].sub(m.ACTUAL_DEMAND_MWH,axis=0);mae=err.abs().mean();bias=err.mean();q=p.ACTUAL_DEMAND_MWH.quantile([.5,.9,.95,.99]);cut=q.loc[.99]
 assert abs(cut-87965.69)<1e-7
 labels=['Bottom 50%','50–90%','90–95%','95–99%','Top 1%'];m['group']=pd.cut(m.ACTUAL_DEMAND_MWH,[-np.inf,*q.tolist(),np.inf],labels=labels)
 top=m.ACTUAL_DEMAND_MWH>=cut;assert top.sum()==88
 assert (m['group']=='Top 1%').equals(top),'Boundary ambiguity in load grouping'
 for k,v in {'ERCOT_DAY_AHEAD':1135,'HYBRID_50_50':2006,'WEATHER_XGBOOST':2477,'ROLLING_SARIMA':2662,'SEASONAL_NAIVE':4205}.items():assert round(mae[k])==v,(k,mae[k])
 peak=err.loc[top].abs().mean()
 for k,v in {'ERCOT_DAY_AHEAD':1158,'WEATHER_SARIMAX':1176,'ROLLING_SARIMA':1242,'HYBRID_50_50':3189,'WEATHER_XGBOOST':6421}.items():assert round(peak[k])==v
 opposite=int(((err.ROLLING_SARIMA*err.WEATHER_XGBOOST)<0).sum());assert opposite==4022
 months=m.loc[top,'local'].dt.month.value_counts().sort_index().to_dict();hours=m.loc[top,'local'].dt.hour.value_counts().sort_index().to_dict()
 assert months=={7:24,8:64} and hours=={15:10,16:17,17:21,18:23,19:14,20:3}
 for k in ['HYBRID_50_50','XGBOOST','WEATHER_XGBOOST']:assert (err.loc[top,k]<0).sum()==88
 row=p.loc[p.utc==pd.Timestamp('2026-07-22 21:00',tz='UTC')].iloc[0]
 for k,v in {'ACTUAL_DEMAND_MWH':90402,'ROLLING_SARIMA':88883,'WEATHER_XGBOOST':78913,'HYBRID_50_50':83898}.items():assert round(row[k])==v
 miss=row.ACTUAL_DEMAND_MWH-row.HYBRID_50_50;assert round(miss)==6504
 # Existing historical lag features checked against elapsed-hour definitions.
 np.testing.assert_allclose(a.demand_lag_24,a.demand_mwh.shift(24),equal_nan=True)
 np.testing.assert_allclose(a.demand_lag_168,a.demand_mwh.shift(168),equal_nan=True)
 hist=a.set_index('utc').demand_mwh
 np.testing.assert_allclose(p.SEASONAL_NAIVE,hist.reindex(pd.DatetimeIndex(p.utc)-pd.Timedelta(hours=168)).values,atol=0,rtol=0)
 # Original 24-hour moving average includes shift(24), not a claim about live predictor availability.
 roll_matches=[]
 for shift in [0,1,24]:
  for minp in [1,24]:
   if np.allclose(a.demand_roll_mean_24,a.demand_mwh.shift(shift).rolling(24,min_periods=minp).mean(),equal_nan=True):roll_matches.append({'shift_hours':shift,'window_hours':24,'min_periods':minp})
 summary={'status':'pass','historical_hours':len(a),'holdout_hours':len(p),'matched_hours':len(m),'historical_span_utc':[str(a.utc.min()),str(a.utc.max())],'missing_by_original_column':a.drop(columns=['utc','local']).isna().sum().astype(int).to_dict(),'overall_mae':mae.to_dict(),'signed_bias':bias.to_dict(),'high_load_mae':peak.to_dict(),'load_cutoffs_mwh':{str(k):v for k,v in q.items()},'load_group_counts':m.groupby('group',observed=True).size().astype(int).to_dict(),'opposite_sign_hours':opposite,'signed_error_correlation':float(err.ROLLING_SARIMA.corr(err.WEATHER_XGBOOST)),'high_load_month_counts':{str(k):v for k,v in months.items()},'high_load_hour_counts':{str(k):v for k,v in hours.items()},'hybrid_max_arithmetic_difference':float(abs(p.HYBRID_50_50-(p.ROLLING_SARIMA+p.WEATHER_XGBOOST)/2).max()),'hybrid_reduction_vs_naive_pct':100*(1-mae.HYBRID_50_50/mae.SEASONAL_NAIVE),'july_case':{k:float(row[k]) for k in ['ACTUAL_DEMAND_MWH']+MODELS},'july_case_utc':str(row.utc),'july_case_local':str(row.local),'july_hybrid_underforecast':float(miss),'rolling_mean_reconciliation':roll_matches,'source_limitations':LIMIT}
 write(ROOT/'outputs/evidence/DATA_RECONCILIATION.json',summary)
 pd.DataFrame({'mae_mwh':mae,'signed_bias_mwh':bias,'high_load_mae_mwh':peak}).to_csv(ROOT/'outputs/evidence/tables/model_metrics.csv',float_format='%.10f')
 p.to_csv(ROOT/'outputs/evidence/tables/normalized_predictions.csv',index=False,float_format='%.10f')
 hourly=err.abs().assign(local_hour=m.local.dt.hour).groupby('local_hour').mean();hourly.to_csv(ROOT/'outputs/evidence/tables/hourly_mae.csv',float_format='%.10f')
 # Independent plotted-source tables for every empirical original used at runtime.
 assert (a.hour==a.local.dt.hour).all(), 'Stored local-hour feature disagrees with UTC conversion'
 historical=a.copy();historical['local_hour']=historical.local.dt.hour;historical['local_month']=historical.local.dt.month;historical['weekend']=historical.local.dt.dayofweek>=5
 historical.groupby(['local_month','local_hour']).demand_mwh.mean().unstack().to_csv(ROOT/'outputs/evidence/tables/F03_month_hour_mean_mwh.csv',float_format='%.10f')
 historical.groupby(['season','local_hour']).demand_mwh.mean().unstack().to_csv(ROOT/'outputs/evidence/tables/F04_season_hour_mean_mwh.csv',float_format='%.10f')
 historical.groupby(['weekend','local_hour']).demand_mwh.mean().unstack().to_csv(ROOT/'outputs/evidence/tables/F05_weekend_hour_mean_mwh.csv',float_format='%.10f')
 historical.assign(abs_change=historical.demand_mwh.diff().abs()).groupby('local_hour').abs_change.mean().to_csv(ROOT/'outputs/evidence/tables/F08_hourly_absolute_change_mwh.csv',float_format='%.10f')
 week=p[(p.local>=pd.Timestamp('2026-07-19',tz='America/Chicago'))&(p.local<pd.Timestamp('2026-07-26',tz='America/Chicago'))]
 week.to_csv(ROOT/'outputs/evidence/tables/F09_F10_F16_July_week.csv',index=False,float_format='%.10f')
 err[['ROLLING_SARIMA','WEATHER_XGBOOST']].assign(utc=m.utc.values,opposite_sign=(err.ROLLING_SARIMA*err.WEATHER_XGBOOST)<0).to_csv(ROOT/'outputs/evidence/tables/F20_paired_signed_errors.csv',index=False,float_format='%.10f')
 m.loc[top].to_csv(ROOT/'outputs/evidence/tables/D08_selected_88_hours.csv',index=False,float_format='%.10f')
 row.to_frame('value').to_csv(ROOT/'outputs/evidence/tables/D05_exact_hour.csv')

 return {'actual':a,'pred':p,'matched':m,'error':err,'summary':summary,'labels':labels,'cutoffs':q,'hourly':hourly}

def savefig(fig,aid,title,alt,sources,checks):
 dest=OUT/'generated'/f'{aid}.png';fig.savefig(dest,dpi=150,metadata={'Software':'ERCOT Milestone 2'})
 fig.savefig(dest.with_suffix('.svg'),metadata={'Date':None,'Creator':'ERCOT Milestone 2'})
 plt.close(fig)
 with Image.open(dest) as im:w,h=im.size
 return {'asset_id':aid,'kind':'derived_from_csv','path':str(dest.relative_to(ROOT)),'vector_path':str(dest.with_suffix('.svg').relative_to(ROOT)),'source_path':sources,'source_calculation':checks,'figure_title':title,'alt_text':alt,'width':w,'height':h,'sha256':sha(dest),'numerical_checks':'pass','explanation':alt,'limitations':LIMIT,'scene_ids':[],'cue_ids':[]}

def empirical(state):
 p,m,e=state['pred'],state['matched'],state['error'];rows=[]
 week=p[(p.local>=pd.Timestamp('2026-07-19',tz='America/Chicago'))&(p.local<pd.Timestamp('2026-07-26',tz='America/Chicago'))];assert len(week)==168
 fig,ax=plt.subplots(figsize=(12.8,6.0));fig.subplots_adjust(left=.09,right=.98,bottom=.19,top=.80)
 cols=['ACTUAL_DEMAND_MWH','ROLLING_SARIMA','WEATHER_XGBOOST'];assert 'HYBRID_50_50' not in cols
 for c in cols:ax.plot(week.local,week[c]/1000,color=TOK['colors'][c],label=NAMES[c],lw=2.2)
 ax.set(ylabel='Thousand MWh per hourly interval',xlabel='Central local date (CDT)',title='')
 ax.xaxis.set_major_locator(mdates.DayLocator(tz=week.local.dt.tz));ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d',tz=week.local.dt.tz));ax.grid(axis='y',color=TOK['grid']);ax.legend(loc='lower left',bbox_to_anchor=(0,1.02),ncol=3,frameon=False)
 fig.suptitle('Original forecasts and observed demand, July 19–25, 2026', y=.97, fontsize=18, weight='bold')
 fig.text(.09,.025,'R11P   Supplied hourly predictions. Historical comparison; forecast issuance conditions differ.',fontsize=12,color=TOK['muted'])
 week[['utc','local']+cols].to_csv(ROOT/'outputs/evidence/tables/R11P_plot_data.csv',index=False,float_format='%.10f')
 rows.append(savefig(fig,'R11P','Original forecasts and observed demand','Observed demand, rolling SARIMA and Weather XGBoost traces over all 168 July-week hours, without hybrid.','source/inputs/data/ercot_model_predicitons_comparison_with_hybrid.csv','Select [July19 00:00,July26 00:00) America/Chicago; values /1000. 168 rows. No hybrid line or legend.'))
 focus=['ERCOT_DAY_AHEAD','ROLLING_SARIMA','WEATHER_XGBOOST'];counts=m.groupby('group',observed=True).size().reindex(state['labels']);grouped=e.abs().assign(group=m.group).groupby('group',observed=True)[focus].mean().reindex(state['labels']);grouped.to_csv(ROOT/'outputs/evidence/tables/R12P_plot_data.csv',float_format='%.10f')
 fig,ax=plt.subplots(figsize=(12.8,6));fig.subplots_adjust(left=.09,right=.98,bottom=.23,top=.80);x=np.arange(5);width=.24
 for j,c in enumerate(focus):ax.bar(x+(j-1)*width,grouped[c],width,color=TOK['colors'][c],label=NAMES[c])
 ax.set_xticks(x,[f'{v}\n(n={counts[v]:,})' for v in state['labels']]);ax.set(ylabel='MAE (MWh, lower is better)',title='');ax.grid(axis='y',color=TOK['grid']);ax.legend(loc='lower left',bbox_to_anchor=(0,1.02),ncol=3,frameon=False)
 fig.suptitle('Original methods across observed-demand groups', y=.97, fontsize=18, weight='bold')
 fig.text(.09,.065,'R12P   Cutoffs from all 8,760 actuals; errors on 8,640 matched hours. Top 1%: 88 hours.',fontsize=12,color=TOK['muted']);fig.text(.09,.025,'Retrospective groups selected using demand measured afterward. These are not predicted alerts.',fontsize=12,color=TOK['muted'])
 fig.canvas.draw()
 def norm_region(x0,x1):
  lo=ax.transData.transform((x0,0));hi=ax.transData.transform((x1,ax.get_ylim()[1]));fw,fh=fig.canvas.get_width_height();return [float(lo[0]/fw),float(1-hi[1]/fh),float((hi[0]-lo[0])/fw),float((hi[1]-lo[1])/fh)]
 write(ROOT/'outputs/new_plot_geometry.json',{'R12P':{'ordinary_groups':norm_region(-.40,.40),'top_group':norm_region(3.60,4.40),'provenance':'Exact matplotlib transData bounds after final layout, normalized to complete exported image'}})
 rows.append(savefig(fig,'R12P','Original methods across observed-demand groups','Three pre-combination methods. Rolling SARIMA has much lower error at the highest observed loads.','source/inputs/data/ercot_model_predicitons_comparison_with_hybrid.csv','Observed actual quantiles [.50,.90,.95,.99] from all holdout; common-row mean abs(forecast−actual). 88 top hours. No hybrid.'))
 return rows

def qa_assets(rows):
 results=[]
 for r in rows:
  p=ROOT/r['path']
  with Image.open(p) as im:
   assert im.size==(r['width'],r['height']),(r['asset_id'],im.size,r['width'],r['height'])
   assert np.asarray(im.convert('RGB')).std()>3,'Blank image '+r['asset_id']
  assert r['figure_title'] and r['alt_text'] and r['sha256'];results.append({'asset_id':r['asset_id'],'status':'pass','pixel_dimensions':[r['width'],r['height']]})
 # New assets only: contacts accompany detailed native cue screenshots.
 new=[r for r in rows if r['kind']!='original_notebook'];thumbs=[]
 for r in new:
  im=Image.open(ROOT/r['path']).convert('RGB');im.thumbnail((440,270));tile=Image.new('RGB',(464,308),'#E7EDF2');tile.paste(im,((464-im.width)//2,25));ImageDraw.Draw(tile).text((10,7),r['asset_id'],fill='#19344A');thumbs.append(tile)
 for batch in range((len(thumbs)+11)//12):
  part=thumbs[batch*12:(batch+1)*12];sheet=Image.new('RGB',(464*3,308*((len(part)+2)//3)),'white')
  for i,im in enumerate(part):sheet.paste(im,((i%3)*464,(i//3)*308))
  sheet.save(ROOT/f'outputs/evidence/new_assets_contact_{batch+1:02}.jpg')
 write(ROOT/'outputs/evidence/ASSET_QA.json',results)
 return results

if __name__ == "__main__":
 initialize()
 a,p=load_inputs()
 state=reconcile(a,p)
 rows=empirical(state)
 qa_assets(rows)
 print("PASS: frozen predictions reconciled; two research charts regenerated.")
