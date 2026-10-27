import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from coords import rect_normalized, project_contain

class CoordinatesTest(unittest.TestCase):
    def test_source_normalization(self):
        self.assertEqual(rect_normalized([50, 25, 100, 50], [200, 100]), [.25, .25, .5, .5])
    def test_contain_letterbox(self):
        self.assertEqual(project_contain([50, 25, 100, 50], [200, 100],
            {"x":0,"y":0,"width":200,"height":200}), [50, 75, 100, 50])
    def test_reject_outside(self):
        with self.assertRaises(ValueError):
            rect_normalized([190, 0, 50, 20], [200, 100])

if __name__ == "__main__":
    unittest.main()
