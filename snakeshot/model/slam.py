from abc import ABC

from snakeshot.model.player import Player
from snakeshot.model.tour import Tour


class Slam(ABC):
    def __init__(self, config: dict, pool_depth: int = 1000):
        self._player_pools: dict[str, list[Player]] = {
            "M": Tour("ATP", pool_depth).players,
            "W": Tour("WTA", pool_depth).players,
        }
        # odds: Odds(config.get("slam"), config.get("tour"))
        Slam._set_odds(Slam._scrape_odds_list(), self._player_pools)

    @classmethod
    def _scrape_odds_list(
        cls,
    ) -> dict[str, list]:
        pass

    @classmethod
    def _set_odds(cls, odds, players):
        pass

    wim_m = "https://www.oddschecker.com/tennis/wimbledon/mens/mens-wimbledon/winner"
    wim_w = (
        "https://www.oddschecker.com/tennis/wimbledon/womens/womens-wimbledon/winner"
    )
