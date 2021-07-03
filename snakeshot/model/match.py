from snakeshot.model.player import Player


# TODO : Change to two players instead of list, just for init
class Match:
    def __init__(self, players: list[Player], winner_actual: Player = None):
        self._players: list[Player] = players
        self._winner_expected: int = self._set_winner_expected()
        self._winner_actual: Player = winner_actual

    @property
    def winner_expected(self) -> Player:
        return self._players[self._winner_expected]

    def _set_winner_expected(self) -> int:
        if self._players[0].odds == self._players[1].odds:
            return 0 if self._players[0].rank < self._players[1].rank else 1
        else:
            return 0 if self._players[0].odds < self._players[1].odds else 1
