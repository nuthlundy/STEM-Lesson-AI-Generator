from abc import ABC, abstractmethod

class ControllerInterface(ABC):
    @abstractmethod
    def start_session(self) -> None:
        pass

    @abstractmethod
    def end_session(self) -> None:
        pass
