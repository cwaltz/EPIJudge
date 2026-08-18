import base64
import gzip
import logging
from typing import Protocol

# Configure logging for visibility into the data flow
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class DataStore(Protocol):
    """
    Interface Segregation Principle (ISP):
    The protocol mandates only what is absolutely necessary for a data store.
    Any class implementing both `write` and `read` automatically satisfies this
    protocol.
    """

    def write(self, data: str) -> None:
        ...

    def read(self) -> str:
        ...


class InMemoryFileStore:
    """
    Single Responsibility Principle (SRP):
    Strictly responsible for persisting and retrieving raw string data.
    It knows nothing about encoding, compression, or the outside world.
    """

    def __init__(self, filename: str) -> None:
        self._filename = filename
        self._storage = ""

    def write(self, data: str) -> None:
        logger.info(f"[Store] Writing data to disk '{self._filename}'...")
        self._storage = data

    def read(self) -> str:
        logger.info(f"[Store] Reading data from disk '{self._filename}'...")
        return self._storage


class BaseStoreDecorator:
    """
    Liskov Substitution Principle (LSP):
    This decorator acts as a DataStore, but also safely delegates back to a
    DataStore. We can swap it in for the base component without the client
    knowing.
    """

    def __init__(self, wrappee: DataStore) -> None:
        self._wrappee = wrappee

    def write(self, data: str) -> None:
        self._wrappee.write(data)

    def read(self) -> str:
        return self._wrappee.read()


class Base64EncodingDecorator(BaseStoreDecorator):
    """
    Open/Closed Principle (OCP):
    We extend the store's behavior to support Base64 encoding/decoding
    without ever touching the InMemoryFileStore code.
    """

    def write(self, data: str) -> None:
        logger.info("[Decorator: Base64] Encoding data on write.")
        encoded_data = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        self._wrappee.write(encoded_data)

    def read(self) -> str:
        encoded_data = self._wrappee.read()
        logger.info("[Decorator: Base64] Decoding data on read.")
        return base64.b64decode(encoded_data.encode("utf-8")).decode("utf-8")


class GZipCompressionDecorator(BaseStoreDecorator):
    """
    Symmetrical Operations:
    Compresses strings down to hex on write, and inflates hex to strings on
    read.
    """

    def write(self, data: str) -> None:
        logger.info("[Decorator: GZip] Compressing data on write.")
        compressed_bytes = gzip.compress(data.encode("utf-8"))
        compressed_hex = compressed_bytes.hex()
        self._wrappee.write(compressed_hex)

    def read(self) -> str:
        compressed_hex = self._wrappee.read()
        logger.info("[Decorator: GZip] Decompressing data on read.")
        compressed_bytes = bytes.fromhex(compressed_hex)
        decompressed_data = gzip.decompress(compressed_bytes)
        return decompressed_data.decode("utf-8")


class StoreClient:
    """
    Dependency Inversion Principle (DIP):
    The client relies solely on the `DataStore` abstraction. It does not know
    whether the store is compressed, encoded, or just raw text.
    """

    def __init__(self, store: DataStore):
        self._store = store

    def save_salary_records(self, records: str) -> None:
        logger.info("--- Client Initiating Save ---")
        self._store.write(records)

    def load_salary_records(self) -> str:
        logger.info("--- Client Initiating Load ---")
        return self._store.read()


if __name__ == "__main__":
    sensitive_data = ("employee: Alice, salary: $150,000 | "
                      "employee: Bob, salary: $140,000")

    # 1. Create the base component
    raw_store = InMemoryFileStore("salaries.dat")

    # 2. Stack the decorators
    # The innermost layer is GZip, the outermost is Base64.
    secure_store = Base64EncodingDecorator(
        GZipCompressionDecorator(raw_store)
    )

    # 3. Inject into the client
    client = StoreClient(secure_store)

    # --- EXECUTION FLOW ---

    # Write Flow (Top-Down): Base64 -> GZip -> Store
    client.save_salary_records(sensitive_data)

    # Use the public interface of the raw component to inspect the data,
    # completely bypassing the decorators while respecting encapsulation.
    print(
        f"\n[DEBUG] Raw storage payload looks like this:\n{raw_store.read()}\n")

    # Read Flow (Bottom-Up): Store -> GZip -> Base64
    retrieved_data = client.load_salary_records()

    print(f"\n[DEBUG] Final retrieved payload:\n{retrieved_data}")

    assert sensitive_data == retrieved_data, ("Data mismatch! Bidirectional "
                                              "decorators failed.")
    print("\nSUCCESS: Symmetrical write/read operations completed flawlessly.")
