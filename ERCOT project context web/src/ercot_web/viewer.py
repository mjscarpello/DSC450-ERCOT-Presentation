"""Build a completely offline, interactive context-web explorer using Python + Plotly."""
from pathlib import Path
import json
from collections import defaultdict
import networkx as nx
from plotly.offline.offline import get_plotlyjs
from .graph import load_graph, ROOT

TYPE_COLOR = {
 'source':'#8ea4c8','role':'#d6b2ff','question':'#f8c66d','data':'#5bb8af',
 'decision':'#bf99f4','model':'#55c8ce','metric':'#32af91','finding':'#ffad68',
 'visual':'#67a5ef','visual_collection':'#8c9fba','limitation':'#ed7e91','hypothesis':'#e3b15e',
 'open':'#f07c81','deliverable':'#c6d3e7','report_section':'#adb5c3',
 'appendix_question':'#9faad0'}
TIERS={'source':-3.4,'role':-2.9,'data':-1.8,'question':-2.4,'decision':-.8,
 'model':-.6,'metric':.65,'visual':1.35,'visual_collection':1.9,'finding':2.4,
 'hypothesis':2.8,'limitation':3.,'report_section':3.7,'appendix_question':4.1,
 'deliverable':4.5,'open':4.4}


def generate(outpath:Path|str=ROOT/'outputs'/'ERCOT_CONTEXT_WEB.html', source=None):
    g=load_graph(source or ROOT/'data'/'context_graph.json')
    simple=nx.Graph()
    for a,b,e in g.edges(data=True):
        if simple.has_edge(a,b):simple[a][b]['weight']=max(simple[a][b]['weight'],e['weight'])
        else:simple.add_edge(a,b,weight=e['weight'])
    initial={n:(TIERS.get(info['type'],0), (((sum(ord(x) for x in n)*37)%100)/50-1)*2.2)
             for n,info in g.nodes(data=True)}
    layout=nx.spring_layout(simple,pos=initial,seed=31,iterations=190,k=1.15,weight='weight',scale=2.8)
    rows=[]
    for n,info in g.nodes(data=True):
        rec={'id':n,'x':round(float(layout[n][0])*.82+TIERS.get(info['type'],0)*.36,5),
            'y':round(float(layout[n][1])+.03*((sum(ord(ch) for ch in n)%7)-3),5),
            **dict(info)}
        rec['degree']=int(g.degree(n))
        rows.append(rec)
    edges=[{'from':a,'to':b,**dict(d)} for a,b,d in g.edges(data=True)]
    graph={'nodes':rows,'edges':edges,'meta':g.graph.get('metadata',{}),'typeColors':TYPE_COLOR}
    out=Path(outpath);out.parent.mkdir(parents=True,exist_ok=True)
    tpl=(Path(__file__).with_name('viewer_template.html')).read_text(encoding='utf8')
    plotjs=get_plotlyjs()
    payload=json.dumps(graph,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    text=tpl.replace('/*__OFFLINE_PLOTLY__*/',plotjs).replace('/*__GRAPH_JSON__*/',payload)
    out.write_text(text,encoding='utf8')
    return {'path':str(out),'nodes':len(rows),'edges':len(edges),'bytes':out.stat().st_size}

if __name__=='__main__':print(generate())
