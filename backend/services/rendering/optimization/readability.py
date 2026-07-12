class ReadabilityOptimizer:
    @staticmethod
    def evaluate_font_readability(font_family: str, size: float) -> bool:
        if size < 10.0:
            return False
        return True
