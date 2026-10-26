"""Build a reproducible, detailed, source-linked research graph.

The stored v1 graph is the reviewed baseline. All new figure nodes and numerical facts
are generated deterministically. This builder never executes or changes the source notebook.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import json,re
from datetime import date
ROOT=Path(__file__).resolve().parents[2]

FIG_FINDINGS={
'F01':['FIND-SEASONAL'],'F02':['FIND-SEASONAL'],'F03':['FIND-SEASONAL'],'F03A':['FIND-SEASONAL'],'F03B':['FIND-SEASONAL'],'F03C':['FIND-SEASONAL'],'F03D':['FIND-SEASONAL'],'F03E':['FIND-SEASONAL'],
'F04':['FIND-SEASONAL'],'F05':['FIND-SEASONAL'],'F06':['FIND-SEASONAL'],'F07':['FIND-SEASONAL'],'F08':['FIND-SEASONAL'],'F09':['FIND-SEASONAL'],
'F10':['FIND-ERCOT','FIND-SUMMER-WEEK'],'F11':['FIND-ERCOT'],'F12':['DEC-ERROR-DIRECTION'],'F13':['FIND-ERCOT-PEAK'],
'F14':['FIND-OVERALL','FIND-ERCOT'],'F15':['FIND-OVERALL','FIND-ERCOT'],'F16':['FIND-SUMMER-WEEK'],'F17':['FIND-PEAK','FIND-UNDER'],
'F18':['FIND-DIVERGENCE'],'F19':['FIND-DIVERGENCE'],'F20':['DEC-COMPLEMENT'],
'F21':['FIND-BLEND-TEST'],'F22':['FIND-BLEND-TEST'],'F23':['FIND-BLEND-TEST'],'F24':['FIND-BLEND-TEST','FIND-SUMMER-WEEK'],'F25':['FIND-BLEND-TEST'],
'F26':['FIND-DIVERGENCE'],'F27':['FIND-DIVERGENCE'],'F28':['FIND-DIVERGENCE'],'F29':['FIND-DIVERGENCE'],'F30':['FIND-DIVERGENCE'],'F31':['FIND-DIVERGENCE'],'F32':['FIND-DIVERGENCE','FIND-OVERALL'],'F33':['FIND-DIVERGENCE','FIND-SUMMER-WEEK']}

FIGURE_TITLES={
 'F01':'Historical monthly demand trend','F02':'January–September demand across years','F03':'Typical demand by month and hour',
 'F03A':'Four-season daily demand heatmaps','F03B':'Fall 2025 daily demand heatmap','F03C':'Winter 2025–26 daily demand heatmap',
 'F03D':'Spring 2026 daily demand heatmap','F03E':'Summer 2026 daily demand heatmap','F04':'Seasonal hourly load profiles',
 'F05':'Weekday versus weekend profiles','F06':'Monthly demand distributions','F07':'Share of peak demand hours by month',
 'F08':'Hourly demand ramping patterns','F09':'July 2026 high-load week','F10':'ERCOT actual versus day-ahead forecast',
 'F11':'ERCOT hourly mean absolute error','F12':'ERCOT monthly MAE and signed bias','F13':'ERCOT errors during top-demand decile',
 'F14':'Eight-model matched-sample MAE leaderboard','F15':'Model accuracy in relative percentage terms',
 'F16':'July week: actual demand versus model predictions','F17':'Forecast error by observed demand category',
 'F18':'Forecast error by Central-local hour','F19':'Forecast error across calendar months',
 'F20':'Paired SARIMA and weather XGBoost signed errors','F21':'Hybrid validation error by blend weight',
 'F22':'Fixed versus earlier-selected hybrid on later period','F23':'Hybrid performance across later-period demand groups',
 'F24':'July peak-week forecast overlay with fixed hybrid','F25':'Frequency with which hybrid reduces absolute error',
 'F26':'Hourly MAE divergence, model comparison A','F27':'Hourly MAE divergence, model comparison B',
 'F28':'Monthly improvement relative to each model’s MAE','F29':'Seasonal improvement relative to each model’s MAE',
 'F30':'Model MAE divergence by month and hour','F31':'Model MAE divergence by season and hour',
 'F32':'Skill relative to naive baseline and ERCOT','F33':'Individual hourly errors during the July peak week'
}

FIG_LIMITATIONS={
'F03':['LIMIT-CAUSAL'],'F03A':['LIMIT-CAUSAL'],'F03B':['LIMIT-CAUSAL'],'F03C':['LIMIT-CAUSAL'],'F03D':['LIMIT-CAUSAL'],'F03E':['LIMIT-CAUSAL'],
'F10':['LIMIT-ORIGIN'],'F13':['LIMIT-PEAK-BIN'],'F14':['LIMIT-ORIGIN','LIMIT-WEATHER'],'F15':['LIMIT-ORIGIN'],
'F17':['LIMIT-PEAK-BIN'],'F20':['LIMIT-ORIGIN'],
'F21':['LIMIT-ORIGIN'],'F22':['LIMIT-ORIGIN'],'F23':['LIMIT-PEAK-BIN'],
'F25':['LIMIT-ORIGIN'],'F26':['LIMIT-ORIGIN'],'F27':['LIMIT-ORIGIN'],'F32':['LIMIT-ORIGIN']}
MODEL_COLUMNS={'ERCOT_DAY_AHEAD':'METHOD-ERCOT','HYBRID_50_50':'METHOD-HYBRID','WEATHER_XGBOOST':'METHOD-WXGB','XGBOOST':'METHOD-XGB','ROLLING_SARIMA':'METHOD-SARIMA','WEATHER_SARIMAX':'METHOD-SARIMAX','SEASONAL_NAIVE':'METHOD-NAIVE','PROPHET':'METHOD-PROPHET'}
SECTION_DETAILS=[
 ('SEC-PROBLEM','Business problem and hypothesis','Report page 3: why advance hourly electricity-demand forecasts matter, what is compared and the original hypothesis.',3,['GOAL-RESEARCH','GOAL-BUSINESS']),
 ('SEC-DATA','Data preparation and feature design','Report page 4: 41,616 consecutive UTC observations, validity checks, calendar and weather features.',4,['DATA-HISTORY','DATA-FEATURES','DATA-WEATHER']),
 ('SEC-MODELS','Modeling approaches','Report page 5: chronological holdout, naive, rolling SARIMA, Prophet, XGBoost and weather additions.',5,['DEC-ROLL','METHOD-SARIMA','METHOD-WXGB']),
 ('SEC-RESULTS','Matched-sample forecasting results','Report pages 5–6: eight-method MAE leaderboard and official hybrid comparison.',5,['FIND-OVERALL','FIND-ERCOT']),
 ('SEC-BEHAVIOR','Observed demand versus forecasts','Report pages 6–7: summer-week overlay and demand-level comparison.',6,['FIND-SUMMER-WEEK','FIND-PEAK']),
 ('SEC-PEAK','Peak-demand performance','Report page 7: 88 historical top-one-percent load hours; cross-model ranking and underforecast bias.',7,['FIND-PEAK','FIND-UNDER','FIND-CAUSE']),
 ('SEC-RECOMMEND','Recommendations and limits','Report page 8: critical methodological qualifications, ethics and future work.',8,['LIMIT-ORIGIN','LIMIT-WEATHER','LIMIT-CAUSAL']),
 ('SEC-QA','Appendix: research questions and answers','Report pages 12–13: ten documented clarifications about methods, fairness and implications.',12,['FIND-OVERALL','FIND-PEAK','LIMIT-ORIGIN'])]
APPENDIX_Q=[
 ('What business decision does the project inform?',['GOAL-BUSINESS','LIMIT-CAUSAL']),
 ('What exactly are we predicting?',['GOAL-RESEARCH','DATA-HISTORY']),
 ('Why use ERCOT’s published forecast?',['METHOD-ERCOT','LIMIT-ORIGIN']),
 ('Does adding weather always help?',['FIND-WEATHER','LIMIT-WEATHER']),
 ('Which team model performed best?',['FIND-OVERALL','FIND-PEAK']),
 ('Why didn’t any model beat ERCOT?',['FIND-ERCOT','LIMIT-WEATHER']),
 ('How do models perform on the highest-demand hours?',['FIND-PEAK','FIND-UNDER']),
 ('Is the ERCOT comparison fair?',['LIMIT-ORIGIN','LIMIT-WEATHER']),
 ('Could this model be used operationally today?',['LIMIT-ORIGIN','LIMIT-CAUSAL']),
 ('What would most improve forecasts?',['DEC-WEIGHT-TEST','LIMIT-ORIGIN','LIMIT-WEATHER'])]

def build(outpath=None):
    base=json.loads((ROOT/'data'/'graph_v1_reference.json').read_text())
    fig_notes=json.loads((ROOT/'data'/'figure_notes.json').read_text())
    metrics=json.loads((ROOT/'data'/'model_metrics.json').read_text())
    nodes={n['id']:dict(n) for n in base['nodes']};edges=[]; seen=set()
    # Legacy visual cluster nodes summarize multiple figures; individual FIG-Fxx nodes own image assets.
    for legacy_id in [n for n in nodes if n.startswith('V-')]:
        nodes[legacy_id]['type']='visual_collection'
    def add_node(id,type,title,summary='',status='source-supported',sources=None,**kw):
        if id in nodes:raise ValueError(f'duplicate node {id}')
        nodes[id]=dict(id=id,type=type,title=title,summary=summary,status=status,sources=sources or [],**kw)
    def connect(a,b,relation,weight=3,kind='context',flow='association',rationale=None):
        if a not in nodes or b not in nodes:raise ValueError(f'unknown endpoint {a}->{b}')
        key=(a,b,relation)
        if key in seen:return
        seen.add(key)
        edges.append(dict(**{'from':a,'to':b},relation=relation,weight=weight,kind=kind,flow=flow,
           rationale=rationale or f'{relation}: {nodes[a]["title"]} and {nodes[b]["title"]}. Editorial link; not a causal coefficient.'))
    def infer_prior_weight(e):
        r=e['relation'].lower()
        if '50%' in r or 'produces' in r or 'defines matched' in r:return 5
        if any(s in r for s in ['prepared','engineered','supported preparation','officially exported','covers test','defines denominator','aligned using','visualized by','contains']):return 4
        if any(s in r for s in ['supports / describes','needed to resolve','documents current status']):return 2
        if 'suggest' in r or 'hypothesis' in r:return 1
        return 3
    for e in base['edges']:
        flow='dependency' if e['relation'].lower() in ('prepared','engineered','officially exported','produces','enables common-hour evaluation','defines matched hours for','supports','reveals','contributes evidence to','changed implementation of') else 'association'
        connect(e['from'],e['to'],e['relation'],infer_prior_weight(e),kind='original-link',flow=flow,
                rationale='Preserved from source-linked context web v1. Relationship strength is an editorial classification; inspect original source before asserting causality.')
    # Add per-figure fine-grained nodes with notebook cell references and source image paths.
    for fid,info in fig_notes.items():
        heading=FIGURE_TITLES.get(fid) or info['title'].split('—',1)[-1].strip().split('|')[0].strip() or f'Visualization {fid}'
        q=info['research_question'] or {
           'F14':'Which forecasting approaches have the smallest matched-hour MAE?',
           'F16':'How do actual July-hourly demand and alternative model predictions differ?',
           'F20':'Do rolling SARIMA and weather XGBoost make complementary signed errors?',
        }.get(fid, f'What aspect of ERCOT demand or forecast behavior does {fid} show?')
        fig_id=f'FIG-{fid}'
        add_node(fig_id,'visual',f'{fid} | {heading}',
                 summary=info['notebook_commentary_excerpt'],
                 sources=[{'file':'DSC450_ERCOT_Full_Visualization_Hybrid.ipynb',
                    'locator':f'notebook code cell {info["source_notebook_cell_0_based"]} (zero-based); preceding explanatory markdown cell {info["source_markdown_cell_0_based"]}'}],
                 asset_path=info['figure_path'],notebook_cell=info['source_notebook_cell_0_based'],
                 research_question=q,sha256=info['image_sha256'])
        add_node(f'Q-{fid}','question',f'{fid}: {q}',
                 summary='Analytical question or presentation reading purpose attached to the corresponding notebook figure.',
                 status='source-supported' if info['research_question'] else 'interpretive',
                 sources=nodes[fig_id]['sources'],kind='figure-research-question')
        connect('SRC-NOTEBOOK',fig_id,'contains embedded figure',4,'provenance','dependency',f'Figure {fid} extracted from existing notebook output at recorded cell.')
        connect('SRC-NOTEBOOK',f'Q-{fid}','documents visual question',4,'provenance','dependency','Notebook Markdown records the intent of this figure; generated question marked interpretive where absent.')
        connect(f'Q-{fid}',fig_id,'answered or illustrated by',4,'reasoning','dependency','Notebook figure designed to investigate the attached question; it need not fully answer it.')
        if fid.startswith('F0') and fid not in ('F03A','F03B','F03C','F03D','F03E'): src='SRC-CLEAN'
        elif fid.startswith('F0'):src='SRC-CLEAN'
        elif fid in ['F10','F11','F12','F13']:src='SRC-PRED'
        else: src='SRC-PRED'
        connect(src,fig_id,'provides input values for visual',4,'provenance','dependency','Figure sources are mapped from notebook narrative and source CSV roles; check exact code for additional inputs.')
        for claim in FIG_FINDINGS[fid]:
            connect(fig_id,claim,'visual evidence for interpretation',4,'evidence','dependency',f'Figure {fid} offers descriptive or diagnostic support; not necessarily causal proof.')
            connect(claim,fig_id,'communicated with',3,'presentation','dependency',f'Changes to claim {claim} may require a new annotation or review of figure {fid}.')
        for lim in FIG_LIMITATIONS.get(fid,[]):
            connect(lim,fig_id,'qualifies interpretation of',4,'caveat','dependency',f'{lim} applies when interpreting or presenting {fid}.')
        if fid in ('F03','F03A','F03B','F03C','F03D','F03E','F04','F05'):
            connect(fig_id,'DATA-FEATURES','motivates engineered time features',3,'reasoning','association','Observed temporal patterns help justify, but do not validate, time features.')
    # Cross-reference legacy thematic collections to the individual source images.
    coll={'V-F03':['F03'],'V-F03-SEASONS':['F03A','F03B','F03C','F03D','F03E'],
     'V-F12':['F12'],'V-F13':['F13'],'V-F14':['F14'],'V-F16':['F16'],'V-F17':['F17'],
     'V-F20':['F20'],'V-F21-25':['F21','F22','F23','F24','F25'],
     'V-F26-33':['F26','F27','F28','F29','F30','F31','F32','F33']}
    for group,fs in coll.items():
        for fid in fs:
            connect(f'FIG-{fid}',group,'belongs to figure collection',4,'organization','dependency',
                'Links a source figure to its original thematic summary without losing individual image identity.')
    # Add exact quantitative observations, linked to method + CSV + conclusions.
    labels={'ERCOT_DAY_AHEAD':'ERCOT benchmark','HYBRID_50_50':'Official 50/50 hybrid','WEATHER_XGBOOST':'Weather XGBoost',
        'XGBOOST':'Original XGBoost','ROLLING_SARIMA':'Rolling SARIMA','WEATHER_SARIMAX':'Weather SARIMAX','SEASONAL_NAIVE':'Seasonal naive','PROPHET':'Prophet'}
    for context,metric in [('overall','overall'),('top_1pct','top 1% of actual test-year demand')]:
      for col in MODEL_COLUMNS:
        m=metrics[context][col]
        mid=f'METRIC-{context.upper()}-{col}'
        add_node(mid,'metric',f'{labels[col]} MAE | {metric}',
            summary=f'MAE={m["MAE_MWh"]:,.3f} MWh; MAPE={m["MAPE_percent"]:.4f}%; signed forecast−actual bias={m["signed_bias_MWh"]:,.3f} MWh; test context={metric}.',
            status='csv-verified',sources=[{'file':metrics['source_file'],'locator':f'{col}, ACTUAL_DEMAND_MWH; {context}, row subset as defined in metrics.py'}],
            value=m['MAE_MWh'],unit='MWh',metric='MAE',context=context,mape=m['MAPE_percent'],signed_bias=m['signed_bias_MWh'])
        connect('SRC-PRED',mid,'used to calculate exact MAE',5,'provenance','dependency','Calculated directly on the shared prediction export, not transcribed from image.')
        connect(MODEL_COLUMNS[col],mid,'evaluated as',5,'quantitative','dependency',f'Corresponds to predictions in column {col} in {context} subset.')
        if context=='overall':
            connect(mid,'FIND-OVERALL' if col!='ERCOT_DAY_AHEAD' else 'FIND-ERCOT', 'contributes matched-error result',5,'evidence','dependency','MAE calculated on the 8,640 common forecast-available hours.')
            connect(mid,'FIG-F14','shown on overall leaderboard',5,'quantitative','dependency','F14 includes all matched-hour model MAE bars.')
        else:
            connect(mid,'FIND-PEAK','supports retrospective peak ranking',5,'evidence','dependency','Top 1% defined on observed actual demand across full 8,760-hour test year.')
            connect(mid,'FIG-F17','supports demand-group comparison',4,'quantitative','dependency','Top load category on F17 is aligned with retrospective high-demand performance.')
            connect('LIMIT-PEAK-BIN',mid,'restricts operational interpretation',5,'caveat','dependency','Selection uses observed future outcome and cannot be treated as advance-known regime.')
    facts=[
     ('FACT-HISTORY','Historical demand observation count',41616,'hours','Historical EIA-930 cleaned hourly observations, January 2022–September 2026','DATA-HISTORY'),
     ('FACT-TEST','Full holdout length',metrics['test_hours'],'hours','Chronological test from October 2025 through September 2026','DATA-SPLIT'),
     ('FACT-MATCHED','Shared comparison sample',metrics['matched_hours'],'hours','Rows with an ERCOT day-ahead prediction and all other required model values','DATA-SHARED'),
     ('FACT-MISSING','Missing ERCOT forecast hours',metrics['missing_ercot_hours'],'hours','Missing ERCOT benchmark rows excluded for full leaderboard comparison','DATA-SHARED'),
     ('FACT-TOP1','Retrospective peak-load matched hours',metrics['top_1pct_matched_hours'],'hours','Observed demand at or above 99th percentile of full 8,760 hours','FIND-PEAK'),
     ('FACT-CUTOFF','Peak-hour definition threshold',metrics['top_1pct_threshold_all_test_hours_MWh'],'MWh','Observed-demand 99th percentile across full test year, not the matched subset','LIMIT-PEAK-BIN'),
     ('FACT-HYBRID-IMPROVEMENT','Hybrid improvement over seasonal naive',metrics['hybrid_MAE_improvement_over_naive_percent'],'percent','Reduction of matched-hour MAE relative to seasonal naive','FIND-OVERALL'),
    ]
    for nid,title,val,unit,summary,target in facts:
        src='SRC-CLEAN' if nid=='FACT-HISTORY' else 'SRC-PRED'
        add_node(nid,'metric',title,summary,'csv-verified' if nid!='FACT-HISTORY' else 'source-supported',
          sources=[{'file':metrics['source_file'] if nid!='FACT-HISTORY' else 'Milestone_2_ERCOT_Hybrid_Updated(2).docx','locator':'computed metrics data' if nid!='FACT-HISTORY' else 'Methods / Analysis p.4'}],value=val,unit=unit)
        connect(src,nid,'documents numerical fact',5 if nid!='FACT-HISTORY' else 4,'provenance','dependency','Numerical datum derives from the indicated dataset or report.')
        connect(nid,target,'grounds numerical statement',5,'evidence','dependency','This numeric fact supports the named research statement.')
    # Verifiable relationship for exact hybrid calculation, versus a hypothesis about causal extrapolation.
    connect('METRIC-OVERALL-HYBRID_50_50','FACT-HYBRID-IMPROVEMENT','used in improvement calculation',5,'quantitative','dependency','100 × (1 - hybrid MAE / naive MAE).')
    connect('METRIC-OVERALL-SEASONAL_NAIVE','FACT-HYBRID-IMPROVEMENT','baseline denominator in improvement',5,'quantitative','dependency','Seasonal naive MAE is the denominator.')
    connect('FIND-CAUSE','LIMIT-CAUSAL','requires qualification',3,'caveat','association','Tree extrapolation is a plausible mechanism, not isolated by an experiment.')
    # Report section nodes and traceable appendix prompts.
    for nid,title,summary,page,targets in SECTION_DETAILS:
        add_node(nid,'report_section',title,summary,status='source-supported',sources=[{'file':'Milestone_2_ERCOT_Hybrid_Updated(2).docx','locator':f'printed page {page}'}])
        connect('SRC-REPORT',nid,'contains written evidence',4,'provenance','dependency','Report section exists in the October 25 hybrid-updated document.')
        for target in targets:connect(target,nid,'explained in report section',4,'communication','dependency',f'Report section discusses {target}.')
    for i,(title,targets) in enumerate(APPENDIX_Q,1):
        nid=f'QA-{i:02d}'
        add_node(nid,'appendix_question',f'Appendix Q{i}: {title}',
         'Final report appendix question; answer must be checked against exact approved wording.',
         status='source-supported',sources=[{'file':'Milestone_2_ERCOT_Hybrid_Updated(2).docx','locator':f'Appendix, printed pages 12–13, question {i}'}])
        connect('SEC-QA',nid,'includes question',4,'documentation','dependency','Approved appendix includes this question.')
        for target in targets:connect(target,nid,'addresses question',4,'reasoning','dependency','The linked concept informs this appendix response.')
    # Project-level data/model-to-finding links clarify end-to-end source-of-truth chain.
    connect('DATA-HISTORY','METHOD-SARIMA','training/forecast input',4,'dataflow','dependency','Rolling time-series model uses observed demand history.')
    connect('DATA-FEATURES','METHOD-XGB','model input',4,'dataflow','dependency','XGBoost uses calendar and historical lag predictors.')
    connect('DATA-FEATURES','METHOD-WXGB','model input',4,'dataflow','dependency','Weather XGBoost also uses historical and calendar features.')
    connect('DATA-WEATHER','METHOD-WXGB','observed-weather engineered predictors',4,'dataflow','dependency','Historical observed weather features informed model comparison; future-available inputs still need auditing.')
    connect('DATA-WEATHER','METHOD-SARIMAX','external regressors',4,'dataflow','dependency','Historical weather regressors used in tested SARIMAX variant.')
    connect('METHOD-SARIMA','METHOD-HYBRID','contributes 50% predictions',5,'dataflow','dependency','Official hybrid averages these actual prediction columns.')
    connect('METHOD-WXGB','METHOD-HYBRID','contributes 50% predictions',5,'dataflow','dependency','Official hybrid averages these actual prediction columns.')
    connect('DATA-SHARED','METRIC-OVERALL-HYBRID_50_50','restricts common evaluation sample',5,'dataflow','dependency','Exclude 120 missing ERCOT hours before leaderboard comparison.')
    connect('FIND-PEAK','SEC-RECOMMEND','motivates demand-regime caution',4,'reasoning','dependency','Peak errors support considering condition-aware evaluation, not deploying a switching rule.')
    connect('LIMIT-ORIGIN','SEC-RECOMMEND','qualifies deployment claim',5,'caveat','dependency','Forecast issuance alignment remains unresolved.')
    meta=dict(base.get('metadata',{}),version='2.0-python',generated='2026-10-26',
       purpose='Python-queryable, source-linked, weighted research context graph; not an approved script.',
       edge_weight_scale={'1':'tentative/planned','2':'contextual','3':'interpretive','4':'direct documented','5':'quantitatively derived'},
       weight_warning='Relationship strength is editorial and does not represent probability, correlation, causation or statistical significance.',
       data_integrity='CSV metrics independently recalculated. Original model-training code and future forecast availability not comprehensively audited.')
    result={'metadata':meta,'nodes':list(nodes.values()),'edges':edges}
    out=Path(outpath) if outpath else ROOT/'data'/'context_graph.json'
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    return result
if __name__=='__main__':
    d=build();print('Built',len(d['nodes']),'nodes,',len(d['edges']),'edges')
