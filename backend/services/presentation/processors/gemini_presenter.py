from services.presentation.interfaces.presenter import PresenterInterface
from services.presentation.schemas import PresentationSessionModel
from services.presentation.processors.deterministic_presenter import DeterministicPresenter

class GeminiPresenter(PresenterInterface):
    def __init__(self, fallback_presenter: PresenterInterface = None):
        self.fallback = fallback_presenter or DeterministicPresenter()

    def before_present(self, session_path: str) -> None:
        self.fallback.before_present(session_path)

    def present(self, session_path: str) -> PresentationSessionModel:
        session = self.fallback.present(session_path)
        session.metadata["ai_presentation_assistant_active"] = True
        return session

    def after_present(self, session: PresentationSessionModel) -> None:
        self.fallback.after_present(session)
