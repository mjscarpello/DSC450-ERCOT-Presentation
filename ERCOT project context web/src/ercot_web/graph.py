"""Typed, weighted ERCOT research-knowledge graph and safe graph traversal."""
from __future__ import annotations
import json
import math
from collections import deque
from pathlib import Path
import networkx as nx

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data' / 'context_graph.json'

# Weight means editorial strength of CONNECTION, not statistical correlation or confidence.
WEIGHTS = {1:'tentative / planning association',2:'background context',3:'meaningful interpretation',4:'direct documented relationship',5:'direct quantitative derivation'}
STATUSES = {'csv-verified', 'source-supported', 'conversation-supported', 'interpretive', 'user-plan', 'open'}


def load_graph(path: str | Path = DATA) -> nx.MultiDiGraph:
    raw = json.loads(Path(path).read_text(encoding='utf-8'))
    g = nx.MultiDiGraph(metadata=raw.get('metadata', {}))
    for n in raw['nodes']:
        info = dict(n)
        nid = info.pop('id')
        g.add_node(nid, **info)
    for i,e in enumerate(raw['edges']):
        info = dict(e)
        a=info.pop('from'); b=info.pop('to')
        if a not in g or b not in g:
            raise ValueError(f'Dangling edge: {a} -> {b}')
        info.setdefault('weight', 2)
        info.setdefault('kind','context')
        info.setdefault('flow','association')
        g.add_edge(a,b,key=f'e{i:04d}',**info)
    return g


def node_detail(g:nx.MultiDiGraph, node_id:str)->dict:
    if node_id not in g:
        raise KeyError(f'Unknown node: {node_id}')
    neighbors=[]
    for u,v,k,e in g.in_edges(node_id,keys=True,data=True):
        neighbors.append({'direction':'incoming','id':u,'title':g.nodes[u]['title'],**e})
    for u,v,k,e in g.out_edges(node_id,keys=True,data=True):
        neighbors.append({'direction':'outgoing','id':v,'title':g.nodes[v]['title'],**e})
    return {'id':node_id, **dict(g.nodes[node_id]), 'connections':sorted(neighbors,key=lambda x:-x['weight'])}


def neighborhood(g:nx.MultiDiGraph,node_id:str,depth:int=2,min_weight:int=1,category:str|None=None):
    if node_id not in g: raise KeyError(node_id)
    found={node_id}; frontier={node_id}
    for _ in range(depth):
        new=set()
        for a in frontier:
            for b in g.predecessors(a):
                if any((e['weight']>=min_weight and (not category or e.get('kind')==category)) for e in g.get_edge_data(b,a).values()):new.add(b)
            for b in g.successors(a):
                if any((e['weight']>=min_weight and (not category or e.get('kind')==category)) for e in g.get_edge_data(a,b).values()):new.add(b)
        frontier=new-found; found.update(frontier)
    h=g.subgraph(found).copy()
    for a,b,k,d in list(h.edges(keys=True,data=True)):
        if d['weight']<min_weight or (category and d.get('kind')!=category):h.remove_edge(a,b,k)
    return h


def trace(g:nx.MultiDiGraph,start:str,end:str,min_weight:int=1,max_hops:int=8)->list[dict]:
    """Find weighted short explanation chain treating associations as navigable either way.

    Traversing an association backward does NOT assert reverse causality.
    """
    if start not in g or end not in g: raise KeyError('Unknown start/end')
    h=nx.Graph()
    for a,b,e in g.edges(data=True):
        if e['weight']<min_weight:continue
        cost=1+(5-e['weight'])*0.45
        if not h.has_edge(a,b) or cost<h[a][b]['cost']:
            h.add_edge(a,b,cost=cost,relation=e['relation'],weight=e['weight'])
    path=nx.shortest_path(h,start,end,weight='cost')
    if len(path)-1>max_hops:raise ValueError(f'Shortest path is {len(path)-1} hops > limit {max_hops}')
    return [{'id':p,'title':g.nodes[p]['title'],'via':None if i==0 else dict(h[path[i-1]][p])} for i,p in enumerate(path)]


def impact(g:nx.MultiDiGraph,node_id:str,max_depth:int=5,min_weight:int=1)->list[dict]:
    """Follow only explicitly marked *dependency* edges outward; no inferred causality."""
    if node_id not in g:raise KeyError(node_id)
    seen={node_id}; todo=deque([(node_id,0)])
    result=[]
    while todo:
        a,d=todo.popleft()
        if d>=max_depth:continue
        for b in g.successors(a):
            valid=[e for e in g.get_edge_data(a,b).values() if e.get('flow')=='dependency' and e['weight']>=min_weight]
            if valid and b not in seen:
                seen.add(b);todo.append((b,d+1))
                result.append({'id':b,'title':g.nodes[b]['title'],'type':g.nodes[b]['type'],'depth':d+1,'via':valid[0]['relation']})
    return result


def audit(g:nx.MultiDiGraph)->dict:
    issues=[]
    for n,info in g.nodes(data=True):
        if not info.get('title'):issues.append(f'{n}: missing title')
        if info.get('status') not in STATUSES:issues.append(f'{n}: unknown status {info.get("status")}')
        if info.get('type')=='visual' and not info.get('asset_path'):issues.append(f'{n}: missing visual asset')
        if info.get('type') in ('finding','hypothesis') and not (info.get('sources') or g.in_degree(n)): issues.append(f'{n}: unsupported claim')
    for a,b,e in g.edges(data=True):
        w=e.get('weight')
        if not isinstance(w,int) or w not in WEIGHTS:issues.append(f'{a}->{b}: invalid weight {w}')
        if not e.get('rationale'):issues.append(f'{a}->{b}: missing relation rationale')
    return {'nodes':g.number_of_nodes(),'edges':g.number_of_edges(),'types':{t:sum(1 for _,d in g.nodes(data=True) if d['type']==t) for t in sorted({d['type'] for _,d in g.nodes(data=True)})},'isolated_nodes':list(nx.isolates(g)),'issues':issues}
