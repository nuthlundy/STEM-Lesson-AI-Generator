from core.monitoring.metrics import PipelineMetrics

class HealthEvaluator:
    @staticmethod
    def evaluate(metrics: PipelineMetrics) -> str:
        if metrics.failure_count > 0:
            return "Critical"
        if metrics.peak_memory_bytes > 200 * 1024 * 1024:
            return "Warning"
        return "Healthy"
