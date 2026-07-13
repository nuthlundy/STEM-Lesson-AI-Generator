from typing import List, Dict, Any

class SearchQuery:
    @staticmethod
    def matches(item: Dict[str, Any], query_str: str, exact: bool = False, prefix: bool = False) -> float:
        name = str(item.get("name", "")).lower()
        desc = str(item.get("description", "")).lower()
        q = query_str.lower()
        
        if exact:
            if q == name or q == desc:
                return 1.0
            return 0.0
            
        if prefix:
            if name.startswith(q) or desc.startswith(q):
                return 0.8
            return 0.0
            
        score = 0.0
        if q in name:
            score += 0.5
        if q in desc:
            score += 0.3
        return score
