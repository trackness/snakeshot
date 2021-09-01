from abc import ABC, abstractmethod
from typing import Generator

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


class Type1(Draw):
    def __init__(self, year: int, gender: str, name: str, domain: str):
        self._year = year
        self._name: str = name
        self._gender: str = gender
        self._domain_lang: str = domain
        super().__init__()

    # TODO : trim this down
    def _draw_to_dict(self):
        draw_list: list = self._draws_list()
        draw: dict = self._draw(draw_list)
        matches: Generator = Type1._matches(draw)
        return Type1._players(matches)

    def _draws_list(self) -> list:
        draw_list: Response = session.get(
            f"https://{self._domain_lang}/scores/feeds/"
            f"{self._year}/draws/draws.json",
            f"{self._year} {self._name} draws list",
            add={"Host": self._domain_lang.split("/")[0]},
        )
        return dict(draw_list.json()).get("draws")

    def _draw(self, draw_list: list) -> dict:
        draw_url: str = next(t for t in draw_list if t.get("id") == self._gender).get(
            "feed_url"
        )
        draw: Response = session.get(
            draw_url, f"{self._gender} {self._year} {self._name} draw"
        )
        return dict(draw.json())

    @classmethod
    def _matches(cls, draw: dict) -> Generator:
        return (match for idx, match in enumerate(draw.get("matches")) if idx <= 63)

    @classmethod
    def _players(cls, matches: Generator) -> dict:
        players = {}
        for match in matches:
            players.update(Type1._team_to_player(match.get("team1")))
            players.update(Type1._team_to_player(match.get("team2")))
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


class Wimbledon(Type1):
    def __init__(self, year: int, gender: str):
        gender = {"Mens": "MS", "Womens": "LS"}.get(gender)
        domain = "www.wimbledon.com/en_GB"
        super().__init__(year, gender, "Wimbledon", domain)


class USOpen(Type1):
    # https://www.usopen.org/en_US/scores/feeds/2021/draws/draws.json
    def __init__(self, year: int, gender: str):
        gender = {"Mens": "MS", "Womens": "WS"}.get(gender)
        domain = "www.usopen.org/en_US"
        super().__init__(year, gender, "US Open", domain)
