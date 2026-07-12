from typing import Dict, List
from core.artifacts.artifact import Artifact
from core.artifacts.resolver import ArtifactResolver
from core.artifacts.validator import ArtifactValidator
from core.artifacts.dependency_graph import DependencyGraph
from core.artifacts.exceptions import (
    DuplicateArtifactError,
    ArtifactNotFoundError,
    MissingDependencyError,
    ValidationError
)

class ArtifactRegistry:
    """Centralized registry managing pipelines artifacts, metadata, and dependencies."""
    
    def __init__(self, workspace_root: str = "."):
        self._artifacts: Dict[str, Artifact] = {}
        self._resolver = ArtifactResolver(workspace_root)
        self._graph = DependencyGraph()

    def register(self, artifact: Artifact) -> None:
        """Registers a new artifact and updates the dependency graph."""
        if artifact.artifact_id in self._artifacts:
            raise DuplicateArtifactError(f"Artifact '{artifact.artifact_id}' is already registered.")
            
        ArtifactValidator.validate(artifact)
        
        self._artifacts[artifact.artifact_id] = artifact
        self._graph.add_node(artifact.artifact_id)
        for dep in artifact.dependencies:
            self._graph.add_edge(artifact.artifact_id, dep)

    def get(self, artifact_id: str) -> Artifact:
        """Retrieves artifact metadata, raising ArtifactNotFoundError if missing."""
        if artifact_id not in self._artifacts:
            raise ArtifactNotFoundError(f"Artifact '{artifact_id}' not found in registry.")
        return self._artifacts[artifact_id]

    def exists(self, artifact_id: str) -> bool:
        """Checks if artifact metadata exists and its file physically exists on disk."""
        if artifact_id not in self._artifacts:
            return False
        artifact = self._artifacts[artifact_id]
        return self._resolver.exists(artifact.relative_path)

    def resolve(self, artifact_id: str) -> str:
        """Returns the absolute file path for a registered artifact."""
        artifact = self.get(artifact_id)
        return self._resolver.resolve_path(artifact.relative_path)

    def list(self) -> List[Artifact]:
        """Lists all registered artifacts."""
        return list(self._artifacts.values())

    def validate(self, artifact_id: str) -> None:
        """Validates schema properties and verifies that all dependencies are registered."""
        artifact = self.get(artifact_id)
        ArtifactValidator.validate(artifact)
        
        for dep in artifact.dependencies:
            if dep not in self._artifacts:
                raise MissingDependencyError(
                    f"Artifact '{artifact_id}' references missing dependency: '{dep}'."
                )

        from core.events.event import Event
        from core.events.dispatcher import get_event_dispatcher
        import datetime
        import uuid
        
        get_event_dispatcher().publish(Event(
            event_id=str(uuid.uuid4()),
            event_name="ArtifactValidated",
            source_engine=artifact.engine_name,
            timestamp=datetime.datetime.now().isoformat(),
            payload={"artifact_id": artifact_id}
        ))

    def dependencies(self, artifact_id: str) -> List[str]:
        """Lists all artifact IDs that this artifact depends on."""
        artifact = self.get(artifact_id)
        return artifact.dependencies

    def consumers(self, artifact_id: str) -> List[str]:
        """Lists all artifact IDs that consume this artifact."""
        self.get(artifact_id)
        consumers_list = []
        for art in self._artifacts.values():
            if artifact_id in art.dependencies:
                consumers_list.append(art.artifact_id)
        return consumers_list

    def producers(self, artifact_id: str) -> List[str]:
        """Lists the engine names that produce this artifact."""
        artifact = self.get(artifact_id)
        return [artifact.produced_by]

