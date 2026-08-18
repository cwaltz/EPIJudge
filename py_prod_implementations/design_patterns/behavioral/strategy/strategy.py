from typing import Protocol


# 1. Define the "Interfaces" (Strategies) using Protocols
class FlyBehavior(Protocol):
    def fly(self) -> str:
        ...


class QuackBehavior(Protocol):
    def quack(self) -> str:
        ...


# 2. Implement Concrete Strategies
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


# 3. The Context (The Duck)
class Duck:
    # We use constructor injection to pass the strategies
    def __init__(self, name: str, fly_behavior: FlyBehavior,
                 quack_behavior: QuackBehavior):
        self.name = name
        self.fly_behavior = fly_behavior
        self.quack_behavior = quack_behavior

    def perform_fly(self) -> str:
        # Delegate the flying behavior to the strategy
        return self.fly_behavior.fly()

    def perform_quack(self) -> str:
        # Delegate the quacking behavior to the strategy
        return self.quack_behavior.quack()

    # The magic of Strategy: changing behavior at runtime
    def set_fly_behavior(self, new_behavior: FlyBehavior) -> None:
        self.fly_behavior = new_behavior


# 4. Let's see it in action
if __name__ == "__main__":
    # Create a Mallard Duck
    mallard = Duck("Mallard", FlyWithWings(), NormalQuack())
    print(f"{mallard.name}: {mallard.perform_fly()}")

    # Create a Rubber Duck
    rubber_duck = Duck("Rubber Duck", FlyNoWay(), Squeak())
    print(f"{rubber_duck.name}: {rubber_duck.perform_fly()}")

    # Runtime change! Someone gave the rubber duck a rocket pack.
    class RocketPoweredFly:
        def fly(self) -> str:
            return "3.. 2.. 1.. Liftoff!"


    rubber_duck.set_fly_behavior(RocketPoweredFly())
    print(f"{rubber_duck.name} later: {rubber_duck.perform_fly()}")
