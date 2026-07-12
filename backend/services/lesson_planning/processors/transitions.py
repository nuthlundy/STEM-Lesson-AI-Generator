from typing import List
from services.lesson_planning.schemas import Transition

class TransitionGenerator:
    """Generates connecting transitions between consecutive lesson timeline segments."""
    
    @staticmethod
    def generate_transitions(timeline: List[str]) -> List[Transition]:
        transitions = []
        for idx in range(len(timeline) - 1):
            from_sec = timeline[idx]
            to_sec = timeline[idx + 1]
            note = f"Moving from {from_sec} to {to_sec}: Let's connect our conceptual progress to the next segment."
            transitions.append(Transition(
                from_section=from_sec,
                to_section=to_sec,
                transition_notes=note
            ))
        return transitions
