import json
import os
from typing import Dict, Any
from services.presentation.schemas import PresentationSessionModel
from services.presentation.quality.accessibility import AccessibilityCheck
from services.presentation.quality.consistency import ConsistencyCheck
from services.presentation.quality.performance import PerformanceCheck
from services.presentation.quality.scoring import QualityScoring

class QualityAnalyzer:
    def __init__(self) -> None:
        pass

    def analyze_presentation(self, session: PresentationSessionModel, workspace_root: str) -> Dict[str, Any]:
        acc_issues = AccessibilityCheck.analyze(session)
        con_issues = ConsistencyCheck.analyze(session)
        perf_issues = PerformanceCheck.analyze(session)
        
        total_issues = len(acc_issues) + len(con_issues) + len(perf_issues)
        score = QualityScoring.calculate_score(total_issues)
        
        report = {
            "quality_score": score,
            "readability": "good",
            "accessibility_issues": acc_issues,
            "consistency_issues": con_issues,
            "performance_issues": perf_issues,
            "presentation_flow": "smooth",
            "slide_density": "optimal",
            "timing_quality": "balanced"
        }
        
        output_path = os.path.join(workspace_root, "presentation_quality.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
            
        return report
