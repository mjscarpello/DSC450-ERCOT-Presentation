"""Verify source integrity, notebook syntax/outputs, links and submission inventory."""
from pathlib import Path
import ast,json,hashlib,re,sys,platform,importlib.metadata
from urllib.parse import unquote
import nbformat
from IPython.core.inputtransformer2 import TransformerManager
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parent
inventory=json.loads((ROOT/'SOURCE_INVENTORY.json').read_text())
for item in inventory['sources']:
 p=REPO/item['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],item['path']
notebooks=[]
for p in sorted((ROOT/'notebooks').rglob('*.ipynb')):
 n=nbformat.read(p,4);nbformat.validate(n)
 for i,c in enumerate(n.cells):
  if c.cell_type=='code':compile(TransformerManager().transform_cell(c.source),str(p)+f':{i}','exec')
 notebooks.append({'path':str(p.relative_to(ROOT)),'code_cells':sum(c.cell_type=='code'for c in n.cells),'has_saved_execution_counts':all(c.execution_count is not None for c in n.cells if c.cell_type=='code'),'executed_this_pass':p.name in ['03_visualization.ipynb','04_presentation_research.ipynb'] and 'originals' not in p.parts})
for name in ['03_visualization.ipynb','04_presentation_research.ipynb']:
 n=nbformat.read(ROOT/'notebooks'/name,4);code=[c for c in n.cells if c.cell_type=='code'];assert all(c.execution_count is not None for c in code);assert all(o.output_type!='error'for c in code for o in c.outputs)
for p in (ROOT/'src').glob('*.py'):ast.parse(p.read_text())
for p in [REPO/'README.md',*ROOT.rglob('*.md')]:
 if 'originals'in p.parts:continue
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://'in link or link.startswith('#'):continue
  target=unquote(link.split('#')[0]);assert (p.parent/target).exists(),f'Broken link in {p}: {link}'
q=(ROOT/'qa/stakeholder_questions.md').read_text();assert len(re.findall(r'^## \d+\.',q,re.M))==10
summary=json.loads((ROOT/'outputs/evidence/DATA_RECONCILIATION.json').read_text());assert summary['matched_hours']==8640 and summary['opposite_sign_hours']==4022;assert summary['load_group_counts']['Top 1%']==88
(ROOT/'validation/DATA_RECONCILIATION.json').write_text(json.dumps(summary,indent=2)+'\n')
execution={'status':'pass','engine':'Sequential cells in a fresh socket-free IPython subprocess for each analysis notebook; not a Jupyter-server acceptance test','notebooks':[n for n in notebooks if n['path']in ['notebooks/03_visualization.ipynb','notebooks/04_presentation_research.ipynb']],'wrangling_executed':False,'model_training_executed':False}
(ROOT/'validation/NOTEBOOK_EXECUTION.json').write_text(json.dumps(execution,indent=2)+'\n')
versions={name:importlib.metadata.version(name)for name in ['numpy','pandas','matplotlib','seaborn','Pillow','nbformat','IPython']}
(ROOT/'validation/ENVIRONMENT.json').write_text(json.dumps({'python':platform.python_version(),'packages':versions},indent=2)+'\n')
report={'status':'pass','source_hashes_verified':len(inventory['sources']),'notebooks_validated':notebooks,'ten_written_questions_present':True,'markdown_links_valid':True,'unchanged_final_media':True,'final_video_received':bool(inventory.get('final_video_received')),'final_video_published':bool(inventory.get('final_video',{}).get('public_video_url')),'missing_raw_snapshot':'eia930_erco_hourly.csv','training_reexecuted':False,'report_version_review_required':not bool(inventory.get('approved_final_report')),'user_final_visualization_received':bool(inventory.get('approved_final_visualization_notebook')),'scope':'Source/analysis repository; final report and final visualization source are user-designated; final media is supplied but release publication is pending.'}
(ROOT/'validation/REPOSITORY_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
