from abc import ABC, abstractmethod

from snakeshot.utils import session

from requests import Response


class Draw(ABC):
    def __init__(self):
        self._players: dict[str, dict] = self._draw_to_dict()

    @property
    def players(self):
        return self._players

    @abstractmethod
    def _draw_to_dict(self):
        raise NotImplementedError


class Wimbledon(Draw):
    def __init__(self, year: int, gender: str):
        self._year = year
        self._name: str = "Wimbledon"
        self._gender: str = gender
        self._draw_gender: str = {"Mens": "MS", "Womens": "LS"}.get(gender)
        self._base_url: str = (
            f"https://www.wimbledon.com/en_GB/scores/feeds/{year}/draws"
        )
        super().__init__()

    # TODO : trim this down
    def _draw_to_dict(self):
        draw_list: list = self._draws_list()
        draw: dict = self._draw(draw_list)
        matches: list = Wimbledon._matches(draw)
        return Wimbledon._players(matches)

    def _draws_list(self) -> list:
        draw_list: Response = session.get(
            f"https://www.wimbledon.com/en_GB/scores/feeds/"
            f"{self._year}/draws/draws.json",
            f"{self._year} {self._name} draws list",
        )
        return dict(draw_list.json()).get("draws")

    def _draw(self, draw_list: list) -> dict:
        draw_url: str = next(
            t for t in draw_list if t.get("id") == self._draw_gender
        ).get("feed_url")
        draw: Response = session.get(
            draw_url, f"{self._gender} {self._year} {self._name} draw"
        )
        return dict(draw.json())

    @classmethod
    def _matches(cls, draw: dict) -> list:
        return [match for idx, match in enumerate(draw.get("matches")) if idx <= 63]

    @classmethod
    def _players(cls, matches: list) -> dict:
        players = {}
        for match in matches:
            players.update(Wimbledon._team_to_player(match.get("team1")))
            players.update(Wimbledon._team_to_player(match.get("team2")))
        return players

    @classmethod
    def _team_to_player(cls, team: dict) -> dict:
        return {
            f"{team.get('firstNameA')} {team.get('lastNameA')}": {
                "first_name": team.get("firstNameA"),
                "last_name": team.get("lastNameA"),
                "nationality": team.get("nationA"),
                "seed": team.get("seed"),
                "entry_type": team.get("entryStatus"),
            }
        }
