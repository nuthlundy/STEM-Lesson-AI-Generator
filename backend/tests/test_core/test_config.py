import unittest
import os
import json
import tempfile
from core.config.settings import Settings
from core.config.providers import Provider
from core.config.environments import Environment
from core.config.loader import ConfigLoader
from core.config.registry import ConfigRegistry
from core.config.exceptions import (
    ValidationError,
    DuplicateProviderError,
    ProviderNotFoundError
)

class TestConfigSystem(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.registry = ConfigRegistry()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_default_config_loading(self):
        settings = ConfigLoader.load()
        self.assertEqual(settings.environment, "development")
        self.assertTrue(settings.cache)
        self.assertEqual(settings.retry_policy, 3)

    def test_config_loading_with_env_overrides(self):
        os.environ["STEM_ENVIRONMENT"] = "testing"
        os.environ["STEM_TIMEOUT"] = "45.5"
        os.environ["STEM_CACHE"] = "false"
        try:
            settings = ConfigLoader.load()
            self.assertEqual(settings.environment, "testing")
            self.assertEqual(settings.timeout, 45.5)
            self.assertFalse(settings.cache)
        finally:
            del os.environ["STEM_ENVIRONMENT"]
            del os.environ["STEM_TIMEOUT"]
            del os.environ["STEM_CACHE"]

    def test_config_loading_from_file(self):
        file_path = os.path.join(self.temp_dir.name, "config.json")
        with open(file_path, "w") as f:
            json.dump({
                "environment": "staging",
                "timeout": 12.0,
                "logging": "DEBUG"
            }, f)
            
        settings = ConfigLoader.load(file_path)
        self.assertEqual(settings.environment, "staging")
        self.assertEqual(settings.timeout, 12.0)
        self.assertEqual(settings.logging, "DEBUG")

    def test_validation_invalid_environment(self):
        file_path = os.path.join(self.temp_dir.name, "invalid_config.json")
        with open(file_path, "w") as f:
            json.dump({
                "environment": "invalid_env"
            }, f)
            
        with self.assertRaises(ValidationError):
            ConfigLoader.load(file_path)

    def test_validation_invalid_retry_policy(self):
        file_path = os.path.join(self.temp_dir.name, "invalid_config.json")
        with open(file_path, "w") as f:
            json.dump({
                "retry_policy": 15
            }, f)
            
        with self.assertRaises(ValidationError):
            ConfigLoader.load(file_path)

    def test_validation_invalid_timeout(self):
        file_path = os.path.join(self.temp_dir.name, "invalid_config.json")
        with open(file_path, "w") as f:
            json.dump({
                "timeout": -5.0
            }, f)
            
        with self.assertRaises(ValidationError):
            ConfigLoader.load(file_path)

    def test_provider_registration_and_lookup(self):
        prov = Provider(
            provider_name="gemini-flash",
            provider_type="Gemini",
            model_name="gemini-1.5-flash",
            api_key="mock-key"
        )
        self.registry.register_provider(prov)
        retrieved = self.registry.get_provider("gemini-flash")
        self.assertEqual(retrieved.model_name, "gemini-1.5-flash")
        self.assertEqual(retrieved.provider_type, "Gemini")

    def test_duplicate_provider_registration_protection(self):
        prov = Provider(
            provider_name="gemini-flash",
            provider_type="Gemini",
            model_name="gemini-1.5-flash",
            api_key="mock-key"
        )
        self.registry.register_provider(prov)
        with self.assertRaises(DuplicateProviderError):
            self.registry.register_provider(prov)

    def test_provider_not_found(self):
        with self.assertRaises(ProviderNotFoundError):
            self.registry.get_provider("missing-provider")

    def test_list_providers(self):
        prov1 = Provider(
            provider_name="gemini-flash",
            provider_type="Gemini",
            model_name="gemini-1.5-flash"
        )
        prov2 = Provider(
            provider_name="openai-gpt4",
            provider_type="OpenAI",
            model_name="gpt-4o"
        )
        self.registry.register_provider(prov1)
        self.registry.register_provider(prov2)
        
        providers_list = self.registry.list_providers()
        self.assertEqual(len(providers_list), 2)
        names = [p.provider_name for p in providers_list]
        self.assertIn("gemini-flash", names)
        self.assertIn("openai-gpt4", names)

    def test_invalid_provider_type_validation(self):
        prov = Provider(
            provider_name="bad-provider",
            provider_type="UnknownType",
            model_name="gpt-4"
        )
        with self.assertRaises(ValidationError):
            self.registry.register_provider(prov)

    def test_environment_switching(self):
        settings_dev = Settings(environment="development")
        settings_prod = Settings(environment="production")
        
        self.registry.update_settings(settings_dev)
        self.assertEqual(self.registry.settings.environment, "development")
        
        self.registry.update_settings(settings_prod)
        self.assertEqual(self.registry.settings.environment, "production")

    def test_provider_validation_method(self):
        prov = Provider(
            provider_name="claude-sonnet",
            provider_type="Claude",
            model_name="claude-3-5-sonnet"
        )
        self.registry.register_provider(prov)
        self.registry.validate_provider("claude-sonnet")

if __name__ == "__main__":
    unittest.main()
