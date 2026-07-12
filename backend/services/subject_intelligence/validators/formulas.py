from services.subject_intelligence.types import ValidationReport

def validate_formula_syntax(formula: str) -> ValidationReport:
    """Base validator skeleton for chemical/math formulas."""
    return {"valid": True, "errors": [], "details": {}}
