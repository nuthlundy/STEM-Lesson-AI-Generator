from typing import Dict, List, Any

class BloomTaxonomy:
    REMEMBERING = "Remembering"
    UNDERSTANDING = "Understanding"
    APPLYING = "Applying"
    ANALYZING = "Analyzing"
    EVALUATING = "Evaluating"
    CREATING = "Creating"

    @staticmethod
    def get_levels() -> List[str]:
        return [
            BloomTaxonomy.REMEMBERING,
            BloomTaxonomy.UNDERSTANDING,
            BloomTaxonomy.APPLYING,
            BloomTaxonomy.ANALYZING,
            BloomTaxonomy.EVALUATING,
            BloomTaxonomy.CREATING
        ]

    @staticmethod
    def calculate_distribution(alignments: List[Any]) -> Dict[str, float]:
        counts = {level: 0 for level in BloomTaxonomy.get_levels()}
        total = len(alignments)
        if total == 0:
            return {level: 0.0 for level in BloomTaxonomy.get_levels()}
        
        for align in alignments:
            level = align.bloom_level
            if level in counts:
                counts[level] += 1
        
        return {level: round(counts[level] / total, 2) for level in BloomTaxonomy.get_levels()}
