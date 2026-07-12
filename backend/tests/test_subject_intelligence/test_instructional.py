import unittest
from services.subject_intelligence.instructional.scheduler import ConceptDependencyScheduler
from services.subject_intelligence.instructional.sequence import LearningSequenceGenerator
from services.subject_intelligence.instructional.gap_detection import GapDetectionEngine
from services.subject_intelligence.instructional.readiness import LessonReadinessAnalyzer
from services.subject_intelligence.instructional.metadata import InstructionalMetadataGenerator
from services.subject_intelligence.instructional.summary import SubjectSummaryGenerator
from services.subject_intelligence.graph.models import KnowledgeGraph, GraphNode, GraphEdge
from services.subject_intelligence.curriculum.schemas import LearningObjective
from services.subject_intelligence.constants import STEMSubject

class TestInstructionalModeling(unittest.TestCase):
    def test_concept_dependency_scheduler(self):
        # Algebra -> Calculus
        nodes = [
            GraphNode(id="topic_algebra", label="Algebra", type="concept"),
            GraphNode(id="topic_calculus", label="Calculus", type="concept"),
        ]
        edges = [
            GraphEdge(source="topic_algebra", target="topic_calculus", type="prerequisite")
        ]
        graph = KnowledgeGraph(nodes=nodes, edges=edges)
        
        scheduled = ConceptDependencyScheduler.schedule(graph)
        self.assertEqual(scheduled, ["Algebra", "Calculus"])

    def test_learning_sequence_generator(self):
        # Mock objectives
        objs = [
            LearningObjective(
                id="lo_1",
                description="Apply Algebra to solve equations.",
                bloom_level="Apply",
                mapped_concepts=["Algebra"]
            )
        ]
        
        sequence = LearningSequenceGenerator.generate_sequence(["Algebra"], objs)
        self.assertEqual(len(sequence), 1)
        self.assertEqual(sequence[0].concept, "Algebra")
        self.assertIn("Apply Algebra to solve equations.", sequence[0].objectives)

    def test_gap_detection(self):
        covered = ["Calculus"]
        prereqs = {"Calculus": ["Algebra", "Trigonometry"]}
        
        gaps = GapDetectionEngine.detect_gaps(covered, prereqs)
        self.assertEqual(gaps, ["Algebra", "Trigonometry"])

    def test_lesson_readiness_analyzer(self):
        # Ready (no cycles, no gaps)
        nodes = [GraphNode(id="topic_algebra", label="Algebra", type="concept")]
        graph = KnowledgeGraph(nodes=nodes, edges=[])
        report = LessonReadinessAnalyzer.analyze(graph, 0)
        self.assertTrue(report.ready)
        self.assertEqual(report.readiness_score, 1.0)
        
        # Unready (3 gaps)
        report2 = LessonReadinessAnalyzer.analyze(graph, 3)
        self.assertTrue(report2.readiness_score == 0.7) # 1.0 - 0.3 = 0.7 (still ready as score is >= 0.7)
        
        # Unready (critical cycle)
        edges = [
            GraphEdge(source="topic_algebra", target="topic_calculus", type="prerequisite"),
            GraphEdge(source="topic_calculus", target="topic_algebra", type="prerequisite")
        ]
        nodes.append(GraphNode(id="topic_calculus", label="Calculus", type="concept"))
        graph_cycle = KnowledgeGraph(nodes=nodes, edges=edges)
        report3 = LessonReadinessAnalyzer.analyze(graph_cycle, 0)
        self.assertFalse(report3.ready)
        self.assertEqual(report3.readiness_score, 0.2)

if __name__ == "__main__":
    unittest.main()
