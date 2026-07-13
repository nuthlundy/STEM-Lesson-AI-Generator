import json
import os
from typing import Dict, Any
from services.presentation.navigation.controller import NavigationController
from services.presentation.timing.timer import PresentationTimer
from services.presentation.presenter.checklist import TeachingChecklistResolver
from services.presentation.presenter.objectives import LearningObjectivesResolver

class PresentationSessionBuilder:
    @staticmethod
    def build_delivery_session(
        workspace_root: str,
        navigation: NavigationController,
        timer: PresentationTimer,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        delivery_data = {
            "navigation_state": {
                "current_slide": navigation.navigator.current_slide(),
                "history": navigation.get_history(),
                "bookmarks": navigation.get_bookmarks()
            },
            "presenter_tools": {
                "checklist": TeachingChecklistResolver.get_checklist(),
                "objectives": LearningObjectivesResolver.get_objectives()
            },
            "timing_information": {
                "elapsed_seconds": timer.get_elapsed_seconds(),
                "estimated_total_seconds": navigation.navigator.total_slides * 300
            },
            "session_metadata": metadata
        }
        
        output_path = os.path.join(workspace_root, "presentation_delivery.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(delivery_data, f, indent=2)
            
        return delivery_data
