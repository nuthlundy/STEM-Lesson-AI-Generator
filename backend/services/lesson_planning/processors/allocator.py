from typing import Dict

class TimeAllocationEngine:
    """Allocates logical durations for the 10 required lesson sections."""
    
    DEFAULT_DURATION_MAP = {
        "Introduction": 5,
        "Learning Objectives": 3,
        "Prior Knowledge": 5,
        "Lesson Development": 20,
        "Guided Practice": 15,
        "Independent Practice": 15,
        "Review": 5,
        "Reflection": 5,
        "Homework Placeholder": 2,
        "Closing": 5
    }
    
    @staticmethod
    def allocate_durations(total_minutes: int) -> Dict[str, int]:
        if total_minutes <= 0:
            total_minutes = 60
            
        base_total = sum(TimeAllocationEngine.DEFAULT_DURATION_MAP.values())
        allocated = {}
        accumulated = 0
        
        keys = list(TimeAllocationEngine.DEFAULT_DURATION_MAP.keys())
        for idx, key in enumerate(keys):
            if idx == len(keys) - 1:
                allocated[key] = max(1, total_minutes - accumulated)
            else:
                share = round((TimeAllocationEngine.DEFAULT_DURATION_MAP[key] / base_total) * total_minutes)
                share = max(1, share)
                allocated[key] = share
                accumulated += share
                
        return allocated
