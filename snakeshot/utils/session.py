import requests
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def get_session(headers=None) -> Session:
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
    if headers:
        session.headers = headers
    else:
        session.headers = {
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.93 Safari/537.36",
        }
    return session
