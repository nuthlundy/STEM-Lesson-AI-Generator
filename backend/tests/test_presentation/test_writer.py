import unittest
import tempfile
import os
import json
from services.presentation.writers.json_writer import JsonPresentationWriter
from services.presentation.schemas import PresentationSessionModel

class TestPresentationWriter(unittest.TestCase):
    def test_json_writer_export(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            model = PresentationSessionModel(
                session_id="test-session",
                presentation_path="lesson.pptx",
                duration_seconds=3600,
                slides=[]
            )
            writer = JsonPresentationWriter()
            out_path = os.path.join(tmp_dir, "session.json")
            writer.write(model, out_path)
            
            self.assertTrue(os.path.exists(out_path))
            with open(out_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["session_id"], "test-session")

if __name__ == "__main__":
    unittest.main()
