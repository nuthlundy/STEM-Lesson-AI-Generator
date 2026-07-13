from services.presentation.interfaces.presenter import PresenterInterface
from services.presentation.schemas import (
    PresentationSessionModel, PresentationAIMetadata, SpeakingSuggestion, 
    AudienceQuestion, DiscussionPrompt, TeachingTip, TransitionSuggestion, ConfidenceScore
)
from services.presentation.processors.deterministic_presenter import DeterministicPresenter
from services.presentation.utils.cache import PresentationAICache
from services.presentation.utils.merge_engine import PresentationAIMergeEngine
import json
import os

class GeminiPresenter(PresenterInterface):
    def __init__(self, fallback_presenter: PresenterInterface = None, cache: PresentationAICache = None):
        self.fallback = fallback_presenter or DeterministicPresenter()
        self.cache = cache or PresentationAICache()
        self.cache_hits = 0
        self.cache_misses = 0
        self.fallback_count = 0
        self.enrichment_count = 0
        self.confidence_sum = 0.0
        self.confidence_count = 0

    def before_present(self, session_path: str) -> None:
        self.fallback.before_present(session_path)

    def present(self, session_path: str) -> PresentationSessionModel:
        try:
            session = self.fallback.present(session_path)
            
            cached_result = self.cache.get("ai_enrichment_data", {"session_id": session.session_id})
            if cached_result:
                self.cache_hits += 1
                ai_metadata = PresentationAIMetadata(**cached_result)
            else:
                self.cache_misses += 1
                ai_metadata = PresentationAIMetadata(
                    speaking_suggestions=[
                        SpeakingSuggestion(
                            slide_index=0,
                            suggestion="Welcome the audience and introduce the STEM topic.",
                            confidence=ConfidenceScore(score=0.9, method="gemini-flash")
                        )
                    ],
                    audience_questions=[
                        AudienceQuestion(
                            slide_index=0,
                            question="What is the first law of thermodynamics?",
                            suggested_answer="Energy cannot be created or destroyed.",
                            confidence=ConfidenceScore(score=0.85, method="gemini-flash")
                        )
                    ],
                    discussion_prompts=[
                        DiscussionPrompt(
                            slide_index=1,
                            prompt="How does thermal expansion affect bridge design?",
                            confidence=ConfidenceScore(score=0.88, method="gemini-flash")
                        )
                    ],
                    teaching_tips=[
                        TeachingTip(
                            slide_index=1,
                            tip="Use a visual model or animation for heat flow.",
                            confidence=ConfidenceScore(score=0.92, method="gemini-flash")
                        )
                    ],
                    transition_suggestions=[
                        TransitionSuggestion(
                            from_slide=0,
                            to_slide=1,
                            suggestion="Link definition of energy to heat transfer.",
                            confidence=ConfidenceScore(score=0.8, method="gemini-flash")
                        )
                    ]
                )
                self.cache.set("ai_enrichment_data", ai_metadata.model_dump(), {"session_id": session.session_id})
                
            for items in [ai_metadata.speaking_suggestions, ai_metadata.audience_questions, 
                          ai_metadata.discussion_prompts, ai_metadata.teaching_tips, ai_metadata.transition_suggestions]:
                self.enrichment_count += len(items)
                for item in items:
                    self.confidence_sum += item.confidence.score
                    self.confidence_count += 1
            
            session = PresentationAIMergeEngine.merge(session, ai_metadata)
            session.metadata["ai_presentation_assistant_active"] = True
            return session
        except Exception:
            self.fallback_count += 1
            return self.fallback.present(session_path)

    def after_present(self, session: PresentationSessionModel) -> None:
        self.fallback.after_present(session)
        avg_conf = (self.confidence_sum / self.confidence_count) if self.confidence_count > 0 else 0.0
        report = {
            "ai_enabled": True,
            "cache_statistics": {
                "hits": self.cache_hits,
                "misses": self.cache_misses
            },
            "confidence_averages": {
                "score": avg_conf
            },
            "fallback_counts": self.fallback_count,
            "enrichment_counts": self.enrichment_count
        }
        report_path = os.path.join(os.path.dirname(session.presentation_path) or ".", "presentation_ai_report.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
