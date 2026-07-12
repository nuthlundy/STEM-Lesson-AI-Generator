from core.monitoring.metrics import PipelineMetrics
from core.monitoring.health import HealthEvaluator

class MetricsStatistics:
    @staticmethod
    def calculate_statistics(metrics: PipelineMetrics) -> None:
        total_stages = len(metrics.stage_metrics)
        if total_stages > 0:
            total_duration = sum(sm.duration for sm in metrics.stage_metrics.values())
            metrics.total_duration = total_duration
            metrics.average_processing_time = round(total_duration / total_stages, 4)
            if total_duration > 0:
                metrics.throughput = round(total_stages / total_duration, 4)
        metrics.health_state = HealthEvaluator.evaluate(metrics)
