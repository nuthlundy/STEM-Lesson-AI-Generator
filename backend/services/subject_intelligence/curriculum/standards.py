from typing import List
from services.subject_intelligence.constants import STEMSubject
from services.subject_intelligence.curriculum.schemas import StandardAlignment

class StandardsAlignmentEngine:
    """Matches subject domains and keywords to standardized curriculum definitions."""
    
    STANDARDS_REGISTRY = {
        STEMSubject.PHYSICS: [
            StandardAlignment(standard_code="NGSS.HS-PS2-1", description="Analyze data to support the claim that Newton's second law of motion describes the mathematical relationship among the net force on a macroscopic object, its mass, and its acceleration.", aligned_concepts=["Mechanics", "force", "mass", "acceleration"]),
            StandardAlignment(standard_code="NGSS.HS-PS3-1", description="Create a computational model to calculate the change in the energy of one component in a system when the change in energy of the other component(s) and energy flows in and out of the system are known.", aligned_concepts=["Thermodynamics", "energy", "heat"])
        ],
        STEMSubject.MATH: [
            StandardAlignment(standard_code="CCSS.MATH.HSF-BF.A.1", description="Write a function that describes a relationship between two quantities.", aligned_concepts=["Calculus", "Algebra", "function", "derivative"])
        ],
        STEMSubject.CHEMISTRY: [
            StandardAlignment(standard_code="NGSS.HS-PS1-7", description="Use mathematical representations to support the claim that atoms, and therefore mass, are conserved during a chemical reaction.", aligned_concepts=["General Chemistry", "Organic Chemistry", "reaction", "stoichiometry"])
        ],
        STEMSubject.COMPUTER_SCIENCE: [
            StandardAlignment(standard_code="CSTA.3A-AP-17", description="Decompose problems into smaller components through systematic analysis, using constructs such as procedures, modules, and/or APIs.", aligned_concepts=["Algorithms & Data Structures", "Software Engineering", "recursion", "class"])
        ]
    }
    
    @staticmethod
    def get_alignments(subject: STEMSubject, extracted_concepts: List[str]) -> List[StandardAlignment]:
        alignments = []
        registry = StandardsAlignmentEngine.STANDARDS_REGISTRY.get(subject, [])
        for std in registry:
            intersect = set(std.aligned_concepts).intersection(set(extracted_concepts))
            if intersect:
                alignments.append(StandardAlignment(
                    standard_code=std.standard_code,
                    description=std.description,
                    aligned_concepts=list(intersect)
                ))
        return alignments
