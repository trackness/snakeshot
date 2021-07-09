import csv
import operator

from snakeshot.utils import session


class Tour:
    _fieldnames: dict = {
        "rankings_current": ["date", "ranking", "id", "points", "tours"],
        "players": ["id", "first_name", "last_name", "hand", "b_day", "country"],
    }

    def __init__(self, tour: str, depth: int):
        self._depth = depth
        self._tour = tour.lower()
        self._tour_players: dict[str, int] = self._build_tour_players()

    @property
    def players(self):
        return self._tour_players

    def _build_tour_players(self) -> dict[str, int]:
        players = self._players_dict()
        rankings = self._rankings_dict()
        return Tour._sort_dict_by_value(
            {players.get(player_id): ranking for player_id, ranking in rankings.items()}
        )

    def _players_dict(self) -> dict[int, str]:
        return {
            int(player.get("id")): Tour._full_name(player)
            for player in self._target_to_list("players")
        }

    def _rankings_dict(self) -> dict[int, int]:
        return {
            int(ranking.get("id")): int(ranking.get("ranking"))
            for ranking in self._target_to_list("rankings_current")
            if int(ranking.get("ranking")) <= self._depth
        }

    def _target_to_list(self, target) -> list[dict]:
        response = session.get(self._url(target), f"{self._tour} {target}", stream=True)
        return Tour._response_to_dict(target, response)

    @classmethod
    def _response_to_dict(cls, target, content) -> list:
        return list(
            csv.DictReader(
                content.iter_lines(decode_unicode=True),
                delimiter=",",
                fieldnames=Tour._fieldnames.get(target),
            )
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
    def _sort_dict_by_value(cls, d: dict[str, int]) -> dict[str, int]:
        return {k: v for k, v in sorted(d.items(), key=operator.itemgetter(1))}
