from typing import List
from services.subject_intelligence.constants import STEMSubject

class SubjectSummaryGenerator:
    """Generates structural coverage summaries based on detected concepts."""
    
    @staticmethod
    def generate_summary(subject: STEMSubject, concepts: List[str]) -> str:
        concept_list_str = ", ".join(concepts)
        return f"This document covers the STEM discipline '{subject.value.upper()}' and focuses on the core concepts: {concept_list_str}."
