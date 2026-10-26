"""Extract figure metadata and notebook research-question notes without executing notebooks.

Usage: python tools/extract_figure_notes.py /path/to/source.ipynb
"""
import json,re,sys
from pathlib import Path

root=Path(__file__).resolve().parents[1]
nb_path=Path(sys.argv[1]) if len(sys.argv)>1 else root/'sources'/'DSC450_ERCOT_Full_Visualization_Hybrid.ipynb'
nb=json.loads(nb_path.read_text())
cells=nb['cells']
cat=json.loads((root/'data'/'figure_catalog.json').read_text())

def text(c):
    a=c['source']
    return ''.join(a) if isinstance(a,list) else a

def find_question(mark):
    patterns=[r'\*\*(?:Research question|Business question|Question):\*\*\s*\*?([^\n\*]+)', r'\*\*Why I wanted to add these:\*\*\s*([^\n]+)']
    for p in patterns:
        m=re.search(p,mark,re.I)
        if m:return m.group(1).strip('* .')
    return ''

def title(mark):
    for line in mark.splitlines():
        if re.match(r'^#{2,5}\s',line):
            s=re.sub(r'^#{2,5}\s+','',line)
            return s.strip()
    return ''
notes={}
for x in cat:
    idx=x['notebook_cell']
    m_idx=next((i for i in range(idx,-1,-1) if cells[i]['cell_type']=='markdown'),None)
    md=text(cells[m_idx]) if m_idx is not None else ''
    note=' '.join(re.sub(r'[#*`|]+','',md).split())
    q=find_question(md)
    notes[x['id']]={'id':x['id'],'title':title(md),'research_question':q,
        'source_notebook_cell_0_based':idx,
        'source_markdown_cell_0_based':m_idx,
        'notebook_commentary_excerpt':note[:550],
        'figure_path':x['file'],
        'image_sha256':x['sha256']}
(root/'data'/'figure_notes.json').write_text(json.dumps(notes,indent=2,ensure_ascii=False)+'\n')
print(f'Wrote notes for {len(notes)} figures; extracted explicit questions for {sum(bool(v["research_question"]) for v in notes.values())}')
