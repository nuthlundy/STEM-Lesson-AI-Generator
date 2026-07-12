from typing import List

class Misconceptions:
    @staticmethod
    def get_warnings(subject: str) -> List[str]:
        return [
            f"Confusing correlation with causation in {subject} analysis.",
            "Underestimating experimental error margin.",
            "Assuming physical properties scale linearly."
        ]
