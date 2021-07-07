from decimal import Decimal
from statistics import mean

from bs4 import BeautifulSoup
import requests as requests


class Odds:
    _USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    )

    @classmethod
    def scrape(cls, slam: str, tour: str) -> dict[str, Decimal]:
        tour = tour.lower()
        url = f"https://www.oddschecker.com/tennis/{slam}/{tour}/{tour}-{slam}/winner"
        response = requests.get(url, headers={"User-Agent": Odds._USER_AGENT}).text
        soup: BeautifulSoup = BeautifulSoup(response, "html.parser")
        rows = soup.find("tbody", {"id": "t1"}).findAll(
            "tr", {"class": "diff-row evTabRow bc"}
        )
        return {
            row["data-bname"]: mean(Odds._compile(row))
            for row in rows
            if len(Odds._compile(row)) != 0
        }

    @classmethod
    def _compile(cls, row: BeautifulSoup) -> list[Decimal]:
        return [
            Decimal(col["data-odig"])
            for col in row.findAll("td", {"class": "bc bs oi"})
        ]
