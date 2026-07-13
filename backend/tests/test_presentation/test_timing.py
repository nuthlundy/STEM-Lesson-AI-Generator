import unittest
import time
from services.presentation.timing.timer import PresentationTimer
from services.presentation.timing.scheduler import PresentationScheduler
from services.presentation.timing.estimator import PresentationEstimator
from services.presentation.timing.tracker import PresentationTracker

class TestPresentationTiming(unittest.TestCase):
    def test_timer_lifecycle(self):
        timer = PresentationTimer()
        self.assertEqual(timer.get_elapsed_seconds(), 0.0)
        
        timer.start()
        time.sleep(0.01)
        self.assertGreater(timer.get_elapsed_seconds(), 0.0)
        
        timer.pause()
        elapsed_before = timer.get_elapsed_seconds()
        time.sleep(0.01)
        elapsed_after = timer.get_elapsed_seconds()
        self.assertEqual(elapsed_before, elapsed_after)
        
        timer.resume()
        time.sleep(0.01)
        self.assertGreater(timer.get_elapsed_seconds(), elapsed_before)
        
        timer.stop()
        self.assertEqual(timer.get_elapsed_seconds(), 0.0)

    def test_scheduler_duration_split(self):
        scheduler = PresentationScheduler(estimated_duration=3600)
        timings = scheduler.get_section_timings(total_slides=10)
        self.assertEqual(len(timings), 10)
        self.assertEqual(timings[0]["estimated_duration_seconds"], 360)

    def test_estimator_words_per_minute(self):
        duration = PresentationEstimator.estimate_slide_duration("Slide 1", 120)
        self.assertEqual(duration, 90)
        
        total = PresentationEstimator.estimate_total_duration([120, 60])
        self.assertEqual(total, 150)

    def test_tracker_progress(self):
        tracker = PresentationTracker()
        tracker.mark_slide_completed(1)
        tracker.mark_slide_completed(3)
        self.assertEqual(tracker.get_completed_slides(), [1, 3])
        
        tracker.set_actual_elapsed_time(450.5)
        self.assertEqual(tracker.get_actual_elapsed_time(), 450.5)

if __name__ == "__main__":
    unittest.main()
