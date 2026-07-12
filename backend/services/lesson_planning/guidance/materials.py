from typing import List

class MaterialsList:
    @staticmethod
    def get_materials(subject: str) -> List[str]:
        return [
            f"Worksheets on {subject.capitalize()}",
            "Calculators or computing tablets",
            "Reference diagrams and lab sheets"
        ]
