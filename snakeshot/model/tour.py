import csv

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

    def __init__(self, tour: str, n_players: int = 1000):
        if tour.lower() in {"atp", "wta"}:
            self._players: list[Player] = Tour._build_players(tour.lower(), n_players)
        else:
            # TODO : custom logging / exceptions
            raise Exception("fuck")

    @property
    def players(self):
        return self._players

    @classmethod
    def _build_players(cls, tour: str, n_players) -> list[Player]:
        rankings: dict = Tour._url_to_dict(tour, Tour._RANKINGS, Tour._RID)
        players: dict = Tour._url_to_dict(tour, Tour._PLAYERS, Tour._PID)
        return [
            Player(
                first_name=players.get(player).get("first_name"),
                last_name=players.get(player).get("last_name"),
                nationality=players.get(player).get("country_code"),
                rank=rank,
            )
            for rank, player in Tour._limit_rankings(rankings, n_players).items()
        ]

    @classmethod
    def _limit_rankings(cls, rankings: dict, count: int) -> dict[int, str]:
        return {
            int(k): v.get(Tour._PID) for k, v in rankings.items() if int(k) <= count
        }

    @classmethod
    def _url_to_dict(cls, tour: str, target: str, key: str) -> dict[str, dict]:
        url = f"https://raw.githubusercontent.com/JeffSackmann/tennis_{tour}/master/{tour}_{target}.csv"
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
