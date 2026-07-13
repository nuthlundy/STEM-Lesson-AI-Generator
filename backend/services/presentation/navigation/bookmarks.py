from typing import List, Set

class NavigationBookmarks:
    def __init__(self) -> None:
        self._bookmarks: Set[int] = set()

    def add_bookmark(self, slide_index: int) -> None:
        self._bookmarks.add(slide_index)

    def remove_bookmark(self, slide_index: int) -> None:
        self._bookmarks.discard(slide_index)

    def list_bookmarks(self) -> List[int]:
        return sorted(list(self._bookmarks))
