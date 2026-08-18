import weakref
from dataclasses import dataclass
from typing import Protocol


# ============================================================================
# 1. EVENT PAYLOAD
# ============================================================================
@dataclass(frozen=True, slots=True)
class WeatherEvent:
    """
    Immutable data envelope carrying state changes.
    Using slots=True prevents dynamic attribute creation, saving memory.
    frozen=True guarantees Observers cannot accidentally mutate the state.
    """
    temp: float
    humidity: float
    pressure: float


# ============================================================================
# 2. PROTOCOLS (INTERFACES)
# ============================================================================
class Observer(Protocol):
    """Protocol defining the receiver in the Observer pattern."""

    def update(self, event: WeatherEvent) -> None:
        """Process the incoming event payload."""
        ...


class Subject(Protocol):
    """
    Protocol defining the publisher/dispatcher in the Observer pattern.
    Domain classes will depend on this abstraction, not a concrete
    implementation.
    """

    def attach(self, observer: Observer) -> None: ...

    def detach(self, observer: Observer) -> None: ...

    def notify(self, event: WeatherEvent) -> None: ...


# ============================================================================
# 3. INFRASTRUCTURE LAYER (Message Routing)
# ============================================================================
class EventDispatcher:
    """
    Concrete implementation of the Subject Protocol.
    Responsibility: Safely routing events from publishers to subscribers.
    """

    def __init__(self) -> None:
        # Weak references prevent the Lapsed Listener memory leak.
        # Observers garbage-collected by the system are automatically removed.
        self._observers: weakref.WeakKeyDictionary[
            Observer, None] = weakref.WeakKeyDictionary()

    def attach(self, observer: Observer) -> None:
        """Registers an observer for future events."""
        self._observers[observer] = None

    def detach(self, observer: Observer) -> None:
        """Removes an observer safely if it exists."""
        self._observers.pop(observer, None)

    def notify(self, event: WeatherEvent) -> None:
        """
        Pushes the event to all active observers.
        """
        # CRITICAL: Snapshot keys to a list to avoid RuntimeError if the GC
        # alters the WeakKeyDictionary size mid-iteration on another thread.
        active_observers = list(self._observers.keys())

        for observer in active_observers:
            try:
                observer.update(event)
            except Exception as e:
                # FAULT ISOLATION:
                # A crashed observer cannot halt the dispatch loop
                print(
                    f"[{observer.__class__.__name__} Error]: "
                    f"Failed to process event - {e}")


# ============================================================================
# 4. DOMAIN LAYER (Business Logic)
# ============================================================================
class WeatherStation:
    """
    Domain entity responsible for hardware validation and state.
    Responsibility: Enforcing weather business rules and generating events.
    """

    def __init__(self, dispatcher: Subject) -> None:
        # Dependency Injection:
        # The domain relies purely on the Subject Protocol.
        self._dispatcher = dispatcher

    def set_measurements(self, temp: float, humidity: float,
                         pressure: float) -> None:
        """Simulates reading from hardware, validates data, and publishes."""

        # Domain validation logic
        if temp < -50.0 or temp > 60.0:
            raise ValueError(
                f"Temperature {temp}°C is out of bounds for Earth sensors.")

        # Create immutable event envelope
        event = WeatherEvent(temp, humidity, pressure)

        # Delegate routing to the injected infrastructure
        self._dispatcher.notify(event)


# ============================================================================
# 5. CONCRETE OBSERVERS (Subscribers)
# ============================================================================
class CurrentConditionsDisplay:
    """Pure UI component decoupled from the domain."""

    def update(self, event: WeatherEvent) -> None:
        print(f"[Current Display] {event.temp}°C, Humidity: {event.humidity}%")


class AlertSystem:
    """Pure alert component decoupled from the domain."""

    def update(self, event: WeatherEvent) -> None:
        if event.temp > 35.0:
            print(f"[ALERT SYSTEM] Heat warning! Reached {event.temp}°C")


# ============================================================================
# 6. SYSTEM WIRING (Dependency Injection / Main)
# ============================================================================
if __name__ == "__main__":
    print("--- Bootstrapping System ---")
    # 1. Initialize infrastructure
    event_dispatcher = EventDispatcher()

    # 2. Initialize domain, injecting the infrastructure
    station = WeatherStation(event_dispatcher)

    # 3. Initialize observers (Must be assigned to strong reference variables!)
    display = CurrentConditionsDisplay()
    alert = AlertSystem()

    # 4. Wire observers to the dispatcher (Decoupled from WeatherStation)
    event_dispatcher.attach(display)
    event_dispatcher.attach(alert)

    print("\n--- Event 1: Normal Weather ---")
    station.set_measurements(25.0, 65.0, 1013.0)

    print("\n--- Event 2: Extreme Heat ---")
    station.set_measurements(38.0, 40.0, 1010.0)

    print("\n--- Event 3: Alert System goes out of scope (GC triggers) ---")
    del alert  # Simulates object destruction. WeakKeyDict auto-removes it.
    station.set_measurements(39.0, 42.0, 1008.0)
