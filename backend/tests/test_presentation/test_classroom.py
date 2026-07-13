import unittest
import tempfile
import os
from services.presentation.classroom import ClassroomInteractionManager
from services.presentation.engine import PresentationEngine

class TestClassroomInteraction(unittest.TestCase):
    def setUp(self):
        self.mgr = ClassroomInteractionManager()

    def test_manager_instantiation(self):
        self.assertIsNotNone(self.mgr.questions)
        self.assertIsNotNone(self.mgr.polls)
        self.assertIsNotNone(self.mgr.activities)
        self.assertIsNotNone(self.mgr.discussions)
        self.assertIsNotNone(self.mgr.feedback)
        self.assertIsNotNone(self.mgr.responses)

    def test_question_flow_basic(self):
        self.mgr.questions.ask("q1", "What is acceleration?")
        self.assertEqual(self.mgr.questions.get_question("q1")["text"], "What is acceleration?")
        self.mgr.questions.answer("q1", "s1", "Rate of change of velocity")
        self.assertEqual(len(self.mgr.questions.get_question("q1")["answers"]), 1)

    def test_question_categorize(self):
        self.mgr.questions.ask("q2", "Calculate force", "numerical")
        self.assertEqual(self.mgr.questions.get_question("q2")["category"], "numerical")

    def test_question_multiple_answers(self):
        self.mgr.questions.ask("q3", "Explain gravity")
        self.mgr.questions.answer("q3", "s1", "A force")
        self.mgr.questions.answer("q3", "s2", "Curvature of spacetime")
        self.assertEqual(len(self.mgr.questions.get_question("q3")["answers"]), 2)

    def test_poll_flow_basic(self):
        self.mgr.polls.create_poll("p1", "Is gravity a force?", ["Yes", "No"])
        self.mgr.polls.collect_response("p1", "s1", 0)
        summary = self.mgr.polls.summarize("p1")
        self.assertEqual(summary[0], 1)

    def test_poll_multiple_responses(self):
        self.mgr.polls.create_poll("p2", "Best programming language?", ["Python", "C++", "Java"])
        self.mgr.polls.collect_response("p2", "s1", 0)
        self.mgr.polls.collect_response("p2", "s2", 0)
        self.mgr.polls.collect_response("p2", "s3", 1)
        summary = self.mgr.polls.summarize("p2")
        self.assertEqual(summary[0], 2)
        self.assertEqual(summary[1], 1)

    def test_poll_summarize_empty(self):
        self.assertEqual(self.mgr.polls.summarize("non_existent"), {})

    def test_activity_creation(self):
        self.mgr.activities.create_activity("a1", "Bridge Design", "hands-on activity")
        self.assertEqual(self.mgr.activities.get_activity("a1")["name"], "Bridge Design")
        self.assertEqual(self.mgr.activities.get_activity("a1")["type"], "hands-on activity")

    def test_activity_types(self):
        self.mgr.activities.create_activity("a2", "Discuss friction", "think-pair-share")
        self.assertEqual(self.mgr.activities.get_activity("a2")["type"], "think-pair-share")

    def test_discussion_generation(self):
        self.mgr.discussions.add_discussion("d1", "How do loops work?", ["Give a real-world example."])
        self.assertEqual(self.mgr.discussions.get_discussion("d1")["prompt"], "How do loops work?")

    def test_discussion_follow_ups(self):
        self.mgr.discussions.add_discussion("d2", "Energy conservation", ["What is entropy?", "Give examples."])
        self.assertEqual(len(self.mgr.discussions.get_discussion("d2")["follow_ups"]), 2)

    def test_feedback_collection(self):
        self.mgr.feedback.collect_feedback("s1", 5, "Excellent lesson")
        summary = self.mgr.feedback.summarize_feedback()
        self.assertEqual(summary["total_responses"], 1)
        self.assertEqual(summary["average_rating"], 5.0)

    def test_feedback_average(self):
        self.mgr.feedback.collect_feedback("s1", 4)
        self.mgr.feedback.collect_feedback("s2", 2)
        summary = self.mgr.feedback.summarize_feedback()
        self.assertEqual(summary["average_rating"], 3.0)

    def test_feedback_empty_summary(self):
        summary = self.mgr.feedback.summarize_feedback()
        self.assertEqual(summary["average_rating"], 0.0)
        self.assertEqual(summary["total_responses"], 0)

    def test_participation_tracking(self):
        self.mgr.responses.track_response("s1")
        self.mgr.responses.track_response("s1")
        self.assertEqual(self.mgr.responses.get_participation_count("s1"), 2)
        self.assertEqual(self.mgr.responses.get_participation_count("s2"), 0)

    def test_manager_lifecycle_integration(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            engine = PresentationEngine(workspace_root=tmp_dir)
            self.assertIsNone(engine.classroom_manager)
            engine.initialize()
            self.assertIsNotNone(engine.classroom_manager)
            engine.shutdown()
            self.assertIsNone(engine.classroom_manager)

if __name__ == "__main__":
    unittest.main()
