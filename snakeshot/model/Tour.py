import csv
from csv import DictReader

import requests as requests

from snakeshot.model.player import Player


class Tour:
    _RANKINGS = "rankings_current"
    _PLAYERS = "players"
    _fieldnames: dict = {
        _RANKINGS: ["ranking_date", "ranking", "player_id", "ranking_points", "tours"],
        _PLAYERS: [
            "player_id",
            "first_name",
            "last_name",
            "hand",
            "birth_date",
            "country_code",
        ],
    }

    def __init__(self, tour: str):
        if tour.lower() in {"atp", "wta"}:
            self._players: list[Player] = Tour._build_players(tour.lower())
        else:
            raise Exception("fuck")

    @property
    def players(self):
        return self._players

    @classmethod
    def _build_players(cls, tour: str) -> list[Player]:
        count: int = 10
        rankings = {
            ranking.get("player_id"): int(ranking.get("ranking"))
            for ranking in Tour._url_to_dict(tour, Tour._RANKINGS)
            if int(ranking.get("ranking")) <= count
        }
        # [print(f"{v} - {k}") for k, v in rankings.items()]
        players = []
        for player in Tour._url_to_dict(tour, Tour._PLAYERS):
            ranking = rankings.get(player.get("player_id", None))
            if ranking is not None and ranking <= count:
                print(ranking)
                player.update(ranking=ranking)
                players.append(player)
        print(f"players size: {len(players)}")
        return [
            Player(
                first_name=player.get("first_name"),
                last_name=player.get("last_name"),
                nationality=player.get("country_code"),
                rank=player.get("ranking", -1),
            )
            for player in players
        ]

    @classmethod
    def _url_to_dict(cls, tour: str, target: str) -> DictReader:
        return csv.DictReader(
            requests.get(
                f"https://raw.githubusercontent.com/JeffSackmann/tennis_{tour}/master/{tour}_{target}.csv",
                stream=True,
            ).iter_lines(decode_unicode=True),
            delimiter=",",
            fieldnames=Tour._fieldnames.get(target),
        )
