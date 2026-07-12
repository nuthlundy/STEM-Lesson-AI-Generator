from typing import TypedDict, List, Dict, Any

class ValidationReport(TypedDict):
    valid: bool
    errors: List[str]
    details: Dict[str, Any]

# Type alias for general dynamic payload processing
SubjectPayload = Dict[str, Any]
