from decimal import Decimal
from statistics import mean
from loguru import logger

from bs4 import BeautifulSoup

from snakeshot.utils import session


base_url = "https://www.oddschecker.com/tennis"


class Odds:
    def __init__(self, slam: str, tour: str):
        self._slam = slam.replace("_", "-")
        self._tour = tour
        rows = []
        urls = Odds._urls(2021, self._slam, self._tour)
        for url in urls:
            rows = self._fetch(url)
            if rows:
                break
        if not rows:
            logger.warning(f"No odds rows found in response from : {urls}")
            self._odds = {}
        else:
            self._odds = self._from_rows(rows)

    def _fetch(self, url: str) -> []:
        response = session.get(url, description=f"{self._tour} odds").text
        if response == "" or response is None:
            logger.warning(f"Invalid response received from {url}")
            return
        rows = Odds._find_rows(response)
        if len(rows) == 0 or rows is None:
            logger.debug(f"No odds rows found in response from {url}")
            return
        return rows

    @property
    def odds(self):
        return self._odds if self._odds is not None else {}

    @staticmethod
    def _urls(year: int, slam: str, tour: str) -> list:
        slam = slam.lower()
        tour = tour.lower()
        return [
            f"{base_url}/{slam}/{tour}/{tour}-{slam}/winner",
            f"{base_url}/{slam}/{tour}/{year}-{slam}/winner",
            f"{base_url}/{slam}/{tour}/{year}-{slam}-{tour[:-1]}/winner",
        ]

    @classmethod
    def _find_rows(cls, source: str):
        try:
            soup: BeautifulSoup = BeautifulSoup(source, "html.parser")
            return soup.findAll("tr", {"class": "diff-row evTabRow bc"})
        except Exception as e:
            logger.warning(f"No odds rows found: {e}")

    def _from_rows(self, _rows) -> dict:
        _odds = {}
        for _row in _rows:
            try:
                _player_odds = Odds._from_row(_row)
                if _player_odds is not None:
                    _odds.update(_player_odds)
            except Exception as e:
                logger.warning(f"Unable to generate {self._tour} odds: {e}")
        return _odds

    @classmethod
    def _from_row(cls, _row) -> dict:
        _name = _row["data-bname"]
        try:
            _columns = _row.findAll("td", {"class": "bc"})
            if len(_columns) != 0:
                return {
                    _name: mean([Decimal(_column["data-odig"]) for _column in _columns])
                }
            else:
                logger.warning(f"No odds columns found for {_name}")
        except Exception as e:
            logger.warning(f"Unable to generate odds for {_name}: {e}")
