import requests
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from loguru import logger
from requests import HTTPError, Response


def get_session(add: dict, headers: dict) -> Session:
    session = requests.Session()
    session.mount(
        "https://",
        HTTPAdapter(
            max_retries=Retry(
                total=3,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET", "HEAD"],
                backoff_factor=1,
            )
        ),
    )
    if headers is None:
        headers = {
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.93 Safari/537.36",
        }
    if add is not None:
        headers.update(add)
    session.headers = headers
    return session


def get(
    url, description=None, stream=False, add: dict = None, headers: dict = None
) -> Response:
    session = get_session(add=add, headers=headers)
    logger.info(
        f"Fetching"
        f"{f' {description} from' if description is not None else ''} "
        f"{url}"
    )
    try:
        response = session.get(url, stream=stream)
        response.raise_for_status()
        return response
    except HTTPError as e:
        logger.error(f"HTTP error: {e}")
        return Response()
    except Exception as e:
        logger.error(f"Other error: {e}")
        return Response()


def exists(url, add: dict = None, headers: dict = None) -> bool:
    session = get_session(add=add, headers=headers)
    logger.debug(f"Checking if {url} exists")
    try:
        response = session.head(url)
        response.raise_for_status()
        if response.is_redirect:
            return False
        return response.status_code == 200
    except HTTPError as e:
        logger.error(f"HTTP error: {e}")
        return False
    except Exception as e:
        logger.error(f"Other error: {e}")
        return False
