from abc import ABC, abstractmethod

class NavigatorInterface(ABC):
    @abstractmethod
    def next_slide(self) -> int:
        pass

    @abstractmethod
    def previous_slide(self) -> int:
        pass
