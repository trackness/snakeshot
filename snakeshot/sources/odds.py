from decimal import Decimal
from statistics import mean
from urllib.error import HTTPError
from loguru import logger

from bs4 import BeautifulSoup
from requests import Session, Response

from snakeshot.utils.session import get_session


class Odds:
    @classmethod
    def scrape(cls, slam: str, tour: str) -> dict[str, Decimal]:
        slam = slam.lower()
        tour = tour.lower()
        url = (
            f"https://www.oddschecker.com/tennis/"
            f"{slam.lower()}/{tour.lower()}/{tour.lower()}-{slam.lower()}/winner"
        )
        logger.info(f"Scraping {tour.upper()} odds from {url}")
        response = Odds._get_source(url)
        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("tbody", {"id": "t1"})
        if table is None:
            logger.warning("No odds table found")
            return {}
        try:
            rows = table.findAll("tr", {"class": "diff-row evTabRow bc"})
        except Exception as e:
            logger.warning(f"No odds rows found: {e}")
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
            logger.error(f"HTTP error: {e}")
        except Exception as e:
            logger.error(f"Other error: {e}")

    @classmethod
    def _compile(cls, row: BeautifulSoup) -> list[Decimal]:
        return [
            Decimal(col["data-odig"])
            for col in row.findAll("td", {"class": "bc bs oi"})
        ]
