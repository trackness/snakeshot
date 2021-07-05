from abc import ABC

from snakeshot.model.player import Player


class Slam(ABC):
    def __init__(self):
        self._player_pools: dict[str, list[Player]] = {
            # "M": Slam._mens_200(),
            # "W": Slam._womens_200(),
        }
        Slam._set_odds(Slam._scrape_odds_list(), self._player_pools)

    # @classmethod
    # def _mens_200(cls) -> list[Player]:
    #     players = Slam._player_rankings(
    #         Slam._url_to_dict(Slam._atp_players, Slam._player_fieldnames),
    #         Slam._url_to_dict(Slam._atp_rankings, Slam._ranking_fieldnames),
    #     )
    #     # return [Slam._atp_to_player(player) for player in a]
    #     return ["a"]
    #
    # @classmethod
    # def _atp_to_player(cls, player: dict) -> Player:
    #     return Player(
    #         _id=player.find("td", {"class": "rank-cell"}).text,
    #         gender="M",
    #         first_name="",
    #         last_name="",
    #         full_name=player.find("span", {"class": "player-cell-wrapper"})
    #         .find("a")
    #         .text,
    #         nationality=player.find("div", {"class": "country-item"})
    #         .find("img")
    #         .get("alt"),
    #         rank=player.get("ranking"),
    #     )
    #
    # @classmethod
    # def _womens_200(cls) -> list[Player]:
    #     pages = [
    #         f"https://api.wtatennis.com/tennis/players/ranked?page={i}&pageSize=100&type=rankSingles&metric=SINGLES"
    #         for i in range(2)
    #     ]
    #     results = [requests.get(page).json() for page in pages]
    #     return [
    #         Slam._wta_to_player(player) for player in list(itertools.chain(*results))
    #     ]
    #
    # @classmethod
    # def _wta_to_player(cls, player: dict) -> Player:
    #     return Player(
    #         _id=player.get("player").get("id"),
    #         gender="W",
    #         first_name=player.get("player").get("firstName"),
    #         last_name=player.get("player").get("lastName"),
    #         full_name=player.get("player").get("fullName"),
    #         nationality=player.get("player").get("countryCode"),
    #         rank=player.get("ranking"),
    #     )

    @classmethod
    def _scrape_odds_list(cls):
        pass

    @classmethod
    def _set_odds(cls, odds, players):
        pass
