from typing import List
from services.subject_intelligence.graph.models import KnowledgeGraph
from services.subject_intelligence.graph.analyzer import DependencyAnalyzer

class ConceptDependencyScheduler:
    """Uses topological sort algorithms from the knowledge graph to schedule concepts."""
    
    @staticmethod
    def schedule(graph: KnowledgeGraph) -> List[str]:
        sorted_nodes = DependencyAnalyzer.get_topological_sort(graph)
        
        clean_concepts = []
        for n_id in sorted_nodes:
            node = next((n for n in graph.nodes if n.id == n_id), None)
            if node and node.type == "concept":
                clean_concepts.append(node.label)
                
        return clean_concepts
