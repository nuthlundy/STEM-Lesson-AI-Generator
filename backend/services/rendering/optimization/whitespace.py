class WhitespaceOptimizer:
    @staticmethod
    def calculate_whitespace_ratio(filled_area: float, total_area: float) -> float:
        if total_area <= 0:
            return 0.0
        return (total_area - filled_area) / total_area
