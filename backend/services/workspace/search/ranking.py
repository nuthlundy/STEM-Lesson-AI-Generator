from typing import List, Dict, Any

class SearchRanking:
    @staticmethod
    def rank(results: List[Dict[str, Any]], order_by: str = "relevance") -> List[Dict[str, Any]]:
        if order_by == "recency":
            return sorted(results, key=lambda r: r.get("timestamp", 0.0), reverse=True)
        if order_by == "priority":
            return sorted(results, key=lambda r: r.get("priority", 0), reverse=True)
        return sorted(results, key=lambda r: r.get("score", 0.0), reverse=True)
