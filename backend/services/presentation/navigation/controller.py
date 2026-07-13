from services.presentation.navigation.navigator import PresentationNavigator
from services.presentation.navigation.history import NavigationHistory
from services.presentation.navigation.bookmarks import NavigationBookmarks
from services.presentation.navigation.jump import NavigationJump

class NavigationController:
    def __init__(self, total_slides: int = 10) -> None:
        self.navigator = PresentationNavigator(total_slides=total_slides)
        self.history = NavigationHistory()
        self.bookmarks = NavigationBookmarks()
        self.jump = NavigationJump(max_slides=total_slides)
        self.history.record_visit(0)

    def next(self) -> int:
        idx = self.navigator.next_slide()
        self.history.record_visit(idx)
        return idx

    def previous(self) -> int:
        idx = self.navigator.previous_slide()
        self.history.record_visit(idx)
        return idx

    def jump_to(self, slide_index: int) -> int:
        idx = self.jump.jump_to_slide(slide_index)
        self.navigator.set_current(idx)
        self.history.record_visit(idx)
        return idx

    def add_bookmark(self, slide_index: int) -> None:
        self.bookmarks.add_bookmark(slide_index)

    def remove_bookmark(self, slide_index: int) -> None:
        self.bookmarks.remove_bookmark(slide_index)

    def get_bookmarks(self):
        return self.bookmarks.list_bookmarks()

    def get_history(self):
        return self.history.get_history()
