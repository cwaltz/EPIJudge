"""
Google Gemini chat:
https://gemini.google.com/app/d8f27e74294300d5
"""

import threading
from typing import Any


class SingletonMeta(type):
    """
    Thread-safe Singleton implementation using a Metaclass.
    Controls the creation of the class instance independently of the class
    itself.
    """
    _instances: dict[type, Any] = {}

    # A lock object to synchronize threads during first instantiation
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        # Double-checked locking pattern for optimal performance.
        # We only acquire the lock if the instance doesn't exist yet.
        if cls not in cls._instances:
            with cls._lock:
                # Re-check inside the lock to ensure another thread didn't
                # create the instance while we were waiting for the lock.
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class FeatureToggleConfig(metaclass=SingletonMeta):
    """
    Practical Usecase: Feature Toggle / Configuration Manager.
    All parts of the system will share this exact instance.
    """

    def __init__(self):
        # In production, this would load from AWS Secrets, a YAML file,
        # or a database.
        # The print statement proves __init__ is only executed once.
        print("Initializing FeatureToggleConfig... (Simulating heavy I/O load)")
        self._settings = {
            "enable_new_payment_gateway": True,
            "max_retries": 3,
            "maintenance_mode": False
        }

    def get_setting(self, key: str) -> Any:
        return self._settings.get(key)

    def set_setting(self, key: str, value: Any) -> None:
        self._settings[key] = value


# ==========================================
# Demonstration: Proving the Singleton works
# ==========================================
if __name__ == "__main__":
    print("--- Requesting config object for Module A ---")
    module_a_config = FeatureToggleConfig()

    print("\n--- Requesting config object for Module B ---")
    module_b_config = FeatureToggleConfig()

    print("\n--- Identity Check ---")
    # 'is' checks if both variables point to the exact same memory address
    is_same_object = module_a_config is module_b_config
    print(f"Are module_a_config and module_b_config the exact same object? "
          f"{is_same_object}")

    print("\n--- State Sharing Check ---")
    # Module A modifies the system state
    module_a_config.set_setting("maintenance_mode", True)
    print("Module A enabled maintenance mode.")

    # Module B reads the system state
    state_for_b = module_b_config.get_setting("maintenance_mode")
    print(f"Does Module B see maintenance mode as active? {state_for_b}")
