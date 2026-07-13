from typing import List, Dict, Any
from services.workspace.search.indexer import SearchIndexer
from services.workspace.search.query import SearchQuery
from services.workspace.search.ranking import SearchRanking

class SearchEngine:
    def __init__(self, storage_path: str = ".") -> None:
        self.indexer = SearchIndexer(storage_path=storage_path)

    def search(self, query_str: str, category: str = None, exact: bool = False, prefix: bool = False, order_by: str = "relevance") -> List[Dict[str, Any]]:
        raw_results = []
        for item in self.indexer.index_data:
            if category and item.get("category") != category:
                continue
            score = SearchQuery.matches(item, query_str, exact=exact, prefix=prefix)
            if score > 0.0:
                doc = dict(item)
                doc["score"] = score
                raw_results.append(doc)
        return SearchRanking.rank(raw_results, order_by=order_by)

    def search_projects(self, query_str: str, exact: bool = False) -> List[Dict[str, Any]]:
        return self.search(query_str, category="project", exact=exact)

    def search_artifacts(self, query_str: str, exact: bool = False) -> List[Dict[str, Any]]:
        return self.search(query_str, category="artifact", exact=exact)

    def search_lessons(self, query_str: str, exact: bool = False) -> List[Dict[str, Any]]:
        return self.search(query_str, category="lesson", exact=exact)

    def search_history(self, query_str: str, exact: bool = False) -> List[Dict[str, Any]]:
        return self.search(query_str, category="history", exact=exact)

    def search_templates(self, query_str: str, exact: bool = False) -> List[Dict[str, Any]]:
        return self.search(query_str, category="template", exact=exact)
