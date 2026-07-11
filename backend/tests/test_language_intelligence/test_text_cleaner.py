import unittest
from services.language_intelligence.utils.text_cleaner import TextCleaner

class TestTextCleaner(unittest.TestCase):
    def test_clean_hyphenation(self):
        raw = "This is a kine-\nmatics exam-\r\nple."
        cleaned = TextCleaner.clean_text(raw)
        self.assertEqual(cleaned, "This is a kinematics example.")

    def test_clean_spacing_and_newlines(self):
        raw = "Here   are \n\n some   words.\n"
        cleaned = TextCleaner.clean_text(raw)
        self.assertEqual(cleaned, "Here are some words.")

    def test_empty_string(self):
        self.assertEqual(TextCleaner.clean_text(""), "")
        self.assertEqual(TextCleaner.clean_text("   "), "")

if __name__ == "__main__":
    unittest.main()
