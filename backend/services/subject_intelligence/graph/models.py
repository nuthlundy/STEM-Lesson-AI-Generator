from pydantic import BaseModel, Field
from typing import List, Literal, Dict, Any

class GraphNode(BaseModel):
    id: str
    label: str
    type: Literal["concept", "block", "formula", "vocabulary"]
    properties: Dict[str, Any] = Field(default_factory=dict)

class GraphEdge(BaseModel):
    source: str
    target: str
    type: Literal["prerequisite", "contains", "illustrates"]
    weight: float = 1.0

class KnowledgeGraph(BaseModel):
    nodes: List[GraphNode] = Field(default_factory=list)
    edges: List[GraphEdge] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
