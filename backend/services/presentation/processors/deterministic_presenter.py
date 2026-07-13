import json
from services.presentation.interfaces.presenter import PresenterInterface
from services.presentation.schemas import PresentationSessionModel

class DeterministicPresenter(PresenterInterface):
    def before_present(self, session_path: str) -> None:
        pass

    def present(self, session_path: str) -> PresentationSessionModel:
        self.before_present(session_path)
        with open(session_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        session = PresentationSessionModel(**data)
        self.after_present(session)
        return session

    def after_present(self, session: PresentationSessionModel) -> None:
        pass
