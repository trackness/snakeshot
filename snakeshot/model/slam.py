import itertools
from abc import ABC

import cloudscraper as cloudscraper
import requests as requests
from bs4 import BeautifulSoup
from snakeshot.model.player import Player


class Slam(ABC):
    def __init__(self):
        self._player_pools: dict[str, list[Player]] = {
            "M": Slam._mens_200(),
            "W": Slam._womens_200(),
        }
        Slam._set_odds(Slam._scrape_odds_list(), self._player_pools)

    @classmethod
    def _mens_200(cls) -> list[Player]:
        query = "https://www.atptour.com/en/rankings/singles?&rankRange=1-200"
        response = cloudscraper.create_scraper().get(query)
        table = BeautifulSoup(response.text, "html.parser").find(
            "table", {"class": "mega-table"}
        )
        return [Slam._atp_to_player(player) for player in table.findAll("tr")]

    @classmethod
    def _atp_to_player(cls, player) -> Player:
        return Player(
            _id=player.find,
            gender="W",
            first_name=player.get("player").get("firstName"),
            last_name=player.get("player").get("lastName"),
            full_name=player.get("player").get("fullName"),
            nationality=player.get("player").get("countryCode"),
            rank=player.get("ranking"),
        )

    @classmethod
    def _womens_200(cls) -> list[Player]:
        pages = [
            f"https://api.wtatennis.com/tennis/players/ranked?page={i}&pageSize=100&type=rankSingles&metric=SINGLES"
            for i in range(2)
        ]
        results = [requests.get(page).json() for page in pages]
        return [
            Slam._wta_to_player(player) for player in list(itertools.chain(*results))
        ]

    @classmethod
    def _wta_to_player(cls, player: dict) -> Player:
        return Player(
            _id=player.get("player").get("id"),
            gender="W",
            first_name=player.get("player").get("firstName"),
            last_name=player.get("player").get("lastName"),
            full_name=player.get("player").get("fullName"),
            nationality=player.get("player").get("countryCode"),
            rank=player.get("ranking"),
        )

    @classmethod
    def _scrape_odds_list(cls):
        pass

    @classmethod
    def _set_odds(cls, odds, players):
        pass
