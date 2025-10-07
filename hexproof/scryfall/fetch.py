"""
* Scryfall Request Handling
"""
from pathlib import Path
from typing import Callable, Optional

import requests
import yarl
from backoff import expo, on_exception
from limits import RateLimitItemPerSecond
from limits.storage import MemoryStorage
from limits.strategies import MovingWindowRateLimiter
from omnitils.fetch import download_file, request_header_default
from omnitils.rate_limit import rate_limit
from omnitils.strings import normalize_str
from requests import RequestException

from hexproof.scryfall import schema as ScrySchema
from hexproof.scryfall.enums import ScryURL

# Rate limiter to safely limit Scryfall requests
_rate_limit_storage = MemoryStorage()
_rate_limiter = MovingWindowRateLimiter(_rate_limit_storage)
_rate_limit = RateLimitItemPerSecond(20)


"""
* Handlers
"""


def request_handler_scryfall(func) -> Callable:
    """Wrapper for a Scryfall request function to handle retries and rate limits.

    Notes:
        Scryfall recommends a 5-10 millisecond delay between requests.
        We target the floor of this recommendation: 20 requests/second.
        Might consider dropping this to 10 requests/second in the future.
        https://scryfall.com/docs/api

    Args:
        func: Scryfall request function to wrap.

    Returns:
        The wrapped function.
    """
    @rate_limit(limiter=_rate_limiter, limit=_rate_limit)
    @on_exception(expo, RequestException, max_tries=2, max_time=1)
    def decorator(*args, **kwargs):
        return func(*args, **kwargs)
    return decorator


"""
* Request Utilities
"""


@request_handler_scryfall
def get_file(url: yarl.URL, path: Path, header: Optional[dict] = None) -> Optional[Path]:
    """Download a file from Scryfall's CDN (jpeg, svg, etc) using the appropriate rate limits.

    Note:
        See docs: https://scryfall.com/docs/api/images

    Args:
        url: Scryfall CDN resource URL.
        path: Path to save the file.
        header: Optional header to pass with the request.

    Returns:
        Path if the file is successfully downloaded.
    """
    return Path(
        download_file(
            url=url,
            path=path,
            header=header))


@request_handler_scryfall
def get_json(url: yarl.URL, header: Optional[dict] = None) -> dict:
    """Retrieves JSON results from a Scryfall API request using the appropriate rate limits.

    Args:
        url: Scryfall API request URL.
        header: Optional header to pass with the request.

    Returns:
        Dict containing data from the JSON response.
    """
    if header is None:
        header = request_header_default.copy()
    with requests.get(str(url), headers=header) as r:
        r.raise_for_status()
        return r.json()


def get_paginated_list(
    url: yarl.URL,
    list_object: ScrySchema.ScryfallListSchema = ScrySchema.ListObject,
    header: Optional[dict] = None
) -> ScrySchema.ScryfallList:
    """Processes a Scryfall API request which returns paginated results, appending each page of results to
        the first ListObject gathered.

    Args:
        url: Scryfall API request URL.
        list_object: Scryfall schema to use when processing the ListObject returned.
        header: Optional header to pass with the request.

    Returns:
        A ListObject (CardList, SetList, etc) containing the results of all pages.
    """

    # Grab the first page
    obj = list_object(
        **get_json(
            url=url,
            header=header))

    # Append the next page of results
    if obj.has_more and obj.next_page:
        obj.data.extend(
            get_paginated_list(
                url=yarl.URL(obj.next_page),
                list_object=list_object,
                header=header
            ).data)
    return obj


"""
* Request Object
* Schema: Card
"""


def get_card_unique(uid: str, header: Optional[dict] = None) -> ScrySchema.Card:
    """Grabs a 'Card' object from Scryfall's `/cards/{uid}` endpoint.

    Args:
        uid: The unique Scryfall ID of the card.
        header: Optional header to pass with the request.

    Returns:
        A Scryfall 'Card' object.
    """
    url = ScryURL.API.Cards.Main / uid
    return ScrySchema.Card(
        **get_json(
            url=url,
            header=header))


def get_card_numbered(
    set_code: str,
    number: str,
    lang: Optional[str] = None,
    header: Optional[dict] = None
) -> ScrySchema.Card:
    """Grabs a 'Card' object from Scryfall's `/cards/{set}/{num}/{lang}` endpoint.

    Args:
        set_code: Set containing this card.
        number: Collector number of the card within the given set.
        lang: Optional language printing to retrieve.
        header: Optional header to pass with the request.

    Returns:
        A Scryfall 'Card' object.
    """
    url = ScryURL.API.Cards.Main / set_code / number
    if lang:
        url = url / lang

    # Request data
    return ScrySchema.Card(
        **get_json(
            url=url,
            header=header))


