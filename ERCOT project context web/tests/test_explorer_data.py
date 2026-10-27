"""Guard against broken graph relationships and missing figure assets."""
from pathlib import Path
import json
import unittest
import hashlib
import struct
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
    def test_figure_manifest_matches_source_images(self):
        catalog=json.loads((ROOT/"data/figure_catalog.json").read_text())
        notes=json.loads((ROOT/"data/figure_notes.json").read_text())
        visuals={n["id"].replace("FIG-",""):n for n in self.g["nodes"] if n["type"]=="visual"}
        self.assertEqual(set(visuals),{entry["id"] for entry in catalog})
        for item in catalog:
            fig_id=item["id"]
            with self.subTest(figure=fig_id):
                figure=visuals[fig_id]
                source=ROOT/item["file"]
                img=source.read_bytes()
                self.assertEqual(img[:8],bytes([137,80,78,71,13,10,26,10]),"PNG signature")
                width,height=struct.unpack(">II",img[16:24])
                self.assertEqual((width,height),(item["width"],item["height"]),"PNG dimensions")
                self.assertEqual(len(img),item["bytes"],"PNG byte count")
                digest=hashlib.sha256(img).hexdigest()
                self.assertEqual(item["sha256"],digest,"Catalog digest")
                self.assertEqual(figure["sha256"],digest,"Graph provenance digest")
                self.assertEqual(notes[fig_id]["image_sha256"],digest,"Notebook notes provenance digest")

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
        self.assertIn('src="./scene-review.js"',html)
        self.assertIn('href="./scene-review.css"',html)
        self.assertIn('fetch("./data/context_graph.json")',js)
        self.assertIn('fetch("./data/model_metrics.json")',js)
        self.assertIn("ERCOT%20project%20context%20web/explorer.html",hub)
        self.assertIn("outputs/ERCOT_CONTEXT_WEB.html",html)
if __name__=="__main__":unittest.main()
