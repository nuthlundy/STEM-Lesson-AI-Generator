import unittest
import time
from services.presentation.utilities.timer import LessonTimer
from services.presentation.utilities.countdown import Countdown
from services.presentation.utilities.breaks import BreakReminder
from services.presentation.utilities.attendance import AttendanceTracker
from services.presentation.utilities.statistics import PresentationStatistics
from services.presentation.utilities import UtilityManager

class TestPresentationUtilities(unittest.TestCase):
    def test_lesson_timer(self):
        timer = LessonTimer()
        time.sleep(0.01)
        self.assertGreater(timer.elapsed_seconds(), 0.0)

    def test_countdown(self):
        cd = Countdown(limit_seconds=10)
        self.assertEqual(cd.get_remaining(), 10)
        self.assertEqual(cd.tick(2), 8)
        self.assertEqual(cd.tick(10), 0)

    def test_break_reminder(self):
        br = BreakReminder(interval_seconds=100)
        self.assertFalse(br.should_break(50))
        self.assertTrue(br.should_break(100))

    def test_attendance(self):
        at = AttendanceTracker()
        at.mark_present("s1")
        at.mark_present("s2")
        self.assertEqual(at.get_present_students(), ["s1", "s2"])

    def test_statistics(self):
        stats = PresentationStatistics()
        stats.increment_slide_views()
        stats.increment_clicks()
        self.assertEqual(stats.stats["slide_views"], 1)
        self.assertEqual(stats.stats["total_clicks"], 1)
        
    def test_utility_manager(self):
        mgr = UtilityManager()
        self.assertIsInstance(mgr.timer, LessonTimer)
        self.assertIsInstance(mgr.countdown, Countdown)
        self.assertIsInstance(mgr.breaks, BreakReminder)

if __name__ == "__main__":
    unittest.main()
