from typing import List

class NavigationHistory:
    def __init__(self) -> None:
        self._stack: List[int] = []

    def record_visit(self, slide_index: int) -> None:
        if not self._stack or self._stack[-1] != slide_index:
            self._stack.append(slide_index)

    def get_history(self) -> List[int]:
        return list(self._stack)

    def pop_last(self) -> int:
        if len(self._stack) > 1:
            self._stack.pop()
            return self._stack[-1]
        return 0
