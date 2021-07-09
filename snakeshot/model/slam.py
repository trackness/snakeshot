from snakeshot.model.tournament import Tournament


class Slam:
    _assoc = {"Mens": "ATP", "Womens": "WTA"}

    def __init__(self, name: str, year: int, depth: int = 500):
        self._name = name
        self._year = year
        self._depth = depth
        self._tournaments: dict[str, Tournament] = {
            gender: Tournament(name, year, gender, depth)
            for gender in ["Mens", "Womens"]
        }

    def as_dict(self) -> dict[str, dict]:
        return {tour: t.as_dict() for tour, t in self._tournaments.items()}

    @property
    def tournaments(self) -> dict[str, Tournament]:
        return self._tournaments
