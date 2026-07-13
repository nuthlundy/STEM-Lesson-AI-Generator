import unittest
from services.workspace.templates.template import LessonTemplate
from services.workspace.templates.template_validator import TemplateValidator

class TestTemplateValidator(unittest.TestCase):
    def setUp(self):
        self.tmpl = LessonTemplate(
            template_id="t1",
            template_name="Physics",
            category="Science",
            description="Physics curriculum",
            created_timestamp=123.4
        )

    def test_default_template_valid(self):
        self.assertTrue(TemplateValidator.validate(self.tmpl, []))

    def test_empty_template_name_invalid(self):
        self.tmpl.template_name = ""
        self.assertFalse(TemplateValidator.validate(self.tmpl, []))

    def test_curriculum_ngss_valid(self):
        self.tmpl.supported_curriculum = "NGSS"
        self.assertTrue(TemplateValidator.validate(self.tmpl, []))

    def test_curriculum_ib_valid(self):
        self.tmpl.supported_curriculum = "IB"
        self.assertTrue(TemplateValidator.validate(self.tmpl, []))

    def test_curriculum_ccss_valid(self):
        self.tmpl.supported_curriculum = "CCSS"
        self.assertTrue(TemplateValidator.validate(self.tmpl, []))

    def test_curriculum_unsupported_invalid(self):
        self.tmpl.supported_curriculum = "unsupported"
        self.assertFalse(TemplateValidator.validate(self.tmpl, []))

    def test_duplicate_name_invalid(self):
        dup = LessonTemplate(
            template_id="t2",
            template_name="Physics",
            category="Science",
            description="Another desc",
            created_timestamp=567.8
        )
        self.assertFalse(TemplateValidator.validate(self.tmpl, [dup]))

    def test_same_id_duplicate_name_valid(self):
        dup = LessonTemplate(
            template_id="t1",
            template_name="Physics",
            category="Science",
            description="Another desc",
            created_timestamp=567.8
        )
        self.assertTrue(TemplateValidator.validate(self.tmpl, [dup]))

if __name__ == "__main__":
    unittest.main()
