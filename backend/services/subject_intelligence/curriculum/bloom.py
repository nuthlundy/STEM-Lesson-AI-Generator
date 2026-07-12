from typing import Literal

class BloomTaxonomyClassifier:
    """Classifies learning objective descriptions into Bloom's Taxonomy cognitive levels."""
    
    VERBS = {
        "Remember": ["define", "identify", "list", "recall", "state", "name", "memorize"],
        "Understand": ["explain", "describe", "discuss", "summarize", "classify", "interpret"],
        "Apply": ["apply", "calculate", "solve", "use", "demonstrate", "illustrate", "compute"],
        "Analyze": ["analyze", "compare", "contrast", "differentiate", "distinguish", "examine"],
        "Evaluate": ["evaluate", "judge", "assess", "defend", "rate", "support", "critique"],
        "Create": ["create", "design", "develop", "construct", "formulate", "plan", "compose"]
    }
    
    @staticmethod
    def classify(description: str) -> Literal["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]:
        desc_lower = description.lower()
        words = desc_lower.split()
        first_word = words[0] if words else ""
        first_word = "".join(c for c in first_word if c.isalnum())
        
        for level, verb_list in BloomTaxonomyClassifier.VERBS.items():
            if first_word in verb_list:
                return level
                
        for level, verb_list in BloomTaxonomyClassifier.VERBS.items():
            for verb in verb_list:
                if f" {verb} " in f" {desc_lower} ":
                    return level
                    
        return "Understand"
