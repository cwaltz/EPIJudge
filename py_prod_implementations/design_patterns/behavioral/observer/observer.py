import weakref
from dataclasses import dataclass
from typing import Protocol


# ============================================================================
# EVENT PAYLOAD
# ============================================================================
@dataclass(frozen=True, slots=True)
class WeatherEvent:
    """
    [SOLID: OCP - Open/Closed Principle]
    By passing an event object rather than individual parameters
    (temp, humidity), we can add new fields (e.g., wind_speed) to this
    payload in the future without breaking the method signatures of existing
    Observers.
    """
    temp: float
    humidity: float
    pressure: float


# ============================================================================
# PROTOCOLS (INTERFACES)
# ============================================================================
class Observer(Protocol):
    """
    [SOLID: ISP - Interface Segregation Principle]
    This interface is perfectly segregated. It forces only a single, highly
    cohesive method (`update`). Observers are not forced to implement methods
    they do not need.
    """

    def update(self, event: WeatherEvent) -> None:
        ...


class Subject(Protocol):
    """
    [SOLID: ISP]
    The Subject interface is segregated strictly for subscription management
    and event broadcasting.
    """

    def attach(self, observer: Observer) -> None: ...

    def detach(self, observer: Observer) -> None: ...

    def notify(self, event: WeatherEvent) -> None: ...


# ============================================================================
# INFRASTRUCTURE LAYER
# ============================================================================
class EventDispatcher:
    """
    [SOLID: SRP - Single Responsibility Principle]
    This class has ONE reason to change: if the infrastructure for message
    routing changes (e.g., swapping this local dictionary for a Redis queue).
    It knows absolutely nothing about weather domain logic.
    """

    def __init__(self) -> None:
        self._observers: weakref.WeakKeyDictionary[
            Observer, None] = weakref.WeakKeyDictionary()

    def attach(self, observer: Observer) -> None:
        self._observers[observer] = None

    def detach(self, observer: Observer) -> None:
        self._observers.pop(observer, None)

    def notify(self, event: WeatherEvent) -> None:
        """
        [SOLID: LSP - Liskov Substitution Principle]
        The dispatcher trusts that any object in `_observers` adheres to the
        Observer protocol. We can substitute ANY concrete observer here, and
        the dispatcher will not break or behave unexpectedly.
        """
        active_observers = list(self._observers.keys())

        for observer in active_observers:
            try:
                observer.update(event)
            except Exception as e:
                print(f"[{observer.__class__.__name__} Error]: {e}")


# ============================================================================
# DOMAIN LAYER
# ============================================================================
class WeatherStation:
    """
    [SOLID: SRP]
    This class has ONE reason to change: if the business rules for weather
    validation or hardware interactions change.
    """

    def __init__(self, dispatcher: Subject) -> None:
        """
        [SOLID: DIP - Dependency Inversion Principle]
        High-level domain modules (WeatherStation) do NOT depend on low-level
        infrastructure modules (EventDispatcher). Instead, they both depend on
        the abstract `Subject` Protocol.
        """
        self._dispatcher = dispatcher

    def set_measurements(self, temp: float, humidity: float,
                         pressure: float) -> None:
        if temp < -50.0 or temp > 60.0:
            raise ValueError(f"Hardware error: {temp}°C is out of bounds.")

        event = WeatherEvent(temp, humidity, pressure)
        self._dispatcher.notify(event)


# ============================================================================
# CONCRETE OBSERVERS
# ============================================================================
class CurrentConditionsDisplay:
    def update(self, event: WeatherEvent) -> None:
        print(f"[UI Display] Temp: {event.temp}°C, Humidity: {event.humidity}%")


class AlertSystem:
    def update(self, event: WeatherEvent) -> None:
        if event.temp > 35.0:
            print(f"[ALARM] Extreme Heat Detected: {event.temp}°C!")


# ============================================================================
# SYSTEM WIRING (MAIN)
# ============================================================================
if __name__ == "__main__":
    # Dependency Injection in action
    event_dispatcher = EventDispatcher()
    station = WeatherStation(event_dispatcher)

    # [SOLID: OCP]
    # We can add 100 new observer types here tomorrow. We will NEVER have to
    # modify the code inside EventDispatcher or WeatherStation to support them.
    display = CurrentConditionsDisplay()
    alert = AlertSystem()

    event_dispatcher.attach(display)
    event_dispatcher.attach(alert)

    print("--- Reading 1 ---")
    station.set_measurements(25.0, 65.0, 1013.0)

    print("\n--- Reading 2 ---")
    station.set_measurements(38.0, 40.0, 1010.0)
