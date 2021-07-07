from decimal import Decimal
from statistics import mean
from urllib.error import HTTPError

from bs4 import BeautifulSoup
from requests import Session

from snakeshot.utils.session import get_session


class Odds:
    _USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    )

    @classmethod
    def scrape(cls, slam: str, tour: str) -> dict[str, Decimal]:
        tour = tour.lower()
        url = f"https://www.oddschecker.com/tennis/{slam}/{tour}/{tour}-{slam}/winner"
        source = Odds._get_source(url)
        soup: BeautifulSoup = BeautifulSoup(source, "html.parser")
        rows = soup.find("tbody", {"id": "t1"}).findAll(
            "tr", {"class": "diff-row evTabRow bc"}
        )
        return {
            row["data-bname"]: mean(Odds._compile(row))
            for row in rows
            if len(Odds._compile(row)) != 0
        }

    @classmethod
    def _get_source(cls, url: str) -> str:
        session: Session = get_session(headers={"User-Agent": Odds._USER_AGENT})
        try:
            response = session.get(url)
            response.raise_for_status()
            return response.text
        except HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"Other error occurred: {e}")

    @classmethod
    def _compile(cls, row: BeautifulSoup) -> list[Decimal]:
        return [
            Decimal(col["data-odig"])
            for col in row.findAll("td", {"class": "bc bs oi"})
        ]
