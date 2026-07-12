import unittest
import tempfile
import os
from core.bootstrap import (
    PlatformBootstrap,
    PlatformLoader,
    PlatformInitializer,
    PlatformHealthCheck
)
from core.validation.exceptions import ValidationError

class TestBootstrap(unittest.TestCase):
    def test_initializer(self):
        ctx = PlatformInitializer.initialize()
        self.assertIn("logger", ctx)
        self.assertIn("dispatcher", ctx)
        self.assertIn("plugin_manager", ctx)
        self.assertIn("orchestrator", ctx)

    def test_health_check_preflight(self):
        # Good path
        with tempfile.TemporaryDirectory() as tmp_dir:
            success = PlatformHealthCheck.run_preflight(tmp_dir)
            self.assertTrue(success)
            
            # Bad path (nested non-existent directory)
            bad_path = os.path.join(tmp_dir, "nested_does_not_exist", "sub_does_not_exist")
            success_bad = PlatformHealthCheck.run_preflight(bad_path)
            self.assertFalse(success_bad)

    def test_bootstrap_coordination(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            ctx = PlatformBootstrap.bootstrap(workspace_root=tmp_dir)
            self.assertIn("orchestrator", ctx)
            
            bad_path = os.path.join(tmp_dir, "nested_does_not_exist", "sub_does_not_exist")
            with self.assertRaises(ValidationError):
                PlatformBootstrap.bootstrap(workspace_root=bad_path)

if __name__ == "__main__":
    unittest.main()
