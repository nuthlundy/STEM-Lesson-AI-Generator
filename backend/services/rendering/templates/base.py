from abc import ABC, abstractmethod

class BaseSlideTemplate(ABC):
    @abstractmethod
    def get_template_name(self) -> str:
        pass
