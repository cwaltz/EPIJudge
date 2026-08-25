"""

https://gemini.google.com/app/a6679062c25d8ece
"""

import logging
import os
import uuid
from abc import ABC, abstractmethod
from typing import Protocol, override

# Configure basic logging for the runnable example
logging.basicConfig(level=logging.INFO, format="%(message)s")


# =====================================================================
# 1. THE PRODUCT ABSTRACTION (Interface Segregation & Dependency Inversion)
# =====================================================================
class StorageBackend(Protocol):
    """
    Protocol defining the required behavior for any storage backend.
    Using a Protocol (structural subtyping) instead of an ABC avoids
    forcing third-party SDK wrappers into a strict inheritance tree.
    """

    def upload(self, filename: str, data: bytes) -> str:
        ...


# =====================================================================
# 2. CONCRETE PRODUCTS (Single Responsibility Principle)
# =====================================================================
class S3Storage(StorageBackend):
    def upload(self, filename: str, data: bytes) -> str:
        # Simulates AWS SDK (boto3) interaction
        uri = f"s3://production-bucket/backups/{filename}"
        logging.info(f"[S3] Uploading {len(data)} bytes to {uri}")
        return uri


class AzureBlobStorage(StorageBackend):
    def upload(self, filename: str, data: bytes) -> str:
        # Simulates Azure SDK interaction
        uri = f"https://core.windows.net/blob/backups/{filename}"
        logging.info(f"[Azure Blob] Uploading {len(data)} bytes to {uri}")
        return uri


# =====================================================================
# 3. THE CREATOR (Open/Closed Principle)
# =====================================================================
class BackupService(ABC):
    """
    The Base Creator. Houses the core orchestration logic (compression,
    metadata, transaction logging) but defers infrastructure instantiation.
    """

    def execute_backup(self, payload: str, job_name: str) -> None:
        """The core business logic that relies on the factory method."""
        logging.info(f"--- Starting Backup Job: {job_name} ---")

        # Simulated pre-processing (Compression, encryption, etc.)
        processed_data = payload.encode('utf-8')
        filename = f"{job_name}_{uuid.uuid4().hex[:8]}.bak"

        # FACTORY METHOD CALL: The Creator asks subclasses for the dependency
        storage: StorageBackend = self.create_storage_backend()

        # Interact with the product strictly via its abstract interface
        destination_uri = storage.upload(filename, processed_data)
        logging.info(
            f"Backup complete. Audit log written for: {destination_uri}\n")

    @abstractmethod
    def create_storage_backend(self) -> StorageBackend:
        """The Factory Method. Subclasses must implement this."""
        pass


# =====================================================================
# 4. CONCRETE CREATORS (Liskov Substitution Principle)
# =====================================================================
class AWSBackupJob(BackupService):
    @override
    def create_storage_backend(self) -> StorageBackend:
        # Can include complex AWS-specific configuration/auth parsing here
        # ensuring the base BackupService remains oblivious to AWS logic.
        return S3Storage()


class AzureBackupJob(BackupService):
    @override
    def create_storage_backend(self) -> StorageBackend:
        # Can include Azure-specific client setup here.
        return AzureBlobStorage()


# =====================================================================
# THE DOMAIN LOGIC (The True "Client" of our Creator)
# =====================================================================
class QueueWorker:
    """
    This worker pulls jobs from a queue and processes them.
    Because of the Factory Method pattern, this class is completely
    decoupled from AWS, Azure, S3, or Blob Storage.
    """

    def __init__(self, backup_service: BackupService):
        # We inject the abstract Creator.
        self.backup_service = backup_service

    def process_batch(self, jobs: list[dict]) -> None:
        print(f"Worker starting batch processing with "
              f"{self.backup_service.__class__.__name__}...")
        for job in jobs:
            # The worker just triggers the core workflow.
            # The base BackupService will internally call its Factory Method
            # to instantiate the correct storage backend dynamically.
            self.backup_service.execute_backup(job["payload"], job["name"])


# =====================================================================
# APPLICATION BOOTSTRAP (Wiring it together)
# =====================================================================
def get_configured_backup_service() -> BackupService:
    """
    In a real app, this reads environment variables or a database config
    to determine which infrastructure to use at runtime.
    """
    provider = os.getenv("CLOUD_PROVIDER", "AWS").upper()

    match provider:
        case "AWS":
            return AWSBackupJob()
        case "AZURE":
            return AzureBackupJob()
        case _:
            raise ValueError(f"Unsupported cloud provider: {provider}")


if __name__ == "__main__":
    # 1. Simulate an incoming batch of jobs from an API or Message Queue
    incoming_jobs = [
        {"name": "finance_db_q1", "payload": "ledger_data..."},
        {"name": "user_logs_wk1", "payload": "session_data..."}
    ]

    # 2. Bootstrap: Resolve the environment configuration
    # Try changing this to 'AZURE' in your environment!
    os.environ["CLOUD_PROVIDER"] = "AZURE"
    active_service = get_configured_backup_service()

    # 3. Execution: Pass the configured service into the worker
    worker = QueueWorker(active_service)
    worker.process_batch(incoming_jobs)
