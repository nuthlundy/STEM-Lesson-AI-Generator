import unittest
import os
import json
import tempfile
from core.health import PlatformHealthChecker, PlatformHealthReporter

class TestHealth(unittest.TestCase):
    def test_health_checker(self):
        data = PlatformHealthChecker.run_health_checks()
        self.assertIn("status", data)
        self.assertIn("memory", data)
        self.assertIn("subsystems", data)
        self.assertEqual(data["subsystems"]["logging"], "Healthy")

    def test_health_reporter(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            report = PlatformHealthReporter.generate_report(workspace_root=tmp_dir)
            self.assertIn("health", report)
            
            file_path = os.path.join(tmp_dir, "platform_health.json")
            self.assertTrue(os.path.exists(file_path))
            
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["health"]["subsystems"]["logging"], "Healthy")

if __name__ == "__main__":
    unittest.main()
