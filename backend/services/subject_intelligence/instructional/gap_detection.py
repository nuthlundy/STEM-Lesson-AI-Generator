from typing import List, Dict

class GapDetectionEngine:
    """Finds missing prerequisite concepts by comparing requirements against covered topics."""
    
    @staticmethod
    def detect_gaps(covered_concepts: List[str], concept_prereqs: Dict[str, List[str]]) -> List[str]:
        covered_set = {c.lower() for c in covered_concepts}
        gaps = set()
        
        for concept, prereqs in concept_prereqs.items():
            for pr in prereqs:
                if pr.lower() not in covered_set:
                    gaps.add(pr)
                    
        return sorted(list(gaps))
