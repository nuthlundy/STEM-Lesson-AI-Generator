from services.presentation.interfaces.navigator import NavigatorInterface

class PresentationNavigator(NavigatorInterface):
    def __init__(self, total_slides: int = 1) -> None:
        self.total_slides = total_slides
        self._current_index = 0

    def current_slide(self) -> int:
        return self._current_index

    def next_slide(self) -> int:
        if self._current_index < self.total_slides - 1:
            self._current_index += 1
        return self._current_index

    def previous_slide(self) -> int:
        if self._current_index > 0:
            self._current_index -= 1
        return self._current_index

    def set_current(self, index: int) -> None:
        if 0 <= index < self.total_slides:
            self._current_index = index
