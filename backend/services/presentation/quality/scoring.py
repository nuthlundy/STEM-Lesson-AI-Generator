class QualityScoring:
    @staticmethod
    def calculate_score(issues_count: int) -> float:
        return max(0.0, 100.0 - (issues_count * 10.0))
