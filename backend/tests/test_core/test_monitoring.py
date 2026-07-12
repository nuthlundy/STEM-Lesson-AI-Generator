import unittest
import time
from core.monitoring import (
    get_metrics_tracker,
    Profiler,
    PipelineMetrics,
    MetricsStatistics,
    HealthEvaluator
)
from core.monitoring.exceptions import DuplicateMetricError, MissingCollectorError

class TestMonitoring(unittest.TestCase):
    def setUp(self):
        # Reset global tracker or instantiate a fresh one
        from core.monitoring.tracker import MetricsTracker
        self.tracker = MetricsTracker()

    def test_pipeline_metrics_registration(self):
        metrics = self.tracker.start_pipeline("p1")
        self.assertEqual(metrics.pipeline_name, "p1")
        self.assertEqual(self.tracker.get_pipeline_metrics("p1"), metrics)

    def test_duplicate_pipeline_metrics(self):
        self.tracker.start_pipeline("p2")
        with self.assertRaises(DuplicateMetricError):
            self.tracker.start_pipeline("p2")

    def test_missing_pipeline_metrics(self):
        with self.assertRaises(MissingCollectorError):
            self.tracker.get_pipeline_metrics("non_existent")

    def test_stage_metrics_recording(self):
        self.tracker.start_pipeline("p3")
        self.tracker.record_stage_execution(
            pipeline_name="p3",
            stage_id="stage-a",
            duration=0.55,
            memory_usage=1000,
            success=True,
            retries=1
        )
        metrics = self.tracker.get_pipeline_metrics("p3")
        self.assertEqual(metrics.success_count, 1)
        self.assertEqual(metrics.retry_count, 1)
        self.assertEqual(metrics.peak_memory_bytes, 1000)
        self.assertIn("stage-a", metrics.stage_metrics)
        self.assertEqual(metrics.stage_metrics["stage-a"].duration, 0.55)

    def test_profiler_time_tracking(self):
        with Profiler() as prof:
            time.sleep(0.01)
        self.assertGreater(prof.duration, 0.0)
        self.assertGreater(prof.peak_memory, 0)

    def test_statistics_calculation(self):
        metrics = PipelineMetrics(pipeline_name="p4")
        from core.monitoring.metrics import StageMetrics
        metrics.stage_metrics["s1"] = StageMetrics(stage_id="s1", duration=1.0)
        metrics.stage_metrics["s2"] = StageMetrics(stage_id="s2", duration=2.0)
        
        MetricsStatistics.calculate_statistics(metrics)
        self.assertEqual(metrics.total_duration, 3.0)
        self.assertEqual(metrics.average_processing_time, 1.5)
        self.assertEqual(metrics.throughput, round(2 / 3, 4))

    def test_health_evaluation(self):
        metrics = PipelineMetrics(pipeline_name="p5")
        self.assertEqual(HealthEvaluator.evaluate(metrics), "Healthy")
        
        metrics.peak_memory_bytes = 300 * 1024 * 1024 # 300MB
        self.assertEqual(HealthEvaluator.evaluate(metrics), "Warning")
        
        metrics.failure_count = 1
        self.assertEqual(HealthEvaluator.evaluate(metrics), "Critical")

if __name__ == "__main__":
    unittest.main()
