"""
* MTGJSON Request Handling
"""
import os
from pathlib import Path
from typing import Callable, Optional

import requests
import yarl
from backoff import expo, on_exception
from limits import RateLimitItemPerHour, RateLimitItemPerSecond
from limits.storage import MemoryStorage
from limits.strategies import MovingWindowRateLimiter
from omnitils.fetch import download_file, request_header_default
from omnitils.files.archive import unpack_tar_gz
from omnitils.rate_limit import rate_limit

from hexproof.mtgjson import schema as MTGJsonTypes
from hexproof.mtgjson.enums import MTGJsonURL

# Rate limiter to safely limit MTGJSON requests
_rate_limit_storage = MemoryStorage()
_rate_limiter = MovingWindowRateLimiter(_rate_limit_storage)
_mtgjson_rate_limit = RateLimitItemPerSecond(20)
_mtgjson_gql_rate_limit = RateLimitItemPerHour(500)


"""
* Handlers
"""


def request_handler_mtgjson(func) -> Callable:
    """Wrapper for MTGJSON request functions to handle retries and rate limits.

    Notes:
        There are no known rate limits for requesting JSON file resources.
        We include a 20-per-second rate limit just to be nice.
    """
    @rate_limit(limiter=_rate_limiter, limit=_mtgjson_rate_limit)
    @on_exception(expo, requests.exceptions.RequestException, max_tries=2, max_time=1)
    def decorator(*args, **kwargs):
        return func(*args, **kwargs)
    return decorator


def request_handler_mtgjson_gql(func) -> Callable:
    """Wrapper for MTGJSON GraphQL request functions to handle retries and rate limits.

    Notes:
        MTGJSON GraphQL requests are capped at 500 per-hour per-token at the moment.
        https://mtgjson.com/mtggraphql/#rate-limits
    """
    @rate_limit(limiter=_rate_limiter, limit=_mtgjson_gql_rate_limit)
    @on_exception(expo, requests.exceptions.RequestException, max_tries=2, max_time=1)
    def decorator(*args, **kwargs):
        return func(*args, **kwargs)
    return decorator


"""
* Request Utilities
"""


@request_handler_mtgjson
def get_json(url: yarl.URL, header: Optional[dict] = None) -> dict:
    """Retrieves JSON results from a MTGJSON API request using the proper rate limits.

    Args:
        url: MTGJSON API request URL.
        header: Optional headers to include in the response.

    Returns:
        Dict containing data from the JSON response.
    """
    if header is None:
        header = request_header_default.copy()
    with requests.get(str(url), headers=header) as r:
        r.raise_for_status()
        return r.json()


"""
* Requesting JSON Assets
"""


@request_handler_mtgjson
def get_cards_atomic_all() -> dict[str, MTGJsonTypes.CardAtomic]:
    """Get a dictionary of all MTGJSON 'CardAtomic' objects mapped to their respective card names.

    Returns:
        A dict with card name as the key, MTGJSON 'CardAtomic' object as the value.
    """
    with requests.get(
        url=MTGJsonURL.BulkJSON.AtomicCards,
        headers=request_header_default.copy()
    ) as res:
        res.raise_for_status()
        _obj = res.json().get('data', [])
        return {k: MTGJsonTypes.CardAtomic(**v) for k, v in _obj.items()}


@request_handler_mtgjson
def get_card_types() -> MTGJsonTypes.CardTypes:
    """Get the current MTGJSON 'CardTypes' resource.

    Returns:
        MTGJSON 'CardTypes' object.
    """
    with requests.get(
        url=MTGJsonURL.BulkJSON.CardTypes,
        headers=request_header_default.copy()
    ) as res:
        res.raise_for_status()
        _obj = res.json().get('data', {})
        return MTGJsonTypes.CardTypes(**_obj)


@request_handler_mtgjson
def get_deck(name: str) -> MTGJsonTypes.Deck:
    """Get a target MTGJSON 'Deck' resource.

    Args:
        name: Name of the deck on MTGJSON.

    Returns:
        MTGJSON 'Deck' object.
    """
    with requests.get(
        url=(MTGJsonURL.Decks / name).with_suffix('.json'),
        headers=request_header_default.copy()
    ) as res:
        res.raise_for_status()
        _obj = res.json().get('data', {})
        return MTGJsonTypes.Deck(**_obj)


@request_handler_mtgjson
def get_deck_list() -> list[MTGJsonTypes.DeckList]:
    """Get the current MTGJSON 'DeckList' resource.

    Returns:
        A list of MTGJSON 'DeckList' objects.
    """
    with requests.get(
        url=MTGJsonURL.BulkJSON.DeckList,
        headers=request_header_default.copy()
    ) as res:
        res.raise_for_status()
        _obj = res.json().get('data', [])
        return [MTGJsonTypes.DeckList(**n) for n in _obj]


