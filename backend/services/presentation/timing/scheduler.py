from typing import Dict, Any, List

class PresentationScheduler:
    def __init__(self, estimated_duration: int = 3600) -> None:
        self.estimated_duration = estimated_duration

    def get_section_timings(self, total_slides: int) -> List[Dict[str, Any]]:
        if total_slides <= 0:
            return []
        per_slide = self.estimated_duration // total_slides
        return [
            {"slide_index": i, "estimated_duration_seconds": per_slide}
            for i in range(total_slides)
        ]
