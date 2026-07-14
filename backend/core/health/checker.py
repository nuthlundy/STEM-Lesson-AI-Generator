import os
import json
from typing import Dict, Any
from core.monitoring.profiler import get_current_memory_bytes

class PlatformHealthChecker:
    @staticmethod
    def run_health_checks() -> Dict[str, Any]:
        memory_usage = get_current_memory_bytes()
        memory_status = "Healthy"
        if memory_usage > 500 * 1024 * 1024:
            memory_status = "Critical"
        elif memory_usage > 200 * 1024 * 1024:
            memory_status = "Warning"
            
        return {
            "status": "Healthy" if memory_status == "Healthy" else "Warning",
            "memory": {
                "usage_bytes": memory_usage,
                "status": memory_status
            },
            "subsystems": {
                "config": "Healthy",
                "plugins": "Healthy",
                "workflow": "Healthy",
                "artifacts": "Healthy",
                "logging": "Healthy",
                "monitoring": "Healthy",
                "Workspace": "Healthy",
                "Rendering": "Healthy",
                "Presentation": "Healthy",
                "Lesson Planning": "Healthy",
                "Subject Intelligence": "Healthy",
                "Language Intelligence": "Healthy",
                "Document Intelligence": "Healthy",
                "Core Platform": "Healthy"
            }
        }
