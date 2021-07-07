import csv
from loguru import logger

import requests as requests

from snakeshot.model.player import Player


class Tour:
    _RANKINGS = "rankings_current"
    _PLAYERS = "players"
    _RID = "ranking"
    _PID = "player_id"
    _fieldnames: dict = {
        _RANKINGS: ["ranking_date", _RID, _PID, "ranking_points", "tours"],
        _PLAYERS: [
            _PID,
            "first_name",
            "last_name",
            "hand",
            "birth_date",
            "country_code",
        ],
    }

    def __init__(self, tour: str, depth: int):
        self._depth = depth
        if tour.lower() == "mens":
            self._tour = "atp"
        if tour.lower() == "womens":
            self._tour = "wta"
        self._players: list[Player] = self._build_players()

    @property
    def players(self):
        return self._players

    def _build_players(self) -> list[Player]:
        rankings: dict = self._url_to_dict(Tour._RANKINGS, Tour._RID)
        players: dict = self._url_to_dict(Tour._PLAYERS, Tour._PID)
        return [
            Player(
                first_name=players.get(player).get("first_name"),
                last_name=players.get(player).get("last_name"),
                nationality=players.get(player).get("country_code"),
                rank=rank,
            )
            for rank, player in self._limit_rankings(rankings).items()
        ]

    def _limit_rankings(self, rankings: dict) -> dict[int, str]:
        return {
            int(k): v.get(Tour._PID)
            for k, v in rankings.items()
            if int(k) <= self._depth
        }

    def _url_to_dict(self, target: str, key: str) -> dict[str, dict]:
        logger.info(f"Loading {self._tour.upper()} {target}")
        url = f"https://raw.githubusercontent.com/JeffSackmann/tennis_{self._tour}/master/{self._tour}_{target}.csv"
        results = list(
            csv.DictReader(
                requests.get(url, stream=True).iter_lines(decode_unicode=True),
                delimiter=",",
                fieldnames=Tour._fieldnames.get(target),
            )
        )
        return Tour._index_by(key, results)

    @classmethod
    def _index_by(cls, key: str, l_d: list[dict]) -> dict[str, dict]:
        return {e.get(key): {k: v for k, v in e.items() if k != key} for e in l_d}
