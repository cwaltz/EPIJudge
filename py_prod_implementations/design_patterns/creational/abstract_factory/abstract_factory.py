"""
Google Gemini chat:
https://gemini.google.com/app/62f33b9f4217dd29

Abstract Factory Pattern in Modern Python (SOLID-Compliant)

Use Case:
    Multi-Cloud Event Exporter requiring compatible Storage and Queue services.
"""

from abc import ABC, abstractmethod
from typing import override


# =====================================================================
# 1. ABSTRACT PRODUCTS (Interface Segregation Principle - ISP)
# =====================================================================
class BlobStorage(ABC):
    """Abstract Product A: Interface for file/object storage."""

    @abstractmethod
    def upload(self, filename: str, data: bytes) -> str:
        """Uploads data and returns the resource URI."""
        pass


class MessageQueue(ABC):
    """Abstract Product B: Interface for message broker/queue."""

    @abstractmethod
    def publish(self, topic: str, message: str) -> None:
        """Publishes an event/notification to a topic."""
        pass


# =====================================================================
# 2. CONCRETE PRODUCTS: AWS Family
# =====================================================================
class S3BlobStorage(BlobStorage):
    @override
    def upload(self, filename: str, data: bytes) -> str:
        return f"s3://production-bucket/{filename} ({len(data)} bytes)"


class SQSMessageQueue(MessageQueue):
    @override
    def publish(self, topic: str, message: str) -> None:
        print(f"[AWS SQS] Sent to '{topic}': {message}")


# =====================================================================
# 3. CONCRETE PRODUCTS: Local/Dev/Test Family
# =====================================================================
class LocalDiskStorage(BlobStorage):
    @override
    def upload(self, filename: str, data: bytes) -> str:
        return f"file:///tmp/dev-storage/{filename} ({len(data)} bytes)"


class InMemoryQueue(MessageQueue):
    @override
    def publish(self, topic: str, message: str) -> None:
        print(f"[Local In-Memory Queue] Topic '{topic}' received: {message}")


# =====================================================================
# 4. ABSTRACT FACTORY
# =====================================================================
class CloudInfrastructureFactory(ABC):
    """
    The Abstract Factory declares methods that return abstract products.
    It guarantees that all created products belong to the same family.
    """

    @abstractmethod
    def create_storage(self) -> BlobStorage:
        pass

    @abstractmethod
    def create_queue(self) -> MessageQueue:
        pass


# =====================================================================
# 5. CONCRETE FACTORIES (Open/Closed Principle - OCP)
# =====================================================================
class AWSFactory(CloudInfrastructureFactory):
    @override
    def create_storage(self) -> BlobStorage:
        return S3BlobStorage()

    @override
    def create_queue(self) -> MessageQueue:
        return SQSMessageQueue()


class LocalDevFactory(CloudInfrastructureFactory):
    @override
    def create_storage(self) -> BlobStorage:
        return LocalDiskStorage()

    @override
    def create_queue(self) -> MessageQueue:
        return InMemoryQueue()


# =====================================================================
# 6. CLIENT CODE (Dependency Inversion Principle - DIP)
# =====================================================================
class InvoiceProcessingService:
    """
    High-level business service.
    Depends only on the Abstract Factory and Abstract Products.
    """

    def __init__(self, factory: CloudInfrastructureFactory) -> None:
        # The factory provides compatible tools for the environment
        self.storage: BlobStorage = factory.create_storage()
        self.queue: MessageQueue = factory.create_queue()

    def process_invoice(self, invoice_id: str, payload: bytes) -> None:
        filename = f"invoice_{invoice_id}.pdf"

        # 1. Store the asset
        uri = self.storage.upload(filename=filename, data=payload)
        print(f"Stored file at: {uri}")

        # 2. Notify subscribers
        self.queue.publish(
            topic="invoices.processed",
            message=f"Invoice {invoice_id} stored at {uri}",
        )


# =====================================================================
# 7. RUNTIME EXECUTION (Composition Root)
# =====================================================================
def get_factory(environment: str) -> CloudInfrastructureFactory:
    """Resolves the infrastructure factory, failing fast on invalid
    configurations."""
    factories: dict[str, type[CloudInfrastructureFactory]] = {
        "production": AWSFactory,
        "development": LocalDevFactory,
    }

    # 1. Look up the factory without a default fallback
    factory_cls = factories.get(environment.lower())

    # 2. Fail fast if the environment is unknown
    if not factory_cls:
        valid_envs = ", ".join(factories.keys())
        raise ValueError(
            f"CRITICAL: Unknown environment '{environment}'. "
            f"Must be one of: [{valid_envs}]"
        )

    return factory_cls()


if __name__ == "__main__":
    sample_payload = b"%PDF-1.4 Invoice Data Sample..."

    print("--- 1. Running in Development Environment ---")
    dev_factory = get_factory("development")
    dev_service = InvoiceProcessingService(dev_factory)
    dev_service.process_invoice(invoice_id="DEV-101", payload=sample_payload)

    print("\n--- 2. Running in Production Environment ---")
    prod_factory = get_factory("production")
    prod_service = InvoiceProcessingService(prod_factory)
    prod_service.process_invoice(invoice_id="PROD-909", payload=sample_payload)
