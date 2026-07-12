from typing import Dict, Any

class ObjectiveValidator:
    """Validates learning objectives against SMART criteria (Specific, Measurable, Actionable)."""
    
    @staticmethod
    def validate(description: str) -> Dict[str, Any]:
        """Runs basic syntactic checks to assert objective actionability."""
        desc_lower = description.lower()
        words = description.split()
        errors = []
        
        # Verb checks
        from services.subject_intelligence.curriculum.bloom import BloomTaxonomyClassifier
        all_verbs = []
        for v_list in BloomTaxonomyClassifier.VERBS.values():
            all_verbs.extend(v_list)
            
        has_verb = any(v in desc_lower for v in all_verbs)
        if not has_verb:
            errors.append("Objective must contain an active cognitive verb (e.g., explain, calculate, analyze).")
            
        # Length check
        if len(words) < 5:
            errors.append("Objective is too short to be specific (minimum 5 words required).")
            
        # Vague verb checks
        vague_verbs = ["know", "learn", "appreciate", "believe"]
        first_word = words[0] if words else ""
        first_word = "".join(c for c in first_word if c.isalnum()).lower()
        if first_word in vague_verbs:
            errors.append(f"Objective uses a vague/non-measurable verb '{first_word}'. Use action verbs instead.")
            
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "details": {
                "length": len(words),
                "has_action_verb": has_verb
            }
        }
