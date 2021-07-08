from abc import ABC, abstractmethod

from decimal import Decimal
from urllib.error import HTTPError
from loguru import logger

import requests as requests
from fuzzywuzzy import process

from snakeshot.model.player import Player

from snakeshot.sources.odds import Odds
from snakeshot.sources.tour import Tour
from snakeshot.model.tournament import Tournament


class Slam(ABC):
    _assoc = {"Mens": "ATP", "Womens": "WTA"}

    def __init__(self, name: str, depth: int = 500):
        self._name = name
        self._depth = depth
        self._tournaments: dict[str, Tournament] = {
            tour: Tournament(self._players(tour)) for tour in ["Mens", "Womens"]
        }

    def __dict__(self) -> dict[str, dict]:
        return {tour: t.__dict__() for tour, t in self._tournaments.items()}

    @property
    def tournaments(self) -> dict[str, Tournament]:
        return self._tournaments

    def _players(self, tour: str) -> list[Player]:
        competitors: list[Player] = self._load_draw(tour)
        self._add_ranks(tour, competitors)
        self._add_odds(tour, competitors)
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

    def _add_ranks(self, tour: str, competitors: list[Player]):
        player_pool: list[Player] = Tour(tour, self._depth).players
        logger.info(f"Assigning {Slam._assoc.get(tour)} rankings")
        [Slam._add_rank(tour, c, player_pool) for c in competitors]

    @classmethod
    def _add_rank(cls, tour: str, competitor: Player, player_pool: list[Player]):
        for p in player_pool:
            if p.full_name == competitor.full_name:
                competitor.rank = p.rank
                logger.debug(Slam._rank_match(tour, "exact", competitor))
                return
        match_name = process.extractOne(
            competitor.full_name, [p.full_name for p in player_pool]
        )
        competitor.rank = next(
            p for p in player_pool if p.full_name == match_name[0]
        ).rank
        logger.debug(Slam._rank_match(tour, "fuzzy", competitor))

    @classmethod
    def _rank_match(cls, tour: str, method: str, player: Player) -> str:
        return (
            f"{Slam._assoc.get(tour)} rank "
            f"{f'({method})':7}: "
            f"{player.summary('tour')}"
        )

    def _add_odds(self, tour: str, competitors: list[Player]):
        odds: dict[str, Decimal] = Odds(self._name, tour).odds
        logger.info(f"Assigning {tour} odds")
        [Slam._add_odd(tour, competitors, *o) for o in odds.items()]

    @classmethod
    def _add_odd(cls, tour: str, competitors: list[Player], player: str, odds: Decimal):
        for c in competitors:
            if c.full_name == player:
                c.odds = odds
                logger.debug(Slam._odds_match(tour, "exact", c))
                return
        match_name = process.extractOne(player, [c.full_name for c in competitors])
        c = next(c for c in competitors if c.full_name == match_name[0])
        c.odds = odds
        logger.debug(Slam._odds_match(tour, "fuzzy", c))

    @classmethod
    def _odds_match(cls, tour: str, method: str, player: Player) -> str:
        return f"{tour} odds " f"{f'({method})':7}: " f"{player.summary('odds')}"
