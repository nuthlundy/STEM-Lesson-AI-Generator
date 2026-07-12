from typing import List
from core.events.event import Event
from core.events.registry import EventRegistry
from core.events.listener import EventListener

class EventDispatcher:
    """Synchronous event dispatcher coordinating subscriptions and publishing."""
    
    def __init__(self):
        self._registry = EventRegistry()
        self._history: List[Event] = []

    def subscribe(self, event_name: str, listener: EventListener) -> None:
        """Registers a listener for a specific event name."""
        self._registry.subscribe(event_name, listener)

    def unsubscribe(self, event_name: str, listener: EventListener) -> None:
        """Removes a listener registration."""
        self._registry.unsubscribe(event_name, listener)

    def publish(self, event: Event) -> None:
        """Publishes an event to all subscribed listeners and logs it to history."""
        self._history.append(event)
        self.dispatch(event)

    def dispatch(self, event: Event) -> None:
        """Synchronously dispatches the event to registered listeners."""
        listeners = self._registry.get_listeners(event.event_name)
        wildcard_listeners = self._registry.get_listeners("*")
        
        for listener in listeners + wildcard_listeners:
            try:
                listener(event)
            except Exception:
                pass

    def history(self) -> List[Event]:
        """Returns the chronological history of published events."""
        return self._history

_global_dispatcher = EventDispatcher()

def get_event_dispatcher() -> EventDispatcher:
    return _global_dispatcher
