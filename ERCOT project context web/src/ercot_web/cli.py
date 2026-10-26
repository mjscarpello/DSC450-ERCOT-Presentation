"""CLI entry point for the research context web."""
import argparse,json,sys
from pathlib import Path
import networkx as nx
from .graph import load_graph,node_detail,neighborhood,trace,impact,audit,ROOT


def main(argv=None):
    ap=argparse.ArgumentParser(prog='ercot-web',description='Source-linked weighted ERCOT research graph')
    ap.add_argument('--graph',default=None,help='Alternate graph JSON path')
    sp=ap.add_subparsers(dest='command',required=True)
    sp.add_parser('build',help='Regenerate graph from version-1 reference, figure notes and metrics snapshot')
    v=sp.add_parser('viewer',help='Regenerate the interactive standalone HTML explorer');v.add_argument('--output',default=None)
    sp.add_parser('stats',help='Show research node and connection counts')
    v=sp.add_parser('inspect',help='Inspect node and all its typed links');v.add_argument('node')
    v=sp.add_parser('near',help='Get the connected knowledge web around a node');v.add_argument('node');v.add_argument('--depth',type=int,default=2);v.add_argument('--min-weight',type=int,default=3)
    v=sp.add_parser('trace',help='Trace strongest relationship chain between two nodes');v.add_argument('start');v.add_argument('end');v.add_argument('--min-weight',type=int,default=1)
    v=sp.add_parser('impact',help='Review affected downstream concepts on supported directed dependencies');v.add_argument('node');v.add_argument('--depth',type=int,default=5)
    sp.add_parser('audit',help='Validate graph integrity and missing source metadata')
    v=sp.add_parser('figures',help='List extracted notebook figures and originating notebook cell');v.add_argument('--query',default='')
    v=sp.add_parser('refresh-metrics',help='Recalculate numerical facts from predictions CSV and rebuild graph');v.add_argument('--csv',required=True)
    v=sp.add_parser('export-edges',help='Export all weighted links as CSV');v.add_argument('--output',default='outputs/graph_edges.csv')
    args=ap.parse_args(argv)
    if args.command=='build':
        from .build import build
        x=build();print(f'Built {len(x["nodes"])} nodes and {len(x["edges"])} edges');return
    if args.command=='refresh-metrics':
        from .metrics import save
        from .build import build
        x=save(args.csv,ROOT/'data'/'model_metrics.json');build()
        print(json.dumps({'matched_hours':x['matched_hours'],'top_1pct_matched_hours':x['top_1pct_matched_hours'],'overall_mae':{m:vals['MAE_MWh'] for m,vals in x['overall'].items()}},indent=2));return
    if args.command=='viewer':
        from .viewer import generate
        print(json.dumps(generate(args.output or ROOT/'outputs'/'ERCOT_CONTEXT_WEB.html',source=args.graph),indent=2));return
    g=load_graph(args.graph or ROOT/'data'/'context_graph.json')
    if args.command=='stats':
        result=audit(g);result.pop('issues');result['top_connected']=[{'node':n,'connections':d} for n,d in sorted(g.degree(),key=lambda x:-x[1])[:12]]
        result['connection_strengths']={w:sum(e['weight']==w for *_,e in g.edges(data=True)) for w in range(1,6)}
    elif args.command=='inspect':result=node_detail(g,args.node)
    elif args.command=='near':
        h=neighborhood(g,args.node,depth=args.depth,min_weight=args.min_weight)
        result={'center':args.node,'nodes':[{'id':n,'type':d['type'],'title':d['title']} for n,d in h.nodes(data=True)],'edges':[{'from':a,'to':b,'relation':e['relation'],'weight':e['weight']} for a,b,e in h.edges(data=True)]}
    elif args.command=='trace':result=trace(g,args.start,args.end,min_weight=args.min_weight)
    elif args.command=='impact':result=impact(g,args.node,args.depth)
    elif args.command=='audit':result=audit(g)
    elif args.command=='figures':result=[{'id':n,'title':v['title'],'notebook_cell':v['notebook_cell'],'asset_path':v['asset_path'],'question':v.get('research_question','')} for n,v in g.nodes(data=True) if v['type']=='visual' and args.query.lower() in (v['title']+' '+v.get('research_question','')).lower()]
    elif args.command=='export-edges':
        import csv
        o=Path(args.output);o=ROOT/o if not o.is_absolute() else o;o.parent.mkdir(parents=True,exist_ok=True)
        with o.open('w',newline='',encoding='utf8') as f:
            w=csv.DictWriter(f,fieldnames=['source','target','relationship','weight','kind','flow','rationale']);w.writeheader()
            for a,b,e in g.edges(data=True):w.writerow({'source':a,'target':b,'relationship':e['relation'],'weight':e['weight'],'kind':e['kind'],'flow':e['flow'],'rationale':e['rationale']})
        result={'path':str(o),'edges_exported':g.number_of_edges()}
    else:ap.error(f'Unknown command {args.command}')
    print(json.dumps(result,indent=2,ensure_ascii=False,default=str))
    if args.command=='audit' and result['issues']:sys.exit(1)

if __name__=='__main__':main()
