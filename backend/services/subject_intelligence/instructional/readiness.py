from typing import List
from services.subject_intelligence.instructional.schemas import ReadinessReport
from services.subject_intelligence.graph.models import KnowledgeGraph
from services.subject_intelligence.graph.analyzer import DependencyAnalyzer

class LessonReadinessAnalyzer:
    """Evaluates loops, gaps, and coverage parameters to establish lesson readiness."""
    
    @staticmethod
    def analyze(graph: KnowledgeGraph, gaps_count: int) -> ReadinessReport:
        cycles = DependencyAnalyzer.detect_cycles(graph)
        
        base_score = 1.0
        if cycles:
            base_score = 0.2
        else:
            base_score -= gaps_count * 0.1
            base_score = max(0.0, base_score)
            
        ready = base_score >= 0.7 and len(cycles) == 0
        
        return ReadinessReport(
            ready=ready,
            gaps_count=gaps_count,
            prerequisite_cycles=cycles,
            readiness_score=round(base_score, 2)
        )
