"""Guard against broken graph relationships and missing figure assets."""
from pathlib import Path
import json
import unittest
ROOT = Path(__file__).resolve().parents[1]
class ExplorerDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=json.loads((ROOT/"data/context_graph.json").read_text())
        cls.m=json.loads((ROOT/"data/model_metrics.json").read_text())
    def test_links_and_figures(self):
        nodes=self.g["nodes"];ids={n["id"] for n in nodes}
        self.assertEqual(len(ids),len(nodes))
        self.assertEqual(len(nodes),178)
        self.assertEqual(len(self.g["edges"]),591)
        for e in self.g["edges"]:
            self.assertIn(e["from"],ids)
            self.assertIn(e["to"],ids)
        figs=[n for n in nodes if n["type"]=="visual"]
        self.assertEqual(len(figs),38)
        for n in figs:
            self.assertTrue((ROOT/n["asset_path"]).is_file(),n["id"])
            self.assertTrue(n.get("research_question"))
            self.assertTrue(n.get("sources"))
    def test_model_comparisons(self):
        m=self.m
        self.assertEqual(m["matched_hours"],8640)
        self.assertEqual(m["top_1pct_matched_hours"],88)
        self.assertEqual(len(m["overall"]),8)
        self.assertEqual(set(m["overall"]),set(m["top_1pct"]))
        overall=m["overall"];peak=m["top_1pct"]
        self.assertLess(overall["HYBRID_50_50"]["MAE_MWh"],overall["ROLLING_SARIMA"]["MAE_MWh"])
        self.assertLess(overall["HYBRID_50_50"]["MAE_MWh"],overall["WEATHER_XGBOOST"]["MAE_MWh"])
        self.assertGreater(overall["HYBRID_50_50"]["MAE_MWh"],overall["ERCOT_DAY_AHEAD"]["MAE_MWh"])
        self.assertLess(peak["ROLLING_SARIMA"]["MAE_MWh"],peak["HYBRID_50_50"]["MAE_MWh"])
    def test_static_entrypoints(self):
        html=(ROOT/"explorer.html").read_text()
        js=(ROOT/"explorer.js").read_text()
        hub=(ROOT.parent/"index.html").read_text()
        self.assertIn('src="./explorer.js"',html)
        self.assertIn('href="./explorer.css"',html)
        self.assertIn('fetch("./data/context_graph.json")',js)
        self.assertIn('fetch("./data/model_metrics.json")',js)
        self.assertIn("ERCOT%20project%20context%20web/explorer.html",hub)
        self.assertIn("outputs/ERCOT_CONTEXT_WEB.html",html)
if __name__=="__main__":unittest.main()
