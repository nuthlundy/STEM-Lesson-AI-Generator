from typing import Dict, Any, List

class RenderingMergeEngine:
    @staticmethod
    def merge(deterministic: Dict[str, Any], ai_data: Dict[str, Any]) -> Dict[str, Any]:
        merged = {}
        for k, v in deterministic.items():
            if isinstance(v, dict):
                merged[k] = dict(v)
            elif isinstance(v, list):
                merged[k] = list(v)
            else:
                merged[k] = v

        for k, v in ai_data.items():
            if k not in merged or merged[k] is None or merged[k] == "":
                if isinstance(v, dict):
                    merged[k] = dict(v)
                elif isinstance(v, list):
                    merged[k] = list(v)
                else:
                    merged[k] = v
            elif isinstance(merged[k], list) and isinstance(v, list):
                for item in v:
                    if item not in merged[k]:
                        merged[k].append(item)
            elif isinstance(merged[k], dict) and isinstance(v, dict):
                merged[k] = RenderingMergeEngine.merge(merged[k], v)
                
        return merged
