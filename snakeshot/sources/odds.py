from decimal import Decimal
from statistics import mean
from urllib.error import HTTPError
from loguru import logger

from bs4 import BeautifulSoup
from requests import Session, Response

from snakeshot.utils.session import get_session


class Odds:
    def __init__(self, slam: str, tour: str):
        self._slam = slam
        self._tour = tour
        self._url = (
            f"https://www.oddschecker.com/tennis/"
            f"{self._slam.lower()}/{self._tour.lower()}/"
            f"{self._tour.lower()}-{self._slam.lower()}/winner"
        )
        logger.info(f"Scraping {self._tour} odds from {self._url}")
        response: str = self._get_source()
        if response == "" or response is None:
            self._odds = {}
            return
        rows = Odds._find_rows(response)
        if len(rows) == 0 or rows is None:
            self._odds = {}
            return
        self._odds = self._from_rows(rows)

    @property
    def odds(self):
        return self._odds if self._odds is not None else {}

    def _get_source(self) -> str:
        session: Session = get_session()
        try:
            response: Response = session.get(self._url)
            response.raise_for_status()
            return response.text
        except HTTPError as e:
            logger.error(f"HTTP error: {e}")
        except Exception as e:
            logger.error(f"Other error: {e}")

    @classmethod
    def _find_rows(cls, source: str):
        try:
            soup: BeautifulSoup = BeautifulSoup(source, "html.parser")
            return soup.findAll("tr", {"class": "diff-row evTabRow bc"})
        except Exception as e:
            logger.warning(f"No odds rows found: {e}")

    def _from_rows(self, rows) -> dict[str, Decimal]:
        odds = {}
        for row in rows:
            try:
                player_odds = Odds._from_row(row)
                if player_odds is not None:
                    odds.update(player_odds)
            except Exception as e:
                logger.warning(f"Unable to generate {self._tour} odds: {e}")
        return odds

    @classmethod
    def _from_row(cls, row) -> dict[str, Decimal]:
        name = row["data-bname"]
        try:
            columns = row.findAll("td", {"class": "bc bs oi"})
            if len(columns) != 0:
                return {
                    name: mean([Decimal(column["data-odig"]) for column in columns])
                }
            else:
                logger.warning(f"No odds columns found for {name}")
        except Exception as e:
            logger.warning(f"Unable to generate odds for {name}: {e}")
