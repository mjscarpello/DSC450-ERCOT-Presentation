"""Fresh-process, socket-free IPython execution with notebook output capture."""
from pathlib import Path
import sys,os
import nbformat
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output
import matplotlib
matplotlib.use('module://matplotlib_inline.backend_inline')
from matplotlib_inline.backend_inline import configure_inline_support
p=Path(sys.argv[1]).resolve();os.chdir(p.parents[1]);n=nbformat.read(p,as_version=4)
shell=InteractiveShell.instance();configure_inline_support(shell,'module://matplotlib_inline.backend_inline')
count=0
for index,c in enumerate(n.cells):
 if c.cell_type!='code':continue
 count+=1
 with capture_output(stdout=True,stderr=True,display=True)as cap:
  result=shell.run_cell(c.source,store_history=True)
 c.execution_count=count;c.outputs=[]
 if cap.stdout:c.outputs.append(nbformat.v4.new_output('stream',name='stdout',text=cap.stdout))
 if cap.stderr:c.outputs.append(nbformat.v4.new_output('stream',name='stderr',text=cap.stderr))
 for item in cap.outputs:c.outputs.append(nbformat.v4.new_output('display_data',data=item.data,metadata=item.metadata))
 if result.error_before_exec or result.error_in_exec:
  out=p.parents[1]/'outputs'/('FAILED_'+p.name);nbformat.write(n,out)
  raise RuntimeError(f'{p.name} cell {index}: {result.error_before_exec or result.error_in_exec}')
nbformat.write(n,p)
print(f'PASS {p.name}: {count} code cells in a fresh socket-free IPython process.')
