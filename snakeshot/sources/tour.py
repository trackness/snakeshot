import csv
import operator
from concurrent.futures import ThreadPoolExecutor
from typing import Generator

from snakeshot.utils import session


class Tour:
    _fieldnames: dict = {
        "rankings_current": ["date", "ranking", "id", "points", "tours"],
        "players": ["id", "first_name", "last_name", "hand", "b_day", "country"],
    }

    def __init__(self, tour: str, depth: int):
        self._depth = depth
        self._tour = tour.lower()
        self._tour_players: dict = self._build_tour_players()

    @property
    def rankings(self):
        return self._tour_players

    def _build_tour_players(self) -> dict:
        with ThreadPoolExecutor(max_workers=2) as pool:
            players = pool.submit(self._players_dict)
            rankings = pool.submit(self._rankings_dict)
        players = dict(players.result())
        rankings = rankings.result()
        return Tour._sort_dict_by_value(
            {players.get(player_id): ranking for player_id, ranking in rankings}
        )

    def _players_dict(self) -> Generator:
        for player in self._target_to_list("players"):
            yield int(player.get("id")), Tour._full_name(player)

    def _rankings_dict(self) -> Generator:
        for ranking in self._target_to_list("rankings_current"):
            if int(ranking.get("ranking")) <= self._depth:
                yield int(ranking.get("id")), int(ranking.get("ranking"))

    def _target_to_list(self, target) -> Generator:
        response = session.get(self._url(target), f"{self._tour} {target}", stream=True)
        return Tour._response_to_rows(target, response)

    @classmethod
    def _response_to_rows(cls, target, content) -> Generator:
        yield from csv.DictReader(
            content.iter_lines(decode_unicode=True),
            delimiter=",",
            fieldnames=Tour._fieldnames.get(target),
        )

    def _url(self, target: str):
        return (
            f"https://raw.githubusercontent.com/JeffSackmann/tennis_"
            f"{self._tour}/master/{self._tour}_{target}.csv"
        )

    @classmethod
    def _full_name(cls, player: dict) -> str:
        return f"{player.get('first_name')} {player.get('last_name')}"

    @classmethod
    def _sort_dict_by_value(cls, d: dict) -> dict:
        return {k: v for k, v in sorted(d.items(), key=operator.itemgetter(1))}
