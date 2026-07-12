import threading
from typing import Dict
from core.monitoring.metrics import PipelineMetrics, StageMetrics
from core.monitoring.exceptions import DuplicateMetricError, MissingCollectorError

class MetricsTracker:
    def __init__(self):
        self._lock = threading.Lock()
        self._pipelines: Dict[str, PipelineMetrics] = {}

    def start_pipeline(self, pipeline_name: str) -> PipelineMetrics:
        with self._lock:
            if pipeline_name in self._pipelines:
                raise DuplicateMetricError(f"Metric collector for {pipeline_name} already registered.")
            metrics = PipelineMetrics(pipeline_name=pipeline_name)
            self._pipelines[pipeline_name] = metrics
            return metrics

    def get_pipeline_metrics(self, pipeline_name: str) -> PipelineMetrics:
        with self._lock:
            if pipeline_name not in self._pipelines:
                raise MissingCollectorError(f"No metric collector for {pipeline_name}.")
            return self._pipelines[pipeline_name]

    def record_stage_execution(
        self,
        pipeline_name: str,
        stage_id: str,
        duration: float,
        memory_usage: int,
        success: bool,
        retries: int = 0
    ) -> None:
        metrics = self.get_pipeline_metrics(pipeline_name)
        with self._lock:
            if stage_id not in metrics.stage_metrics:
                metrics.stage_metrics[stage_id] = StageMetrics(stage_id=stage_id)
            sm = metrics.stage_metrics[stage_id]
            sm.duration = duration
            sm.memory_usage_bytes = memory_usage
            sm.retry_count += retries
            if success:
                sm.success_count += 1
                metrics.success_count += 1
            else:
                sm.failure_count += 1
                metrics.failure_count += 1
            metrics.retry_count += retries
            if memory_usage > metrics.peak_memory_bytes:
                metrics.peak_memory_bytes = memory_usage

_global_tracker = MetricsTracker()

def get_metrics_tracker() -> MetricsTracker:
    return _global_tracker
