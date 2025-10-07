"""
* MTGPics Data Requests
"""
from typing import Callable, Optional

import requests
import yarl
from backoff import expo, on_exception
from limits import RateLimitItemPerSecond
from limits.storage import MemoryStorage
from limits.strategies import MovingWindowRateLimiter
from omnitils.exceptions import return_on_exception
from omnitils.fetch import request_header_default
from omnitils.rate_limit import rate_limit

"""
* MTGPics Request Handlers
"""

# Rate limiter to safely limit MTGPics requests
_rate_limit_storage = MemoryStorage()
_rate_limiter = MovingWindowRateLimiter(_rate_limit_storage)
_rate_limit = RateLimitItemPerSecond(20)


def request_handler_mtgpics(func: Callable) -> Callable:
    """Wrapper for a MTGPics request function to handle retries, rate limits, and a final exception catch.

    Args:
        func: The decorated function.

    Returns:
        Wrapped function.
    """

    @rate_limit(limiter=_rate_limiter, limit=_rate_limit)
    @on_exception(expo, requests.exceptions.RequestException, max_tries=2, max_time=1)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


"""
* Page Requests
"""


@return_on_exception(None)
@request_handler_mtgpics
def get_page_html(url: str | yarl.URL, headers: Optional[dict[str, str]] = None) -> Optional[bytes]:
    """Grab the HTML from a page on MTGPics.

    Args:
        url: URL to the page.
        headers: Headers object to pass with request, uses default if not provided.

    Returns:
        The page as bytes if successful, None otherwise.
    """
    headers = request_header_default.copy() if headers is None else headers
    with requests.get(url, headers=headers) as r:
        r.raise_for_status()

        # Check known cases of invalid page returned
        if "Wrong ref or number." not in r.text:
            if "No card found." not in r.text:
                return r.content
        return None
