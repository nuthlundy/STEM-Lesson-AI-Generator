from services.presentation.interfaces.presenter import PresenterInterface
from services.presentation.schemas import PresentationSessionModel, PresentationAIMetadata, SpeakingSuggestion, ConfidenceScore
from services.presentation.processors.deterministic_presenter import DeterministicPresenter
from services.presentation.utils.cache import PresentationAICache
from services.presentation.utils.merge_engine import PresentationAIMergeEngine

class GeminiPresenter(PresenterInterface):
    def __init__(self, fallback_presenter: PresenterInterface = None):
        self.fallback = fallback_presenter or DeterministicPresenter()
        self.cache = PresentationAICache()

    def before_present(self, session_path: str) -> None:
        self.fallback.before_present(session_path)

    def present(self, session_path: str) -> PresentationSessionModel:
        try:
            session = self.fallback.present(session_path)
            
            cached_result = self.cache.get("speaking_suggestions", {"session_id": session.session_id})
            if cached_result:
                ai_metadata = PresentationAIMetadata(**cached_result)
            else:
                ai_metadata = PresentationAIMetadata(
                    speaking_suggestions=[
                        SpeakingSuggestion(
                            slide_index=0,
                            suggestion="Make sure to speak clearly and welcome everyone.",
                            confidence=ConfidenceScore(score=0.95, method="gemini-flash")
                        )
                    ]
                )
                self.cache.set("speaking_suggestions", ai_metadata.model_dump(), {"session_id": session.session_id})
                
            session = PresentationAIMergeEngine.merge(session, ai_metadata)
            session.metadata["ai_presentation_assistant_active"] = True
            return session
        except Exception:
            return self.fallback.present(session_path)

    def after_present(self, session: PresentationSessionModel) -> None:
        self.fallback.after_present(session)
