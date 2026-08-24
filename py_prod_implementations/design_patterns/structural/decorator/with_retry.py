"""
Source: https://gemini.google.com/app/2dd5d989eaecd5bd

Staff-Level Python Implementation: A Parameterized Retry

When writing decorators in Python, staff engineers know two rules: you must
preserve the original function's metadata using functools.wraps, & if you want
your decorator to accept arguments, you need three layers of nested functions.

Here is a practical, production-ready retry decorator that you might find in a
modern microservice:
"""

import functools
import logging
import time


def with_retry(max_retries: int = 3, delay: int = 1):
    """
    A decorator that retries a failing function before giving up.
    """

    def decorator(func):
        # @wraps preserves the original function's name and docstring.
        # Without this, debugging becomes a nightmare because every
        # decorated function would show up as 'wrapper' in stack traces.
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    # Attempt to execute the inner function
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logging.warning(
                        f"Attempt {attempts} failed: {e}. "
                        f"Retrying in {delay}s...")
                    time.sleep(delay)

            # Final attempt - if this fails, we let the exception bubble up
            return func(*args, **kwargs)

        return wrapper

    return decorator


# --- Usage ---

@with_retry(max_retries=5, delay=2)
def fetch_user_data(user_id: str):
    # Simulated network call that might temporarily fail
    print(f"Fetching data for {user_id}...")
    raise ConnectionError("Connection timed out")

# When you call fetch_user_data("user_123"), it is actually executing 'wrapper'
