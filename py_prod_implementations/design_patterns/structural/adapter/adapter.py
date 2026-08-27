"""
Google Gemini chat:
https://gemini.google.com/app/b4163b3794faae57
"""

import logging
from typing import Protocol

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


# ==========================================
# 1. TARGET INTERFACE (What our app expects)
# ==========================================
class PaymentProcessor(Protocol):
    """
    Defines the domain-specific interface that our application uses.
    Using `typing.Protocol` is the modern Pythonic way to define interfaces.
    Any class with a matching `pay` method will automatically satisfy this
    protocol.

    [SOLID: Interface Segregation Principle (ISP)]
    This protocol is highly specific and minimal (just one method). Clients
    are not forced to depend on massive interfaces with methods they don't use.
    """

    def pay(self, amount_in_dollars: float) -> bool:
        ...


# ==========================================
# 2. ADAPTEE (The incompatible third-party service)
# ==========================================
class LegacyEuroBankAPI:
    """
    An existing third-party or legacy class with an incompatible interface.
    In a real scenario, this is an external SDK that we CANNOT modify.

    [SOLID: Single Responsibility Principle (SRP)]
    This class has exactly one job: handling the complex, domain-specific
    communication with the external European banking system.
    """

    def execute_transaction(self, amount_in_cents: int, currency: str) -> dict:
        # Simulating a complex external API call
        logger.info(
            f"[Legacy API] Processing {amount_in_cents} cents in {currency}...")
        return {"status": "SUCCESS", "transaction_id": "TXN-99812"}


# ==========================================
# 3. ADAPTER (The Bridge)
# ==========================================
class EuroBankAdapter:
    """
    Bridges the gap. It conceptually implements PaymentProcessor (the Target)
    and wraps LegacyEuroBankAPI (the Adaptee).

    [SOLID: Single Responsibility Principle (SRP)]
    This adapter only handles data translation between the two incompatible
    interfaces. It delegates the actual business logic to the Adaptee.

    [SOLID: Liskov Substitution Principle (LSP)]
    Because this matches the `PaymentProcessor` protocol, it can seamlessly
    replace any other payment processor at runtime without breaking the client.
    """

    def __init__(self, legacy_api: LegacyEuroBankAPI):
        self._legacy_api = legacy_api

    def pay(self, amount_in_dollars: float) -> bool:
        # 1. Translate the data from our app's format to the Adaptee's format
        amount_in_cents = int(amount_in_dollars * 100)
        currency = "EUR"

        # 2. Delegate the actual work to the Adaptee
        response = self._legacy_api.execute_transaction(amount_in_cents,
                                                        currency)

        # 3. Translate the Adaptee's response back to what our app expects
        return response.get("status") == "SUCCESS"


# ==========================================
# 4. CLIENT (The Enterprise Application)
# ==========================================
class CheckoutService:
    """
    The domain logic that depends ONLY on the Target interface
    (PaymentProcessor).
    It is completely oblivious to the Legacy API or the Adapter.

    [SOLID: Dependency Inversion Principle (DIP)]
    This service does not depend on the concrete `EuroBankAdapter` or the
    legacy API. It depends purely on the abstract `PaymentProcessor` protocol.

    [SOLID: Open/Closed Principle (OCP)]
    If you integrate Stripe or PayPal later, you don't need to touch this class.
    You simply write a new Adapter and inject it. The system is open to
    extension but closed to modification.
    """

    def __init__(self, payment_processor: PaymentProcessor):
        self._processor = payment_processor

    def checkout(self, cart_total: float):
        logger.info(f"[Checkout] Initiating checkout for ${cart_total:.2f}")

        # The client simply calls the method it expects
        success = self._processor.pay(cart_total)

        if success:
            logger.info("[Checkout] Payment successful. Order complete.")
        else:
            logger.error("[Checkout] Payment failed.")


# ==========================================
# 5. EXECUTION (Dependency Wire-up)
# ==========================================
if __name__ == "__main__":
    # 1. Instantiate the incompatible Adaptee
    legacy_euro_bank_api = LegacyEuroBankAPI()

    # 2. Wrap the Adaptee inside the Adapter
    adapter = EuroBankAdapter(legacy_euro_bank_api)

    # 3. Inject the Adapter into the Client
    checkout = CheckoutService(payment_processor=adapter)

    # 4. Execute domain logic
    checkout.checkout(45.50)
