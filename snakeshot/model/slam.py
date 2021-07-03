from snakeshot.model.player import Player
from snakeshot.model.tournament import Tournament


class Slam:
    def __init__(self, players: dict[str, list[Player]]):
        self._tournaments: dict[str, Tournament] = {
            "Mens": Tournament(players.get("Mens")),
            "Womens": Tournament(players.get("Womens"))
        }
