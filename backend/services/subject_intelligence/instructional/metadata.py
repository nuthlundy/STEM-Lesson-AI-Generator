from services.subject_intelligence.instructional.schemas import InstructionalMetadata
from services.subject_intelligence.constants import STEMSubject

class InstructionalMetadataGenerator:
    """Generates timing, audience, and recommended approach profiles."""
    
    @staticmethod
    def generate(subject: STEMSubject, total_steps: int) -> InstructionalMetadata:
        total_mins = total_steps * 45
        
        if subject == STEMSubject.COMPUTER_SCIENCE:
            audience = "Intermediate High School / Intro College Programming"
            approach = "Hands-on project-based coding activities"
        elif subject == STEMSubject.MATH:
            audience = "High School Geometry or Calculus students"
            approach = "Step-by-step mathematical proof and validation"
        elif subject == STEMSubject.PHYSICS:
            audience = "High School Algebra-based Physics students"
            approach = "Formula derivation and interactive simulation references"
        else:
            audience = "General STEM Secondary Education"
            approach = "Concept identification and vocabulary definitions"
            
        return InstructionalMetadata(
            total_estimated_minutes=total_mins,
            target_audience_profile=audience,
            instructional_approach=approach
        )
