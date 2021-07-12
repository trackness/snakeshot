import json
import math

from snakeshot.model.match import Match
from snakeshot.model.player import Player
from snakeshot.model.round import Round
from snakeshot.sources.draws import Wimbledon, USOpen
from snakeshot.sources.odds import Odds
from snakeshot.sources.tour import Tour
from loguru import logger

from fuzzywuzzy import process


class Tournament:
    _slams = {
        # "australian_open": AustralianOpen,
        # "roland_garros", RolandGarros,
        "wimbledon": Wimbledon,
        "us_open": USOpen,
    }
    _assoc = {"Mens": "ATP", "Womens": "WTA"}

    def __init__(self, slam: str, year: int, gender: str, depth: int):
        players: dict = Tournament._slams.get(slam.lower())(year, gender).players
        self._rounds: list = []
        n_players = len(players)
        if not (n_players > 0 and (n_players & (n_players - 1))):
            self._n_rounds: int = int(math.log2(len(players)))
        else:
            logger.error(
                f"{year} {slam} {gender} draw player count is not a power of 2: {n_players}"
            )
            return
        self._populate_rounds(
            Tournament._draw(
                players,
                Tour(Tournament._assoc.get(gender), depth).rankings,
                Odds(slam, gender).odds,
            )
        )

    def as_dict(self) -> dict:
        return {idx: r.as_dict() for idx, r in enumerate(self._rounds)}

    @property
    def rounds(self) -> list:
        return self._rounds

    def _populate_rounds(self, players: list):
        self._rounds.insert(0, Round(Tournament._players_to_matches(players)))
        for i in range(1, self._n_rounds):
            winners: list = self._rounds[i - 1].winners
            self._rounds.insert(i, Round(Tournament._players_to_matches(winners)))

    @classmethod
    def _players_to_matches(cls, players: list) -> list:
        return [
            Match(players[i * 2], players[i * 2 + 1])
            for i in range(round(len(players) / 2))
        ]

    @classmethod
    def _draw(cls, players: dict, ranks: dict, odds: dict) -> list:
        result: list = []
        for full_name, details in players.items():
            result.append(
                Player(
                    first_name=details.get("first_name"),
                    last_name=details.get("last_name"),
                    nationality=details.get("nationality"),
                    rank=Tournament._matcher(full_name, ranks),
                    seed=details.get("seed"),
                    entry_type=details.get("entry_type"),
                    odds=Tournament._matcher(full_name, odds),
                )
            )
        return result

    @classmethod
    def _matcher(cls, player: str, values: dict):
        value = values.get(player)
        if value is not None:
            return value
        return process.extractOne(player, [values.values()])
