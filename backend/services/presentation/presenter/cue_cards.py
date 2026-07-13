from typing import List

class CueCardResolver:
    @staticmethod
    def get_cue_cards(slide_index: int) -> List[str]:
        return [
            f"Introduce main point of slide {slide_index}",
            "Ask students for feedback",
            "Transition to the next topic"
        ]