@request_handler_mtgjson
def get_keywords() -> MTGJsonTypes.Keywords:
    """Get the current MTGJSON 'Keywords' resource.

    Returns:
        MTGJSON 'Keywords' object.
    """
    with requests.get(
        url=MTGJsonURL.BulkJSON.Keywords,
        headers=request_header_default.copy()
    ) as res:
        res.raise_for_status()
        _obj = res.json().get('data', {})
        return MTGJsonTypes.Keywords(**_obj)


@request_handler_mtgjson
def get_meta() -> MTGJsonTypes.Meta:
    """Get the current MTGJSON 'Meta' resource.

    Returns:
        MTGJSON 'Meta' object.
    """
    with requests.get(
        url=MTGJsonURL.BulkJSON.Meta,
        headers=request_header_default.copy()
    ) as res:
        res.raise_for_status()
        _obj = res.json().get('data', {})
        return MTGJsonTypes.Meta(**_obj)


@request_handler_mtgjson
def get_prices_today_all() -> MTGJsonTypes.Price:
    """Get today's MTGJSON 'PriceFormats' objects mapped to their respective card UUID's.

    Returns:
        A dict with card UUID as the key, MTGJSON 'PriceFormats' object as the value.
    """
    with requests.get(
        url=MTGJsonURL.BulkJSON.AllPricesToday,
        headers=request_header_default.copy()
    ) as res:
        res.raise_for_status()
        _obj = res.json().get('data', [])
        return {k: MTGJsonTypes.PriceFormats(**v) for k, v in _obj.items()}


@request_handler_mtgjson
def get_set(card_set: str) -> MTGJsonTypes.Set:
    """Get a target MTGJSON 'Set' resource.

    Args:
        card_set: The set to look for, e.g. MH2

    Returns:
        MTGJson 'Set' object.
    """
    with requests.get(
        url=(MTGJsonURL.API / card_set.upper()).with_suffix('.json'),
        headers=request_header_default.copy()
    ) as res:
        res.raise_for_status()
        _obj = res.json().get('data', {})
        return MTGJsonTypes.Set(**_obj)


@request_handler_mtgjson
def get_set_list() -> list[MTGJsonTypes.SetList]:
    """Get the current MTGJSON 'SetList' resource.

    Returns:
        A list of MTGJSON 'SetList' objects.
    """
    with requests.get(
        url=MTGJsonURL.BulkJSON.SetList,
        headers=request_header_default.copy()
    ) as res:
        res.raise_for_status()
        _obj = res.json().get('data', [])
        return [MTGJsonTypes.SetList(**n) for n in _obj]


"""
* Downloading JSON Assets
"""


@request_handler_mtgjson
def cache_meta(path: Path) -> Path:
    """Stream a target MTGJSON 'Meta' resource and save it to a file.

    Args:
        path: Path object where the JSON data will be saved.
    """
    download_file(
        url=MTGJsonURL.BulkJSON.Meta,
        path=path)
    return path


@request_handler_mtgjson
def cache_set(card_set: str, path: Path) -> Path:
    """Stream a target MTGJSON 'Set' resource and save it to a file.

    Args:
        card_set: The set to look for, ex: MH2
        path: Path object where the JSON data will be saved.
    """
    download_file(
        url=(MTGJsonURL.Sets / card_set.upper()).with_suffix('.json'),
        path=path)
    return path


@request_handler_mtgjson
def cache_set_list(path: Path) -> Path:
    """Stream the current MTGJSON 'SetList' resource and save it to a file.

    Args:
        path: Path object where the JSON data will be saved.
    """
    download_file(
        url=MTGJsonURL.BulkJSON.SetList,
        path=path)
    return path


@request_handler_mtgjson
def cache_decks_all(path: Path, remove: bool = False) -> Path:
    """Stream the current MTGJSON 'AllDeckFiles' archive, save it, and extract it.

    Args:
        path: Directory to unpack the 'AllDeckFiles' MTGJSON archive.
        remove: Whether to remove archive after extracting.

    Returns:
        Path to the unpacked 'AllDeckFiles' MTGJSON directory.
    """
    archive = path / 'AllDeckFiles.tar.gz'
    download_file(
        url=MTGJsonURL.BulkZip.AllDeckFiles,
        path=archive)

    # Unpack the contents
    unpack_tar_gz(archive)
    if remove:
        os.remove(archive)
    return Path(path / 'AllDeckFiles')


@request_handler_mtgjson
def cache_sets_all(path: Path, remove: bool = False) -> Path:
    """Stream the current MTGJSON 'AllSetFiles' archive, save it, and extract it.

    Args:
        path: Directory to unpack the 'AllSetFiles' MTGJSON archive.
        remove: Whether to remove archive after extracting.

    Returns:
        Path to the unpacked 'AllSetFiles' MTGJSON directory.
    """
    archive = path / 'AllSetFiles.tar.gz'
    download_file(
        url=MTGJsonURL.BulkZip.AllSetFiles,
        path=archive)

    # Unpack the contents
    unpack_tar_gz(archive)
    if remove:
        os.remove(archive)
    return Path(path / 'AllSetFiles')
