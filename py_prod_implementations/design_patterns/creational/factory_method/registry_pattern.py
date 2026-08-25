"""
Google Gemini chat:
https://gemini.google.com/app/a6679062c25d8ece

Prompt:

is our latest implementation (for which we generated mermaid code) of an
enterprise production grade from the POV of design patterns and SOLID
principles? or is there a way to get rid of the simple factory and improve it
further?

let me be clear: I am NOT going to run it in production. I am only studying
the factory method design pattern exclusively for staff engineering interviews.


Response:

This is exactly the kind of critical thinking expected in a staff-level
interview. You identified the "seam" in the design where a SOLID principle (
the Open/Closed Principle) was intentionally compromised.

To answer your question directly: Yes, the previous implementation is
production-grade for 90% of enterprise applications. Pragmatism often beats
purity, and a single match/case block at the entry point of an application is
a widely accepted, low-cost trade-off.

However, for a staff-level interview, you need to show that you know how to
achieve 100% pure OCP if the system demands it (for example, if you are
building a framework where third-party developers can drop in their own cloud
plugins).

To get rid of the Simple Factory's match/case statement, we upgrade it using
the Registry Pattern.

The Staff-Level Upgrade: The Registry Pattern Instead of a centralized
function acting as a traffic cop who knows about every single cloud provider,
we use a Pythonic approach (Decorators) to let the classes register themselves.

Here is how you rewrite the bootstrapping phase to be strictly Open/Closed:
"""

import os
from typing import Type

# 1. THE REGISTRY
# A simple dictionary mapping string names to class types.
BACKUP_PROVIDERS: dict[str, Type['BackupService']] = {}


# 2. THE REGISTRATION DECORATOR
def register_provider(provider_name: str):
    """Decorator to automatically register a new provider class."""

    def decorator(cls: Type['BackupService']):
        BACKUP_PROVIDERS[provider_name.upper()] = cls
        return cls

    return decorator


# ---------------------------------------------------------
# 3. THE CLASSES (Notice the decorators!)
# ---------------------------------------------------------
@register_provider("AWS")
class AWSBackupJob(BackupService):
    def create_storage_backend(self) -> StorageBackend:
        return S3Storage()


@register_provider("AZURE")
class AzureBackupJob(BackupService):
    def create_storage_backend(self) -> StorageBackend:
        return AzureBlobStorage()


# ---------------------------------------------------------
# 4. THE PURE OCP BOOTSTRAPPER (No more match/case!)
# ---------------------------------------------------------
def get_configured_backup_service() -> BackupService:
    """
    This function now perfectly obeys the Open/Closed Principle.
    It never changes, even if you add 50 new cloud providers.
    """
    provider_name = os.getenv("CLOUD_PROVIDER", "AWS").upper()

    # We simply look up the class in the registry dictionary
    provider_class = BACKUP_PROVIDERS.get(provider_name)

    if not provider_class:
        raise ValueError(f"Unsupported cloud provider: {provider_name}")

    return provider_class()  # Instantiate and return


"""
Why this is a Staff-Level Masterclass If you present this progression in 
an interview, you demonstrate deep architectural maturity:

True Open/Closed Compliance: If your company acquires a startup using Google 
Cloud, a developer simply writes @register_provider("GCP") \n class 
GCPBackupJob.... They do not touch the registry, they do not touch the 
get_configured_backup_service() function, and they do not touch the Worker. 
The system is extended purely by adding new code, never modifying existing code.

Inversion of Control (IoC): You moved the responsibility of "knowing what 
exists" from the central factory out to the individual modules.

Plugin Architecture: This exact pattern is how tools like Flask, Click, 
or Celery allow you to register routes, commands, or tasks dynamically. It is 
the foundation of extensible system design.

The Interview Takeaway: When asked to design a system, start with the Simple 
Factory for your Composition Root, acknowledge the OCP violation out loud, 
and explain that you would switch to a Decorator-based Registry Pattern if 
the system required dynamic plugin architecture. This shows you understand 
both theory and pragmatic engineering.
"""
