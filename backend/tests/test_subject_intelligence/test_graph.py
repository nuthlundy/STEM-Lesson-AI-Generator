import unittest
from services.subject_intelligence.graph.models import KnowledgeGraph, GraphNode, GraphEdge
from services.subject_intelligence.graph.builder import GraphBuilder
from services.subject_intelligence.graph.analyzer import DependencyAnalyzer
from services.subject_intelligence.interfaces.engine import SubjectIntelligenceResult, EnrichedSubjectDocumentBlock
from services.subject_intelligence.schemas import SubjectMetadata
from services.language_intelligence.interfaces import LinguisticMetadata, SemanticRole
from services.document_intelligence.interfaces import DocumentMetadata, DocumentBlock
from services.subject_intelligence.constants import STEMSubject

class TestSubjectKnowledgeGraph(unittest.TestCase):
    def test_graph_builder_and_analyzer(self):
        # 1. Build a mock SubjectIntelligenceResult
        meta = DocumentMetadata(
            job_id="test-job-graph",
            original_filename="test.pdf",
            total_pages=1,
            processing_time_sec=1.0,
            requires_ocr=False
        )
        
        # Block 1: Calculus
        sub_meta1 = SubjectMetadata(
            subject=STEMSubject.MATH,
            topic="Calculus",
            prerequisites=["Algebra"],
            vocabulary=["derivative"],
            processing_provider="deterministic"
        )
        ling1 = LinguisticMetadata(
            original_text="F(x) derivative",
            cleaned_text="F(x) derivative",
            semantic_role=SemanticRole.UNKNOWN,
            language="en",
            processing_provider="deterministic"
        )
        block1 = EnrichedSubjectDocumentBlock(
            block_id="b1",
            block_type="paragraph",
            text="F(x) derivative",
            page_number=1,
            source="native_pdf",
            language_metadata=ling1,
            subject_metadata=sub_meta1
        )
        
        result = SubjectIntelligenceResult(metadata=meta, blocks=[block1])
        
        # 2. Build the Graph
        graph = GraphBuilder.build(result)
        
        # Nodes: block b1, topic Calculus, topic Algebra, vocabulary derivative
        node_ids = {n.id for n in graph.nodes}
        self.assertIn("b1", node_ids)
        self.assertIn("topic_calculus", node_ids)
        self.assertIn("topic_algebra", node_ids)
        self.assertIn("vocab_derivative", node_ids)
        
        # Edges
        edge_types = {e.type for e in graph.edges}
        self.assertIn("contains", edge_types) # topic_calculus -> b1
        self.assertIn("prerequisite", edge_types) # topic_algebra -> topic_calculus
        self.assertIn("illustrates", edge_types) # b1 -> vocab_derivative

        # 3. Analyze Prerequisite Dependencies
        # Cycles check (should be empty for this graph)
        cycles = DependencyAnalyzer.detect_cycles(graph)
        self.assertEqual(len(cycles), 0)
        
        # Topological Sort
        sorted_nodes = DependencyAnalyzer.get_topological_sort(graph)
        # Algebra must appear BEFORE Calculus since Algebra is a prerequisite of Calculus
        idx_alg = sorted_nodes.index("topic_algebra")
        idx_calc = sorted_nodes.index("topic_calculus")
        self.assertTrue(idx_alg < idx_calc)

    def test_cycle_detection(self):
        # Build a graph with a loop dependency: A -> B -> C -> A
        nodes = [
            GraphNode(id="A", label="A", type="concept"),
            GraphNode(id="B", label="B", type="concept"),
            GraphNode(id="C", label="C", type="concept"),
        ]
        edges = [
            GraphEdge(source="A", target="B", type="prerequisite"),
            GraphEdge(source="B", target="C", type="prerequisite"),
            GraphEdge(source="C", target="A", type="prerequisite"),
        ]
        graph = KnowledgeGraph(nodes=nodes, edges=edges)
        
        cycles = DependencyAnalyzer.detect_cycles(graph)
        self.assertEqual(len(cycles), 1)
        self.assertIn("A", cycles[0])
        self.assertIn("B", cycles[0])
        self.assertIn("C", cycles[0])

if __name__ == "__main__":
    unittest.main()
