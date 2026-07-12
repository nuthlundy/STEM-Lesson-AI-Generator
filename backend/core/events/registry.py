from typing import Dict, List
from core.events.listener import EventListener

class EventRegistry:
    """Manages the mapping of event names to subscribed listeners."""
    def __init__(self):
        self._listeners: Dict[str, List[EventListener]] = {}

    def subscribe(self, event_name: str, listener: EventListener) -> None:
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(listener)

    def unsubscribe(self, event_name: str, listener: EventListener) -> None:
        if event_name in self._listeners:
            try:
                self._listeners[event_name].remove(listener)
            except ValueError:
                pass

    def get_listeners(self, event_name: str) -> List[EventListener]:
        return self._listeners.get(event_name, [])
