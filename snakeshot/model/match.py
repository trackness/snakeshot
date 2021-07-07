from typing import Union

from snakeshot.model.player import Player


# TODO : Change to two players instead of list, just for init
class Match:
    def __init__(self, idx: int, players: list[Player]):
        self._idx = idx
        self._players: list[Player] = players
        self._winner_expected: int = self._set_winner_expected()

    def __dict__(self) -> dict[str, Union[dict[int, dict], dict]]:
        return {
            "players": {idx: p.__dict__() for idx, p in enumerate(self._players)},
            "winner": self.winner_expected.__dict__(),
        }

    @property
    def idx(self) -> int:
        return self._idx

    @property
    def players(self) -> list[Player]:
        return self._players

    @property
    def winner_expected(self) -> Player:
        return self._players[self._winner_expected]

    def _set_winner_expected(self) -> int:
        if self._players[0].odds == self._players[1].odds:
            return 0 if self._players[0].rank < self._players[1].rank else 1
        else:
            return 0 if self._players[0].odds < self._players[1].odds else 1
