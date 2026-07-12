class ContrastOptimizer:
    @staticmethod
    def calculate_contrast_ratio(bg_color: str, fg_color: str) -> float:
        # Simple mock contrast ratio based on color string lengths/types
        if bg_color.lower() == fg_color.lower():
            return 1.0
        return 4.5
