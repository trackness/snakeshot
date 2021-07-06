from abc import ABC, abstractmethod
from decimal import Decimal
from urllib.error import HTTPError

import requests as requests
from fuzzywuzzy import process

from snakeshot.model.odds import Odds
from snakeshot.model.player import Player
from snakeshot.model.tour import Tour
from snakeshot.model.tournament import Tournament


class Slam(ABC):
    def __init__(self, name: str, depth: int = 500):
        self._name = name
        self._depth = depth
        self._tournaments: dict[str, Tournament] = {
            tour: Tournament(self._players(tour)) for tour in ["Mens", "Womens"]
        }

    def _players(self, tour: str) -> list[Player]:
        competitors: list[Player] = self._load_draw(tour)
        player_pool: list[Player] = Tour(tour, self._depth).players
        [Slam._add_rank(c, player_pool) for c in competitors]
        odds: dict[str, Decimal] = Odds.scrape(self._name.lower(), tour)
        [Slam._add_odds(competitors, *o) for o in odds.items()]
        [c.summary() for c in competitors]
        return competitors

    @abstractmethod
    def _load_draw(self, tour: str) -> list:
        raise NotImplementedError

    @classmethod
    def _request_json(cls, url: str) -> dict:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return dict(response.json())
        except HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"Other error occurred: {e}")

    @classmethod
    def _add_rank(cls, competitor: Player, player_pool: list[Player]) -> None:
        for p in player_pool:
            if p.full_name == competitor.full_name:
                competitor.rank = p.rank
                return
        match_name = process.extractOne(
            competitor.full_name, [p.full_name for p in player_pool]
        )
        competitor.rank = next(
            p for p in player_pool if p.full_name == match_name[0]
        ).rank

    @classmethod
    def _add_odds(cls, competitors: list[Player], player: str, odds: Decimal) -> None:
        for c in competitors:
            if c.full_name == player:
                c.odds = odds
                return
        match_name = process.extractOne(player, [c.full_name for c in competitors])
        next(c for c in competitors if c.full_name == match_name[0]).odds = odds

    @property
    def results(self) -> str:
        pass
