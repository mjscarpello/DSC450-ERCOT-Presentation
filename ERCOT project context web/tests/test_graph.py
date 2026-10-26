import hashlib,json,unittest
from pathlib import Path
from ercot_web.graph import ROOT,load_graph,audit,trace,impact,node_detail,neighborhood

class TestContextGraph(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.graph=load_graph()
 def test_integrity(self):
    result=audit(self.graph)
    self.assertFalse(result['issues'],result['issues'][:8])
    self.assertFalse(result['isolated_nodes'])
    self.assertGreaterEqual(result['nodes'],170)
    self.assertGreaterEqual(result['edges'],550)
 def test_all_38_figure_assets_match_hashes(self):
    figs=[(id,d) for id,d in self.graph.nodes(data=True) if d['type']=='visual']
    self.assertEqual(len(figs),38)
    for id,d in figs:
     p=ROOT/d['asset_path']
     self.assertTrue(p.is_file(),(id,p))
     self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),d['sha256'],id)
 def test_direct_numeric_facts(self):
    d=json.loads((ROOT/'data'/'model_metrics.json').read_text())
    self.assertEqual(d['matched_hours'],8640)
    self.assertEqual(d['top_1pct_matched_hours'],88)
    self.assertLess(d['hybrid_max_abs_formula_difference_MWh'],1e-7)
    self.assertAlmostEqual(self.graph.nodes['METRIC-OVERALL-HYBRID_50_50']['value'],2005.85,delta=.02)
 def test_connection_strength_varies(self):
    weights={e['weight'] for _,_,e in self.graph.edges(data=True)}
    self.assertGreaterEqual(len(weights),4)
 def test_provenance_to_visual_to_claim(self):
    self.assertTrue(self.graph.has_edge('SRC-NOTEBOOK','FIG-F17'))
    self.assertTrue(self.graph.has_edge('FIG-F17','FIND-PEAK'))
    self.assertTrue(self.graph.has_edge('LIMIT-PEAK-BIN','FIG-F17'))
 def test_trace_and_impact(self):
    chain=trace(self.graph,'SRC-PRED','FIND-PEAK')
    self.assertEqual(chain[0]['id'],'SRC-PRED')
    self.assertEqual(chain[-1]['id'],'FIND-PEAK')
    affected={x['id'] for x in impact(self.graph,'SRC-PRED',max_depth=3)}
    self.assertIn('METRIC-OVERALL-HYBRID_50_50',affected)
    sub=neighborhood(self.graph,'FIND-PEAK',depth=1,min_weight=4)
    self.assertIn('FIG-F17',sub)
 def test_claim_statuses(self):
    self.assertEqual(self.graph.nodes['FIND-CAUSE']['status'],'interpretive')
    self.assertEqual(self.graph.nodes['OPEN-UPSTREAM']['status'],'open')
    self.assertEqual(self.graph.nodes['METRIC-TOP_1PCT-ROLLING_SARIMA']['status'],'csv-verified')
if __name__=='__main__':unittest.main()
