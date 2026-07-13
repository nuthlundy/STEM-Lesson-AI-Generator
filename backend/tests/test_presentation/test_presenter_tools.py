import unittest
from services.presentation.presenter.notes import PresenterNotesResolver
from services.presentation.presenter.cue_cards import CueCardResolver
from services.presentation.presenter.checklist import TeachingChecklistResolver
from services.presentation.presenter.objectives import LearningObjectivesResolver

class TestPresenterTools(unittest.TestCase):
    def test_notes_generation(self):
        notes = PresenterNotesResolver.get_notes(slide_index=2)
        self.assertIn("slide 2", notes)

    def test_cue_cards(self):
        cards = CueCardResolver.get_cue_cards(slide_index=1)
        self.assertEqual(len(cards), 3)
        self.assertIn("slide 1", cards[0])

    def test_checklist(self):
        checklist = TeachingChecklistResolver.get_checklist()
        self.assertEqual(len(checklist), 5)
        self.assertIn("projector", checklist[0])

    def test_objectives(self):
        objectives = LearningObjectivesResolver.get_objectives()
        self.assertEqual(len(objectives), 3)
        self.assertIn("STEM", objectives[0])

if __name__ == "__main__":
    unittest.main()
