"""HTTP utilities with retry and rate limiting."""

import logging
import os
import time
from functools import wraps
from typing import Any, Callable, TypeVar

import requests

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "20"))
SLEEP_MIN = int(os.getenv("SLEEP_MIN", "5"))
SLEEP_MAX = int(os.getenv("SLEEP_MAX", "20"))
MAX_RETRIES = 3
BACKOFF_FACTOR = 2

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}

F = TypeVar("F")


def rate_limit() -> None:
    """Apply rate limiting with random sleep between requests."""
    import random

    sleep_time = random.randint(SLEEP_MIN, SLEEP_MAX)
    logger.debug("Rate limiting: sleeping for %d seconds", sleep_time)
    time.sleep(sleep_time)


def fetch_with_retry(
    url: str, timeout: int = REQUEST_TIMEOUT, max_retries: int = MAX_RETRIES
) -> str | None:
    """Fetch a URL with exponential backoff retry logic."""
    headers = REQUEST_HEADERS.copy()
    headers.update(os.getenv("REQUEST_HEADERS_EXTRA", ""))

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            logger.debug("Successfully fetched %s", url)
            return response.text
        except requests.RequestException as exc:
            wait_time = BACKOFF_FACTOR**attempt
            logger.warning(
                "Request failed for %s (attempt %d/%d): %s. Retrying in %ds.",
                url,
                attempt + 1,
                max_retries,
                exc,
                wait_time,
            )
            if attempt < max_retries - 1:
                time.sleep(wait_time)

    logger.error("Failed to fetch %s after %d attempts", url, max_retries)
    return None


def retry_on_failure(max_retries: int = MAX_RETRIES, backoff: int = BACKOFF_FACTOR) -> Callable[[F], F]:
    """Decorator to retry a function on failure with exponential backoff."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    if attempt < max_retries - 1:
                        wait_time = backoff**attempt
                        logger.warning(
                            "%s failed (attempt %d/%d): %s. Retrying in %ds.",
                            func.__name__,
                            attempt + 1,
                            max_retries,
                            exc,
                            wait_time,
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error("%s failed after %d attempts", func.__name__, max_retries)
                        raise
            return None
        return wrapper
    return decorator