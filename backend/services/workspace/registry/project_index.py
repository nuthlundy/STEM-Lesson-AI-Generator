from typing import Dict, List, Optional
from services.workspace.registry.project_metadata import ProjectMetadata

class ProjectIndex:
    def __init__(self) -> None:
        self._index: Dict[str, ProjectMetadata] = {}

    def index_project(self, meta: ProjectMetadata) -> None:
        self._index[meta.project_id] = meta

    def remove_project(self, project_id: str) -> None:
        if project_id in self._index:
            del self._index[project_id]

    def search(self, query: str) -> List[ProjectMetadata]:
        results = []
        for p in self._index.values():
            if query.lower() in p.project_name.lower():
                results.append(p)
        return results

    def lookup(self, project_id: str) -> Optional[ProjectMetadata]:
        return self._index.get(project_id)
