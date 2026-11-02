"""Execute frozen-prediction notebooks; never retrain models or touch media."""
from pathlib import Path
import json,sys,time,subprocess
import nbformat
ROOT=Path(__file__).resolve().parents[1]
results=[]
for name in ['03_visualization.ipynb','04_presentation_research.ipynb']:
 p=ROOT/'notebooks'/name;start=time.time()
 subprocess.run([sys.executable,str(ROOT/'tools/execute_notebook.py'),str(p)],check=True)
 n=nbformat.read(p,as_version=4)
 results.append({'notebook':name,'status':'pass','executed_code_cells':sum(c.cell_type=='code'for c in n.cells),'seconds':round(time.time()-start,2)})
(ROOT/'validation/NOTEBOOK_EXECUTION.json').write_text(json.dumps({'status':'pass','engine':'Fresh socket-free IPython subprocess per notebook, sequential cell execution and captured outputs. Not a Jupyter server/kernel acceptance test.','scope':'Frozen-prediction analysis only; raw cleaning and training not run','notebooks':results},indent=2)+'\n')
print(json.dumps(results,indent=2))
