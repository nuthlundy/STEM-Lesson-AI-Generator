from services.lesson_planning.schemas import DifferentiationBlock
from services.lesson_planning.differentiation.profiles import LearnerProfiles
from services.lesson_planning.differentiation.strategies import DifferentiationStrategies
from services.lesson_planning.differentiation.accommodations import Accommodations
from services.lesson_planning.differentiation.enrichment import Enrichment
from services.lesson_planning.differentiation.intervention import Intervention

class DifferentiationGenerator:
    """Generates default differentiated instruction mappings for lesson plans."""
    
    @staticmethod
    def generate_default() -> DifferentiationBlock:
        profiles = LearnerProfiles.get_all_profiles()
        accommodations = Accommodations.get_default_accommodations()
        strategies = DifferentiationStrategies.get_default_strategies()
        enrichment = Enrichment.get_default_enrichment()
        intervention = Intervention.get_default_intervention()
        
        return DifferentiationBlock(
            learner_profiles=profiles,
            accommodations=accommodations,
            intervention_strategies=intervention,
            enrichment_recommendations=enrichment
        )
