from typing import List, Dict, Set
from services.subject_intelligence.graph.models import KnowledgeGraph

class DependencyAnalyzer:
    """Performs topological sorting and cycle detection on KnowledgeGraphs."""
    
    @staticmethod
    def detect_cycles(graph: KnowledgeGraph) -> List[List[str]]:
        """
        Detects cycles in prerequisite edges.
        Returns a list of cycles (loops) as list of node IDs.
        """
        adj = {}
        for node in graph.nodes:
            if node.type == "concept":
                adj[node.id] = []
                
        for edge in graph.edges:
            if edge.type == "prerequisite":
                if edge.source in adj and edge.target in adj:
                    adj[edge.source].append(edge.target)
                    
        visited = {} # id -> state (0 = unvisited, 1 = visiting, 2 = visited)
        for node_id in adj:
            visited[node_id] = 0
            
        cycles = []
        path = []
        
        def dfs(node):
            visited[node] = 1 # visiting
            path.append(node)
            for neighbor in adj[node]:
                if visited[neighbor] == 1:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
                elif visited[neighbor] == 0:
                    dfs(neighbor)
            path.pop()
            visited[node] = 2 # visited
            
        for node_id in adj:
            if visited[node_id] == 0:
                dfs(node_id)
                
        return cycles

    @staticmethod
    def get_topological_sort(graph: KnowledgeGraph) -> List[str]:
        """
        Performs topological sorting on concept/topic nodes.
        Returns concept node IDs in dependency-resolved order.
        """
        adj = {}
        for node in graph.nodes:
            if node.type == "concept":
                adj[node.id] = []
                
        for edge in graph.edges:
            if edge.type == "prerequisite":
                if edge.source in adj and edge.target in adj:
                    adj[edge.source].append(edge.target)
                    
        visited = set()
        stack = []
        
        def dfs(node):
            visited.add(node)
            for neighbor in adj[node]:
                if neighbor not in visited:
                    dfs(neighbor)
            stack.append(node)
            
        for node_id in adj:
            if node_id not in visited:
                dfs(node_id)
                
        return stack[::-1]
