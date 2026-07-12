import unittest
import os
import tempfile
from core.artifacts.artifact import Artifact
from core.artifacts.registry import ArtifactRegistry, get_canonical_registry
from core.artifacts.exceptions import (
    DuplicateArtifactError,
    ArtifactNotFoundError,
    ValidationError,
    DependencyCycleError,
    MissingDependencyError
)

class TestArtifactRegistry(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.registry = ArtifactRegistry(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_successful_registration_and_lookup(self):
        art = Artifact(
            artifact_id="art1.json",
            artifact_name="Test Art",
            schema_version="1.0",
            engine_name="Document Intelligence Engine",
            engine_version="1.0",
            file_name="art1.json",
            relative_path="art1.json",
            produced_by="Document Intelligence Engine",
            dependencies=[],
            created_at="2026-07-12T00:00:00Z",
            checksum="sha-test",
            description="Testing"
        )
        self.registry.register(art)
        self.assertEqual(self.registry.get("art1.json").artifact_name, "Test Art")
        self.assertFalse(self.registry.exists("art1.json"))
        
        with open(os.path.join(self.temp_dir.name, "art1.json"), "w") as f:
            f.write("{}")
        self.assertTrue(self.registry.exists("art1.json"))

    def test_duplicate_registration_protection(self):
        art = Artifact(
            artifact_id="art.json",
            artifact_name="Test Art",
            schema_version="1.0",
            engine_name="Document Intelligence Engine",
            engine_version="1.0",
            file_name="art.json",
            relative_path="art.json",
            produced_by="Document Intelligence Engine",
            dependencies=[],
            created_at="2026-07-12T00:00:00Z",
            checksum="sha-test",
            description="Testing"
        )
        self.registry.register(art)
        with self.assertRaises(DuplicateArtifactError):
            self.registry.register(art)

    def test_invalid_schema_version_validation(self):
        art = Artifact(
            artifact_id="art.json",
            artifact_name="Test Art",
            schema_version="invalid-version",
            engine_name="Document Intelligence Engine",
            engine_version="1.0",
            file_name="art.json",
            relative_path="art.json",
            produced_by="Document Intelligence Engine",
            dependencies=[],
            created_at="2026-07-12T00:00:00Z",
            checksum="sha-test",
            description="Testing"
        )
        with self.assertRaises(ValidationError):
            self.registry.register(art)

    def test_invalid_engine_name_validation(self):
        art = Artifact(
            artifact_id="art.json",
            artifact_name="Test Art",
            schema_version="1.0",
            engine_name="NonExistentEngine",
            engine_version="1.0",
            file_name="art.json",
            relative_path="art.json",
            produced_by="Document Intelligence Engine",
            dependencies=[],
            created_at="2026-07-12T00:00:00Z",
            checksum="sha-test",
            description="Testing"
        )
        with self.assertRaises(ValidationError):
            self.registry.register(art)

    def test_empty_checksum_validation(self):
        art = Artifact(
            artifact_id="art.json",
            artifact_name="Test Art",
            schema_version="1.0",
            engine_name="Document Intelligence Engine",
            engine_version="1.0",
            file_name="art.json",
            relative_path="art.json",
            produced_by="Document Intelligence Engine",
            dependencies=[],
            created_at="2026-07-12T00:00:00Z",
            checksum="  ",
            description="Testing"
        )
        with self.assertRaises(ValidationError):
            self.registry.register(art)

    def test_missing_dependency_validation(self):
        art = Artifact(
            artifact_id="art.json",
            artifact_name="Test Art",
            schema_version="1.0",
            engine_name="Document Intelligence Engine",
            engine_version="1.0",
            file_name="art.json",
            relative_path="art.json",
            produced_by="Document Intelligence Engine",
            dependencies=["missing_dependency.json"],
            created_at="2026-07-12T00:00:00Z",
            checksum="sha-test",
            description="Testing"
        )
        self.registry.register(art)
        with self.assertRaises(MissingDependencyError):
            self.registry.validate("art.json")

    def test_cycle_detection(self):
        art1 = Artifact(
            artifact_id="art1.json",
            artifact_name="Art 1",
            schema_version="1.0",
            engine_name="Document Intelligence Engine",
            engine_version="1.0",
            file_name="art1.json",
            relative_path="art1.json",
            produced_by="Document Intelligence Engine",
            dependencies=["art2.json"],
            created_at="2026-07-12T00:00:00Z",
            checksum="sha-test",
            description="Testing"
        )
        art2 = Artifact(
            artifact_id="art2.json",
            artifact_name="Art 2",
            schema_version="1.0",
            engine_name="Document Intelligence Engine",
            engine_version="1.0",
            file_name="art2.json",
            relative_path="art2.json",
            produced_by="Document Intelligence Engine",
            dependencies=["art1.json"],
            created_at="2026-07-12T00:00:00Z",
            checksum="sha-test",
            description="Testing"
        )
        self.registry.register(art1)
        self.registry.register(art2)
        
        with self.assertRaises(DependencyCycleError):
            self.registry._graph.topological_sort()

    def test_topological_sort_order(self):
        reg = get_canonical_registry()
        order = reg._graph.topological_sort()
        self.assertEqual(order[0], "lesson.json")
        self.assertEqual(order[-1], "lesson_plan.json")

    def test_consumers_query(self):
        reg = get_canonical_registry()
        consumers = reg.consumers("lesson.json")
        self.assertIn("lesson_language.json", consumers)

    def test_producers_query(self):
        reg = get_canonical_registry()
        self.assertEqual(reg.producers("lesson_plan.json"), ["Lesson Planning Engine"])

if __name__ == "__main__":
    unittest.main()