def get_card_named(
    name: str,
    set_code: Optional[str] = None,
    exact: bool = True,
    header: Optional[dict] = None
) -> ScrySchema.Card:
    """Grabs a 'Card' object from Scryfall's `/cards/named/{name}` endpoint.

    Args:
        name: The name of the card.
        set_code: Optionally limit the search to one set.
        exact: Whether to use exact name search or fuzzy.
        header: Optional header to pass with the request.

    Returns:
        A Scryfall 'Card' object.
    """

    # Create the base query
    search_method = 'exact' if exact else 'fuzzy'
    query = {search_method: normalize_str(name)}
    if set_code is not None:
        query['set'] = set_code.lower()
    url = ScryURL.API.Cards.Named.with_query(query)

    # Request data
    return ScrySchema.Card(
        **get_json(
            url=url,
            header=header))


"""
* Request Object
* Schema: Catalog
"""


def get_catalog(name: str, header: Optional[dict] = None) -> ScrySchema.Catalog:
    """Grabs a 'Catalog' object from Scryfall's `/catalogs/{name}` endpoint.

    Args:
        name: Name of the catalog to look for.
        header: Optional header to pass with the request.

    Returns:
        A Scryfall 'Catalog' object.
    """
    url = ScryURL.API.Catalogs.Main / name.lower()

    # Request data
    return ScrySchema.Catalog(
        **get_json(
            url=url,
            header=header))


"""
* Request Object
* Schema: Set
"""


def get_set(set_code: str, header: Optional[dict] = None) -> ScrySchema.Set:
    """Grabs a 'Set' object from Scryfall's `/sets/{code}` endpoint.

    Args:
        set_code: The set to look for, e.g. MH2
        header: Optional header to pass with the request.

    Returns:
        A Scryfall 'Set' object.
    """
    url = ScryURL.API.Sets.All / set_code.lower()

    # Request data
    return ScrySchema.Set(
        **get_json(
            url=url,
            header=header))


"""
* Request List of Objects
* Schema: SetList, CardList, RulingList
"""


def get_card_rulings(set_code: str, number: str, header: Optional[dict] = None) -> list[ScrySchema.Ruling]:
    """Grab a 'RulingList' object from Scryfall's `/cards/{code}/{number}/rulings` endpoint and
        return the list of 'Ruling' objects.

    Args:
        set_code: The set code of the card to look for, e.g. MH2
        number: The collector number of the card to look for, as a string.
        header: Optional header to pass with the request.

    Returns:
        A list of Scryfall 'Ruling' objects.
    """
    url = ScryURL.API.Cards.Main / set_code.lower() / number / 'rulings'

    # Request data
    return get_paginated_list(
        url=url,
        list_object=ScrySchema.RulingList,
        header=header
    ).data


def get_card_list(params: Optional[dict] = None, header: Optional[dict] = None) -> list[ScrySchema.Card]:
    """Grab a 'CardList' object from Scryfall's `/cards/search` endpoint matching a provided query
        and return the list of 'Card' objects.

    Args:
        params: Search parameters to pass with request.
        header: Optional header to pass with the request.

    Returns:
        A list of Scryfall 'Card' objects.
    """
    url = ScryURL.API.Cards.Search.with_query(params)

    # Request data
    return get_paginated_list(
        url=url,
        list_object=ScrySchema.CardList,
        header=header
    ).data


def get_set_list(header: Optional[dict] = None) -> list[ScrySchema.Set]:
    """Grab a 'SetList' object from Scryfall's `/sets/` endpoint and return the list of 'Set' objects.

    Args:
        header: Optional header to pass with the request.

    Returns:
        A list of Scryfall 'Set' objects.
    """
    # Request data
    return get_paginated_list(
            url=ScryURL.API.Sets.All,
            list_object=ScrySchema.SetList,
            header=header
    ).data


"""
* Downloading JSON Assets
"""


@request_handler_scryfall
def cache_set_list(path: Path, header: Optional[dict] = None) -> Path:
    """Stream the current Scryfall 'Sets' resource and save it to a file.

    Args:
        path: Path object where the JSON data will be saved.
        header: Optional header to pass with the request.

    Returns:
        Path where the JSON file was saved.
    """
    download_file(
        url=ScryURL.API.Sets.All,
        path=path,
        header=header)
    return path
