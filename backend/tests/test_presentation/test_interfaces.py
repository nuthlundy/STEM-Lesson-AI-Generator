import unittest
from services.presentation.interfaces.presenter import PresenterInterface
from services.presentation.interfaces.navigator import NavigatorInterface
from services.presentation.interfaces.controller import ControllerInterface
from services.presentation.schemas import PresentationSessionModel

class TestPresentationInterfaces(unittest.TestCase):
    def test_presenter_subclassing(self):
        class MockPresenter(PresenterInterface):
            def before_present(self, session_path: str) -> None:
                pass
            def present(self, session_path: str) -> PresentationSessionModel:
                return PresentationSessionModel(
                    session_id="mock-id",
                    presentation_path=session_path,
                    duration_seconds=3600,
                    slides=[]
                )
            def after_present(self, session: PresentationSessionModel) -> None:
                pass

        p = MockPresenter()
        session = p.present("path")
        self.assertEqual(session.session_id, "mock-id")

    def test_navigator_subclassing(self):
        class MockNavigator(NavigatorInterface):
            def next_slide(self) -> int:
                return 1
            def previous_slide(self) -> int:
                return 0

        n = MockNavigator()
        self.assertEqual(n.next_slide(), 1)
        self.assertEqual(n.previous_slide(), 0)

    def test_controller_subclassing(self):
        called = []
        class MockController(ControllerInterface):
            def start_session(self) -> None:
                called.append("start")
            def end_session(self) -> None:
                called.append("end")

        c = MockController()
        c.start_session()
        c.end_session()
        self.assertEqual(called, ["start", "end"])

if __name__ == "__main__":
    unittest.main()
