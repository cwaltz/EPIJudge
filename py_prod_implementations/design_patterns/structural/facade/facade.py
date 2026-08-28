import logging
from dataclasses import dataclass
from typing import Protocol

# Setup basic enterprise-style logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


# --- 1. Data Models ---
@dataclass(frozen=True)
class Order:
    order_id: str
    product_id: str
    quantity: int
    customer_email: str
    amount: float


# --- Interface Segregation Principle (ISP) ---
# We create small, highly specific interfaces. Clients are not forced
# to depend on massive classes with methods they don't use.

class InventoryProvider(Protocol):
    def check_stock(self, product_id: str, quantity: int) -> bool: ...

    def reserve_stock(self, product_id: str, quantity: int) -> None: ...


class PaymentProvider(Protocol):
    def process_payment(self, order_id: str, amount: float) -> bool: ...


class NotificationProvider(Protocol):
    def send_receipt(self, email: str, order_id: str) -> None: ...


# --- 2. The Complex Subsystems ---
# In production, these might be external API wrappers, database repositories,
# or gRPC clients communicating with other microservices.

class InventoryService:
    def check_stock(self, product_id: str, quantity: int) -> bool:
        logging.info(
            f"Inventory: Checking stock for {product_id} (qty: {quantity}).")
        # Simulate business logic
        return True

    def reserve_stock(self, product_id: str, quantity: int) -> None:
        logging.info(f"Inventory: Reserving {quantity} units of {product_id}.")


class PaymentGateway:
    def process_payment(self, order_id: str, amount: float) -> bool:
        logging.info(f"Payment: Processing ${amount:.2f} for order {order_id}.")
        return True


class NotificationService:
    def send_receipt(self, email: str, order_id: str) -> None:
        logging.info(
            f"Notification: Sending receipt for {order_id} to {email}.")


# --- 2. Open/Closed & Liskov Substitution (OCP & LSP) ---
# We can add new payment methods (Open for Extension) without modifying
# the Facade (Closed for Modification). Any of these can substitute
# the PaymentProvider safely (LSP).

class StripePaymentGateway:
    def process_payment(self, order_id: str, amount: float) -> bool:
        logging.info(f"Stripe: Charged ${amount}")
        return True


class CryptoPaymentGateway:
    def process_payment(self, order_id: str, amount: float) -> bool:
        logging.info(f"Crypto: Transferred equivalent of ${amount} in BTC")
        return True


# --- 3. The Facade ---
class OrderFulfillmentFacade:
    """
    Provides a simplified interface for the complex order fulfillment process.

    Single Responsibility (SRP):
    The Facade has one job: orchestrating the workflow. It does not calculate
    taxes, connect to the database, or format email templates.
    Those responsibilities remain in the subsystems.

    Dependency Inversion (DIP):
    The Facade does not instantiate InventoryService() directly. It accepts it
    via __init__. This means you can easily pass a MockInventoryService during
    unit testing without changing the Facade's code.
    """

    # We pass dependencies through the constructor (Dependency Injection).
    # This prevents the Facade from being tightly coupled to specific
    # implementations.
    def __init__(
            self,
            inventory: InventoryProvider,
            # Depends on the Protocol, not a concrete class
            payment: PaymentProvider,
            # Depends on the Protocol, not a concrete class
            notifier: NotificationProvider
            # Depends on the Protocol, not a concrete class
    ) -> None:
        self._inventory = inventory
        self._payment = payment
        self._notifier = notifier

    def place_order(self, order: Order) -> bool:
        """The single, simplified method exposed to the client."""
        logging.info(f"--- Starting fulfillment for Order {order.order_id} ---")

        # The Facade orchestrates the workflow so the client doesn't have to.
        if not self._inventory.check_stock(order.product_id, order.quantity):
            logging.error("Fulfillment failed: Out of stock.")
            return False

        if not self._payment.process_payment(order.order_id, order.amount):
            logging.error("Fulfillment failed: Payment declined.")
            return False

        # Only reserve stock after payment succeeds
        self._inventory.reserve_stock(order.product_id, order.quantity)

        # Notify the user
        self._notifier.send_receipt(order.customer_email, order.order_id)

        logging.info(f"--- Order {order.order_id} fulfilled successfully! ---")
        return True


# --- 4. The Client Code ---
def main() -> None:
    # In a real enterprise app (like FastAPI or Django), these instances
    # would be injected automatically by a Dependency Injection container.
    inventory_svc = InventoryService()
    payment_svc = PaymentGateway()
    notification_svc = NotificationService()

    # Law of Demeter:
    # The client (main()) talks only to its direct friend (the Facade).
    # It does not need to chain calls like facade.inventory.check_stock().
    # The Facade is wired up once
    ecommerce_checkout = OrderFulfillmentFacade(
        inventory=inventory_svc,
        payment=payment_svc,
        notifier=notification_svc
    )

    # The client only needs to know about the Data Model and the Facade.
    my_order = Order(
        order_id="ORD-9921",
        product_id="SKU-MACBOOK-PRO",
        quantity=1,
        customer_email="customer@example.com",
        amount=1999.00
    )

    # A complex multi-system workflow executed in one line of code.
    ecommerce_checkout.place_order(my_order)


if __name__ == "__main__":
    main()
