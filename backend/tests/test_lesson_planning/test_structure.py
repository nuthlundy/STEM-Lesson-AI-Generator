import unittest
from services.lesson_planning.schemas import LessonSection
from services.lesson_planning.processors.sequencer import LessonSectionSequencer
from services.lesson_planning.processors.allocator import TimeAllocationEngine
from services.lesson_planning.processors.mapper import ObjectiveMapper
from services.lesson_planning.processors.transitions import TransitionGenerator
from services.lesson_planning.processors.validator import TimelineValidator

class TestLessonStructure(unittest.TestCase):
    def test_sequencer_contents(self):
        seq = LessonSectionSequencer.get_sequence()
        self.assertEqual(len(seq), 10)
        self.assertIn("Introduction", seq)
        self.assertIn("Closing", seq)

    def test_sequencer_strict_order(self):
        seq = LessonSectionSequencer.get_sequence()
        self.assertEqual(seq[0], "Introduction")
        self.assertEqual(seq[-1], "Closing")

    def test_allocator_proportional_60(self):
        allocated = TimeAllocationEngine.allocate_durations(60)
        self.assertEqual(sum(allocated.values()), 60)

    def test_allocator_proportional_90(self):
        allocated = TimeAllocationEngine.allocate_durations(90)
        self.assertEqual(sum(allocated.values()), 90)

    def test_allocator_negative_fallback(self):
        allocated = TimeAllocationEngine.allocate_durations(-10)
        self.assertEqual(sum(allocated.values()), 60)

    def test_mapper_understand_level(self):
        objs = [{"id": "obj_1", "bloom_level": "Understand"}]
        mapping = ObjectiveMapper.map_objectives(objs)
        self.assertIn("Prior Knowledge", mapping["obj_1"])
        self.assertIn("Learning Objectives", mapping["obj_1"])

    def test_mapper_apply_level(self):
        objs = [{"id": "obj_2", "bloom_level": "Apply"}]
        mapping = ObjectiveMapper.map_objectives(objs)
        self.assertIn("Guided Practice", mapping["obj_2"])

    def test_transitions_length(self):
        timeline = ["Intro", "Objectives", "Closing"]
        transitions = TransitionGenerator.generate_transitions(timeline)
        self.assertEqual(len(transitions), 2)
        self.assertEqual(transitions[0].from_section, "Intro")
        self.assertEqual(transitions[0].to_section, "Objectives")

    def test_validator_valid(self):
        sections = [
            LessonSection(title=title, duration_minutes=8, description="walkthrough")
            for title in LessonSectionSequencer.get_sequence()
        ]
        report = TimelineValidator.validate(sections, LessonSectionSequencer.get_sequence(), {"obj_1": ["Learning Objectives"]}, 1)
        self.assertTrue(report.valid)

    def test_validator_invalid_order(self):
        sections = [
            LessonSection(title="Closing", duration_minutes=8, description="walkthrough"),
            LessonSection(title="Introduction", duration_minutes=8, description="walkthrough")
        ]
        report = TimelineValidator.validate(sections, ["Closing", "Introduction"], {}, 0)
        self.assertFalse(report.valid)
        self.assertTrue(any("ordering mismatch" in err for err in report.errors))

if __name__ == "__main__":
    unittest.main()
