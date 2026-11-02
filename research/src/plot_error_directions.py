from pathlib import Path
import hashlib,json
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import StrMethodFormatter
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'figures/error_directions'
R.mkdir(parents=True,exist_ok=True)
SOURCE=ROOT/'outputs/evidence/tables/F20_paired_signed_errors.csv'
d=pd.read_csv(SOURCE);x=d.ROLLING_SARIMA;y=d.WEATHER_XGBOOST
opposite=(x*y)<0;same=(x*y)>0;zero=(x*y)==0
assert len(d)==8640 and opposite.sum()==4022 and zero.sum()==0
assert np.array_equal(opposite,d.opposite_sign)
blue='#0072B2';gray='#8997A3';ink='#19344A'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':ink,'text.color':ink})
fig,ax=plt.subplots(figsize=(12,9),facecolor='white')
fig.subplots_adjust(left=.12,right=.97,bottom=.19,top=.77)
fig.text(.12,.945,'When one model forecasts high, the other can forecast low',fontsize=21,weight='bold')
fig.text(.12,.902,f'{opposite.sum():,} of {len(d):,} matched hours ({opposite.mean():.1%}) had opposite-sign errors',fontsize=16,color=blue)
ax.scatter(x[same],y[same],s=8,c=gray,alpha=.32,edgecolors='none',rasterized=True)
ax.scatter(x[opposite],y[opposite],s=8,c=blue,alpha=.43,edgecolors='none',rasterized=True)
ax.axvline(0,color='#536779',lw=1);ax.axhline(0,color='#536779',lw=1)
ax.set(xlim=(-24000,26000),ylim=(-25000,15000),xlabel='Rolling SARIMA signed error (MWh)',ylabel='Weather XGBoost signed error (MWh)')
ax.set_aspect('equal',adjustable='box');ax.grid(alpha=.12,zorder=0)
for axis in [ax.xaxis,ax.yaxis]:axis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
for xx,yy,text,color,ha,va in [(.02,.97,'OPPOSITE DIRECTIONS\nSARIMA low / XGBoost high',blue,'left','top'),(.98,.97,'BOTH TOO HIGH',gray,'right','top'),(.02,.03,'BOTH TOO LOW',gray,'left','bottom'),(.98,.03,'OPPOSITE DIRECTIONS\nSARIMA high / XGBoost low',blue,'right','bottom')]:
 ax.text(xx,yy,text,transform=ax.transAxes,ha=ha,va=va,color=color,fontsize=11,weight='bold',bbox=dict(facecolor='white',edgecolor='none',alpha=.92,pad=5))
handles=[Line2D([],[],marker='o',linestyle='',color=blue,label=f'Opposite directions: {opposite.sum():,} hours'),Line2D([],[],marker='o',linestyle='',color=gray,label=f'Same direction: {same.sum():,} hours')]
fig.legend(handles=handles,loc='upper left',bbox_to_anchor=(.12,.87),ncol=2,frameon=False,fontsize=12)
fig.text(.12,.115,'Each dot is one shared hour, combining both models’ errors. Pearson r = '+f'{x.corr(y):.2f}',fontsize=12)
fig.text(.12,.079,'Error = forecast − actual. Positive means too high; negative means too low.',fontsize=12)
fig.text(.12,.043,'Opposite errors can partly offset when averaged; this does not guarantee a correct forecast.',fontsize=11,color='#657889')
fig.savefig(R/'F20_opposite_direction_errors.png',dpi=180)
fig.savefig(R/'F20_opposite_direction_errors.svg')
report={'status':'pass','matched_hours':len(d),'opposite_sign_hours':int(opposite.sum()),'same_sign_hours':int(same.sum()),'zero_error_hours':int(zero.sum()),'opposite_sign_percent':float(opposite.mean()*100),'pearson_r':float(x.corr(y)),'definition':'Forecast minus actual, MWh','classification':'Opposite only when error product < 0; neither model is a color category','source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'scope':'The same 8640 shared-hour sample as the presentation, not the larger model-pair-only sample','project_updated':False}
(R/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
