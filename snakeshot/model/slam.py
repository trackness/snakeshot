from snakeshot.model.tournament import Tournament
from loguru import logger


class Slam:
    _assoc = {"Mens": "ATP", "Womens": "WTA"}

    def __init__(self, name: str, year: int, depth: int = 500):
        logger.info(f"Generating {name} {year} tournament")
        self._name = name
        self._year = year
        self._depth = depth
        self._tournaments: dict = {
            gender: Tournament(name, year, gender, depth)
            for gender in ["Mens", "Womens"]
        }

    def as_dict(self) -> dict:
        logger.info(f"Generating {self._name} {self._year} dict")
        return {tour: t.as_dict() for tour, t in self._tournaments.items()}

    @property
    def tournaments(self) -> dict:
        return self._tournaments
