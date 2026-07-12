from typing import Callable, Any
from core.events.event import Event

EventListener = Callable[[Event], Any]
