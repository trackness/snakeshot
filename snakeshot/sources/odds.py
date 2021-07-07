from decimal import Decimal
from statistics import mean
from urllib.error import HTTPError

from bs4 import BeautifulSoup
from requests import Session, Response

from snakeshot.utils.session import get_session


class Odds:
    @classmethod
    def scrape(cls, slam: str, tour: str) -> dict[str, Decimal]:
        tour = tour.lower()
        url = f"https://www.oddschecker.com/tennis/{slam}/{tour}/{tour}-{slam}/winner"
        response = Odds._get_source(url)
        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
        try:
            table = soup.find("tbody", {"id": "t1"})
        except Exception as e:
            print(f"No odds table found: {e}")
            return {}
        try:
            rows = table.findAll("tr", {"class": "diff-row evTabRow bc"})
        except Exception as e:
            print(f"No odds rows found: {e}")
            return {}
        return {
            row["data-bname"]: mean(Odds._compile(row))
            for row in rows
            if len(Odds._compile(row)) != 0
        }

    @classmethod
    def _get_source(cls, url: str) -> Response:
        session: Session = get_session()
        try:
            response: Response = session.get(url)
            response.raise_for_status()
            return response
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


if __name__ == "__main__":
    o = Odds.scrape("wimbledon", "mens")
    [print(f"{k} - {float(v)}") for k, v in o.items()]
