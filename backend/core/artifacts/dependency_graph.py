from typing import Dict, List, Set
from core.artifacts.exceptions import DependencyCycleError, MissingDependencyError

class DependencyGraph:
    def __init__(self):
        self.adj_list: Dict[str, Set[str]] = {}

    def add_node(self, node: str) -> None:
        if node not in self.adj_list:
            self.adj_list[node] = set()

    def add_edge(self, node: str, dependency: str) -> None:
        self.add_node(node)
        self.adj_list[node].add(dependency)

    def get_dependencies(self, node: str) -> List[str]:
        return list(self.adj_list.get(node, set()))

    def detect_missing_dependencies(self) -> List[str]:
        missing = set()
        for node, deps in self.adj_list.items():
            for dep in deps:
                if dep not in self.adj_list:
                    missing.add(dep)
        return list(missing)

    def has_cycle(self) -> bool:
        visited: Dict[str, int] = {node: 0 for node in self.adj_list}
        
        def dfs(node: str) -> bool:
            visited[node] = 1
            for dep in self.adj_list.get(node, []):
                if dep not in visited:
                    continue
                if visited[dep] == 1:
                    return True
                if visited[dep] == 0:
                    if dfs(dep):
                        return True
            visited[node] = 2
            return False

        for node in self.adj_list:
            if visited[node] == 0:
                if dfs(node):
                    return True
        return False

    def topological_sort(self) -> List[str]:
        if self.has_cycle():
            raise DependencyCycleError("Dependency cycle detected; cannot topologically sort.")
            
        visited: Set[str] = set()
        stack: List[str] = []

        def dfs(node: str) -> None:
            visited.add(node)
            for dep in self.adj_list.get(node, []):
                if dep in self.adj_list and dep not in visited:
                    dfs(dep)
            stack.append(node)

        for node in sorted(self.adj_list.keys()):
            if node not in visited:
                dfs(node)
                
        return stack
