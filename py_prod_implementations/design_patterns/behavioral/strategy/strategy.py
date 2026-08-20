from typing import Protocol


# ==============================================================================
# [ISP] INTERFACE SEGREGATION PRINCIPLE
# We do not force ducks to implement a massive `DuckBehavior` interface
# containing fly(), quack(), swim(), and lay_eggs(). Instead, we segregate
# the behaviors into small, focused Protocols. Clients only depend on the
# interfaces they actually need.
# ==============================================================================

class FlyBehavior(Protocol):
    def fly(self) -> str:
        ...


class QuackBehavior(Protocol):
    def quack(self) -> str:
        ...


# ==============================================================================
# [SRP] SINGLE RESPONSIBILITY PRINCIPLE
# Each concrete strategy class has exactly one responsibility and one reason to
# change. `FlyWithWings` only manages the mechanics of natural flight. It
# knows nothing about quacking, duck names, or state management.
# ==============================================================================

class FlyWithWings:
    def fly(self) -> str:
        return "I'm flying with wings!"


class FlyNoWay:
    def fly(self) -> str:
        return "I can't fly."


class NormalQuack:
    def quack(self) -> str:
        return "Quack! Quack!"


class Squeak:
    def quack(self) -> str:
        return "Squeak!"


# ==============================================================================
# THE CONTEXT CLASS
# ==============================================================================

class Duck:
    # [DIP] DEPENDENCY INVERSION PRINCIPLE
    # The high-level `Duck` class does not depend on low-level concrete classes
    # (like `FlyWithWings`). Instead, it depends on the abstractions
    # (`FlyBehavior` and `QuackBehavior` Protocols). The dependencies are
    # injected via the constructor.
    def __init__(self, name: str, fly_behavior: FlyBehavior,
                 quack_behavior: QuackBehavior):
        self.name = name
        self.fly_behavior = fly_behavior
        self.quack_behavior = quack_behavior

    def perform_fly(self) -> str:
        return self.fly_behavior.fly()

    def perform_quack(self) -> str:
        return self.quack_behavior.quack()

    def set_fly_behavior(self, new_behavior: FlyBehavior) -> None:
        self.fly_behavior = new_behavior


# ==============================================================================
# EXECUTION & DEMONSTRATION
# ==============================================================================

if __name__ == "__main__":
    # Create our ducks by composing them with specific strategies
    mallard = Duck("Mallard", FlyWithWings(), NormalQuack())
    rubber_duck = Duck("Rubber Duck", FlyNoWay(), Squeak())

    print(f"{mallard.name}: {mallard.perform_fly()}")
    print(f"{rubber_duck.name}: {rubber_duck.perform_fly()}")
    print("-" * 40)

    # [OCP] OPEN/CLOSED PRINCIPLE
    # We want to add a completely new flying behavior (Rocket). We do NOT need
    # to modify the `Duck` class, nor do we need to touch the existing
    # `FlyBehavior` implementations. The system is OPEN for extension but
    # CLOSED for modification.

    class RocketPoweredFly:
        def fly(self) -> str:
            return "3.. 2.. 1.. Liftoff!"


    print("Someone strapped a rocket to the rubber duck!")

    # [LSP] LISKOV SUBSTITUTION PRINCIPLE
    # We can replace the `FlyNoWay` object with a `RocketPoweredFly` object at
    # runtime. Because both strictly adhere to the `FlyBehavior` Protocol
    # signature, the `Duck` class continues to function perfectly without
    # knowing the underlying implementation changed.

    rubber_duck.set_fly_behavior(RocketPoweredFly())

    print(f"{rubber_duck.name}: {rubber_duck.perform_fly()}")
