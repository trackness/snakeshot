from concurrent.futures import ThreadPoolExecutor

from snakeshot.model.tournament import Tournament
from loguru import logger


class Slam:
    _assoc = {"Mens": "ATP", "Womens": "WTA"}

    def __init__(self, name: str, year: int, depth: int = 1000):
        logger.info(f"Generating {name} {year} tournament")
        self._name = name
        self._year = year
        self._depth = depth
        self._tournaments = {}
        with ThreadPoolExecutor(max_workers=2) as pool:
            [
                pool.submit(self._tour, gender, self._tournaments)
                for gender in Slam._assoc.keys()
            ]

    def _tour(self, gender: str, tournaments: dict):
        tournaments[gender] = Tournament(self._name, self._year, gender, self._depth)

    def as_dict(self) -> dict:
        logger.info(f"Generating {self._name} {self._year} dict")
        return {tour: t.as_dict() for tour, t in self._tournaments.items()}

    @property
    def tournaments(self) -> dict:
        return self._tournaments
