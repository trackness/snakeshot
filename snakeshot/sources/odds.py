from decimal import Decimal
from statistics import mean
from loguru import logger

from bs4 import BeautifulSoup

from snakeshot.utils import session


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
        response = session.get(self._url, description=f"{self._tour} odds").text
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

    @classmethod
    def _find_rows(cls, source: str):
        try:
            soup: BeautifulSoup = BeautifulSoup(source, "html.parser")
            return soup.findAll("tr", {"class": "diff-row evTabRow bc"})
        except Exception as e:
            logger.warning(f"No odds rows found: {e}")

    def _from_rows(self, _rows) -> dict[str, Decimal]:
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
    def _from_row(cls, _row) -> dict[str, Decimal]:
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
