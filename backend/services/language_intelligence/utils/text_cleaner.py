import re

class TextCleaner:
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Deterministically normalizes text by resolving OCR artifacts,
        fixing hyphenation breaks, and consolidating whitespaces.
        """
        if not text:
            return ""
            
        cleaned = text
        
        # 1. Join hyphenated words across line breaks (e.g. "kine-\nmatics" -> "kinematics")
        # Also handles cases with carriage returns
        cleaned = re.sub(r'([a-zA-Z])-\r?\n([a-zA-Z])', r'\1\2', cleaned)
        
        # 2. Replace remaining newlines with spaces
        cleaned = cleaned.replace('\n', ' ').replace('\r', '')
        
        # 3. Consolidate multiple spaces into a single space
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # 4. Trim leading/trailing whitespace
        cleaned = cleaned.strip()
        
        return cleaned
