import unittest
import os
import json
import tempfile
from core.documentation import PlatformDocGenerator

class TestDocumentation(unittest.TestCase):
    def test_summary_generation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            summary = PlatformDocGenerator.generate_summary(workspace_root=tmp_dir)
            self.assertIn("registered_artifacts", summary)
            self.assertIn("registered_providers", summary)
            self.assertIn("supported_engines", summary)
            
            file_path = os.path.join(tmp_dir, "platform_summary.json")
            self.assertTrue(os.path.exists(file_path))
            
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIn("registered_artifacts", data)
            self.assertEqual(data["supported_engines"][0], "Document Intelligence Engine")

if __name__ == "__main__":
    unittest.main()
