from typing import List
from core.workflow.stage import WorkflowStage

class Pipeline:
    def __init__(self, name: str):
        self.name = name
        self.stages: List[WorkflowStage] = []

    def add_stage(self, stage: WorkflowStage) -> None:
        self.stages.append(stage)