def get_canonical_registry(workspace_root: str = ".") -> ArtifactRegistry:
    registry = ArtifactRegistry(workspace_root)
    
    registry.register(Artifact(
        artifact_id="lesson.json",
        artifact_name="Base Lesson Document",
        schema_version="1.0",
        engine_name="Document Intelligence Engine",
        engine_version="1.0",
        file_name="lesson.json",
        relative_path="lesson.json",
        produced_by="Document Intelligence Engine",
        consumed_by=["Language Intelligence Engine", "Subject Intelligence Engine"],
        dependencies=[],
        created_at="2026-07-12T00:00:00Z",
        checksum="sha256-mocked-checksum-lesson",
        description="Text extracted from document intelligence engine."
    ))

    registry.register(Artifact(
        artifact_id="lesson_language.json",
        artifact_name="Language Analysis Result",
        schema_version="1.0",
        engine_name="Language Intelligence Engine",
        engine_version="1.0",
        file_name="lesson_language.json",
        relative_path="lesson_language.json",
        produced_by="Language Intelligence Engine",
        consumed_by=["Subject Intelligence Engine"],
        dependencies=["lesson.json"],
        created_at="2026-07-12T00:00:00Z",
        checksum="sha256-mocked-checksum-language",
        description="Reading difficulty and language metadata."
    ))

    registry.register(Artifact(
        artifact_id="lesson_subject.json",
        artifact_name="Subject Metadata",
        schema_version="1.0",
        engine_name="Subject Intelligence Engine",
        engine_version="1.0",
        file_name="lesson_subject.json",
        relative_path="lesson_subject.json",
        produced_by="Subject Intelligence Engine",
        consumed_by=["Lesson Planning Engine"],
        dependencies=["lesson_language.json"],
        created_at="2026-07-12T00:00:00Z",
        checksum="sha256-mocked-checksum-subject",
        description="Extracted subjects, topics, and difficulty metrics."
    ))

    registry.register(Artifact(
        artifact_id="lesson_subject_graph.json",
        artifact_name="Subject Knowledge Graph",
        schema_version="1.0",
        engine_name="Subject Intelligence Engine",
        engine_version="1.0",
        file_name="lesson_subject_graph.json",
        relative_path="lesson_subject_graph.json",
        produced_by="Subject Intelligence Engine",
        consumed_by=["Lesson Planning Engine"],
        dependencies=["lesson_subject.json"],
        created_at="2026-07-12T00:00:00Z",
        checksum="sha256-mocked-checksum-graph",
        description="Dependency and prerequisite relations for subject knowledge graph."
    ))

    registry.register(Artifact(
        artifact_id="lesson_learning_objectives.json",
        artifact_name="Curriculum Standards Alignment Objectives",
        schema_version="1.0",
        engine_name="Subject Intelligence Engine",
        engine_version="1.0",
        file_name="lesson_learning_objectives.json",
        relative_path="lesson_learning_objectives.json",
        produced_by="Subject Intelligence Engine",
        consumed_by=["Lesson Planning Engine"],
        dependencies=["lesson_subject_graph.json"],
        created_at="2026-07-12T00:00:00Z",
        checksum="sha256-mocked-checksum-objectives",
        description="Learning objectives mapped to Bloom Taxonomy level and CCSS/NGSS standards."
    ))

    registry.register(Artifact(
        artifact_id="lesson_instructional_model.json",
        artifact_name="Instructional Sequencing Metadata",
        schema_version="1.0",
        engine_name="Subject Intelligence Engine",
        engine_version="1.0",
        file_name="lesson_instructional_model.json",
        relative_path="lesson_instructional_model.json",
        produced_by="Subject Intelligence Engine",
        consumed_by=["Lesson Planning Engine"],
        dependencies=["lesson_learning_objectives.json"],
        created_at="2026-07-12T00:00:00Z",
        checksum="sha256-mocked-checksum-instructional",
        description="Topological schedule order and ready state analyzer feedback."
    ))

    registry.register(Artifact(
        artifact_id="lesson_plan.json",
        artifact_name="Final Lesson Plan Document",
        schema_version="1.0",
        engine_name="Lesson Planning Engine",
        engine_version="1.0",
        file_name="lesson_plan.json",
        relative_path="lesson_plan.json",
        produced_by="Lesson Planning Engine",
        consumed_by=[],
        dependencies=["lesson_instructional_model.json"],
        created_at="2026-07-12T00:00:00Z",
        checksum="sha256-mocked-checksum-plan",
        description="Enriched 10-part instruction models with accommodations and assessments."
    ))
    
    return registry
