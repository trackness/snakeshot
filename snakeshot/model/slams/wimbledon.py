from snakeshot.model.player import Player
from snakeshot.model.slam import Slam

from loguru import logger


class Wimbledon(Slam):
    def __init__(self, year: int, depth: int = 1000):
        self._name = "Wimbledon"
        logger.info(f"Generating tournament for {self._name} {year}")
        self._base_url = f"https://www.wimbledon.com/en_GB/scores/feeds/{year}/draws"
        super().__init__(depth)

    @classmethod
    def _tour(cls, tour: str) -> str:
        return {"Mens": "MS", "Womens": "LS"}.get(tour)

    def _load_draw(self, tour: str) -> list[Player]:
        logger.info(f"Loading {tour} {self._name} players")
        matches: list[dict] = self._matches_json(tour)
        players = []
        for i, m in enumerate(matches):
            [
                players.insert(
                    i * 2 + p, Wimbledon._team_to_player(m.get(f"team{p + 1}"))
                )
                for p in range(2)
            ]
        return players

    def _matches_json(self, tour) -> list[dict]:
        index: list = Slam._request_json(f"{self._base_url}/draws.json").get("draws")
        draw_url: str = next(
            t for t in index if t.get("id") == Wimbledon._tour(tour)
        ).get("feed_url")
        draw_json: dict = Slam._request_json(draw_url)
        return draw_json.get("matches")[:64]

    @classmethod
    def _team_to_player(cls, team: dict) -> Player:
        player = Player(
            first_name=team.get("firstNameA"),
            last_name=team.get("lastNameA"),
            nationality=team.get("nationA"),
        )
        if team.get("seed"):
            player.seed = team.get("seed")
        if team.get("entryStatus"):
            player.entry_type = team.get("entryStatus")
        Slam._log_draw_player(player)
        return player


if __name__ == "__main__":
    w = Wimbledon(2021)
