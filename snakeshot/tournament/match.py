from snakeshot.tournament.player import Player


class Match:

    __slots__ = "_round", "_index", "_players", "_winner_expected", "_winner_actual"

    def __init__(
            self,
            r: int,
            i: int,
            players: list[Player],
            winner_actual: Player = None
    ):
        self._round: int = r
        self._index: int = i
        self._players: list[Player] = players
        self._winner_expected: int = self._set_winner_expected()
        self._winner_actual: Player = winner_actual

    @property
    def r(self):
        return self._round

    @property
    def i(self):
        return self._index

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, value: list[Player]):
        self._players = value

    @property
    def winner_expected(self) -> Player:
        return self._players[self._winner_expected]

    def _set_winner_expected(self):
        if self._players[0].odds == self._players[1].odds:
            return 0 if self._players[0].rank < self._players[1].rank else 1
        else:
            return 0 if self._players[0].odds < self._players[1].odds else 1

    @property
    def winner_actual(self) -> Player:
        return self._winner_actual

    @winner_actual.setter
    def winner_actual(self, value: Player):
        self._winner_actual = value
