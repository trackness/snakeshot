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
    return session
