import unittest
import time
from services.workspace.autosave.scheduler import AutosaveScheduler

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.called = 0
        self.scheduler = AutosaveScheduler(interval=0.01, callback=self.callback)

    def callback(self):
        self.called += 1

    def tearDown(self):
        self.scheduler.stop()

    def test_scheduler_starts_and_stops(self):
        self.scheduler.start()
        self.assertTrue(self.scheduler.running)
        self.scheduler.stop()
        self.assertFalse(self.scheduler.running)

    def test_scheduler_triggers_callback(self):
        self.scheduler.start()
        time.sleep(0.05)
        self.scheduler.stop()
        self.assertTrue(self.called > 0)

    def test_scheduler_does_not_trigger_when_stopped(self):
        self.scheduler.start()
        self.scheduler.stop()
        curr = self.called
        time.sleep(0.02)
        self.assertEqual(self.called, curr)

    def test_interval_change(self):
        self.scheduler.interval = 0.5
        self.assertEqual(self.scheduler.interval, 0.5)

    def test_scheduler_no_callback_safe(self):
        sched = AutosaveScheduler(interval=0.01)
        sched.start()
        time.sleep(0.02)
        sched.stop()
        self.assertFalse(sched.running)

    def test_scheduler_corrupted_callback_safe(self):
        def bad_cb():
            raise Exception("Failure mock")
        sched = AutosaveScheduler(interval=0.01, callback=bad_cb)
        sched.start()
        time.sleep(0.02)
        sched.stop()
        self.assertFalse(sched.running)

    def test_double_start_ignored(self):
        self.scheduler.start()
        t1 = self.scheduler._thread
        self.scheduler.start()
        self.assertEqual(self.scheduler._thread, t1)

    def test_double_stop_ignored(self):
        self.scheduler.start()
        self.scheduler.stop()
        self.scheduler.stop()
        self.assertFalse(self.scheduler.running)

if __name__ == "__main__":
    unittest.main()
