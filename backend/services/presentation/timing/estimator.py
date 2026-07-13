from typing import List

class PresentationEstimator:
    @staticmethod
    def estimate_slide_duration(slide_title: str, text_word_count: int) -> int:
        speaking_time = text_word_count // 2
        return 30 + speaking_time

    @staticmethod
    def estimate_total_duration(slide_word_counts: List[int]) -> int:
        return sum(PresentationEstimator.estimate_slide_duration("", wc) for wc in slide_word_counts)
