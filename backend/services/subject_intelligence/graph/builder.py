from typing import List
from services.subject_intelligence.interfaces.engine import SubjectIntelligenceResult
from services.subject_intelligence.graph.models import KnowledgeGraph, GraphNode, GraphEdge

class GraphBuilder:
    """Builds a KnowledgeGraph structure from processed SubjectIntelligenceResult."""
    
    @staticmethod
    def build(result: SubjectIntelligenceResult) -> KnowledgeGraph:
        nodes = {}
        edges = []
        
        # 1. Process blocks and add nodes + inner concept nodes
        for block in result.blocks:
            # Block Node
            b_id = block.block_id
            nodes[b_id] = GraphNode(
                id=b_id,
                label=f"Block {b_id}",
                type="block",
                properties={
                    "block_type": block.block_type,
                    "page_number": block.page_number
                }
            )
            
            # Subject/Topic/Vocab concept nodes
            meta = block.subject_metadata
            if not meta:
                continue
                
            # Topic Node
            if meta.topic:
                t_id = f"topic_{meta.topic.lower().replace(' ', '_')}"
                if t_id not in nodes:
                    nodes[t_id] = GraphNode(
                        id=t_id,
                        label=meta.topic,
                        type="concept",
                        properties={"subject": meta.subject}
                    )
                # Edge: Topic contains Block
                edges.append(GraphEdge(
                    source=t_id,
                    target=b_id,
                    type="contains",
                    weight=meta.confidence or 1.0
                ))
                
                # Prerequisites relationships (between topics/concepts)
                for prereq in meta.prerequisites:
                    p_id = f"topic_{prereq.lower().replace(' ', '_')}"
                    if p_id not in nodes:
                        nodes[p_id] = GraphNode(
                            id=p_id,
                            label=prereq,
                            type="concept",
                            properties={"subject": meta.subject}
                        )
                    # Edge: Prereq -> Topic
                    edges.append(GraphEdge(
                        source=p_id,
                        target=t_id,
                        type="prerequisite",
                        weight=1.0
                    ))

            # Vocabulary Nodes
            for vocab in meta.vocabulary:
                v_id = f"vocab_{vocab.lower().replace(' ', '_')}"
                if v_id not in nodes:
                    nodes[v_id] = GraphNode(
                        id=v_id,
                        label=vocab,
                        type="vocabulary",
                        properties={"subject": meta.subject}
                    )
                # Edge: Block illustrates Vocabulary
                edges.append(GraphEdge(
                    source=b_id,
                    target=v_id,
                    type="illustrates",
                    weight=1.0
                ))
                
        # Deduplicate edges by source + target + type
        unique_edges = []
        seen = set()
        for e in edges:
            key = (e.source, e.target, e.type)
            if key not in seen:
                seen.add(key)
                unique_edges.append(e)
                
        return KnowledgeGraph(
            nodes=list(nodes.values()),
            edges=unique_edges,
            metadata={
                "job_id": result.metadata.job_id,
                "engine": "Subject Intelligence Engine"
            }
        )
