from typing import List

class TeachingChecklistResolver:
    @staticmethod
    def get_checklist() -> List[str]:
        return [
            "Verify projector display is active",
            "Distribute student worksheets",
            "Start the presentation timer",
            "Take attendance",
            "Check speaker volume"
        ]
