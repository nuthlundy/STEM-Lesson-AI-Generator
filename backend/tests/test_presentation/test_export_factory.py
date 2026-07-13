import unittest
from services.presentation.export.factory import PresentationExportFactory
from services.presentation.export.base_exporter import BasePresentationExporter

class TestPresentationExportFactory(unittest.TestCase):
    def setUp(self):
        self.factory = PresentationExportFactory()

    def test_registration_and_lookup(self):
        self.factory.register("pdf", BasePresentationExporter)
        exporter = self.factory.get_exporter("pdf")
        self.assertIsInstance(exporter, BasePresentationExporter)

    def test_unregistered_lookup_raises_error(self):
        with self.assertRaises(ValueError):
            self.factory.get_exporter("unregistered")

    def test_list_supported_types(self):
        self.factory.register("pdf", BasePresentationExporter)
        self.factory.register("html", BasePresentationExporter)
        self.assertEqual(sorted(self.factory.list_supported_types()), ["html", "pdf"])

    def test_factory_multiple_same_registration(self):
        self.factory.register("pdf", BasePresentationExporter)
        self.factory.register("pdf", BasePresentationExporter)
        self.assertIn("pdf", self.factory.list_supported_types())

    def test_factory_reset_lookup(self):
        self.factory.register("txt", BasePresentationExporter)
        exporter = self.factory.get_exporter("txt")
        self.assertIsNotNone(exporter)

    def test_factory_supported_types_empty_default(self):
        self.assertEqual(self.factory.list_supported_types(), [])

    def test_factory_get_exporter_returns_fresh_instance(self):
        self.factory.register("pdf", BasePresentationExporter)
        e1 = self.factory.get_exporter("pdf")
        e2 = self.factory.get_exporter("pdf")
        self.assertNotEqual(id(e1), id(e2))

    def test_factory_type_checks(self):
        self.assertTrue(hasattr(self.factory, "register"))

if __name__ == "__main__":
    unittest.main()
