from decimal import Decimal

from snakeshot.model.player import Player


# TODO : Change to two players instead of list, just for init
class Match:
    def __init__(self, p1: Player, p2: Player):
        self._players: list = [p1, p2]
        self._winner_expected: int = self._set_winner_expected()

    def as_dict(self) -> dict:
        return {
            "players": {idx: p.as_dict() for idx, p in enumerate(self._players)},
            "winner": self.winner_expected.as_dict(),
        }

    @property
    def players(self) -> list:
        return self._players

    @property
    def winner_expected(self) -> Player:
        return self._players[self._winner_expected]

    def _set_winner_expected(self) -> int:
        odds = [Decimal(Match._max_if_missing(player.odds)) for player in self._players]
        if odds[0] != odds[1]:
            return Match._index_of_min(odds)
        rank = [Match._max_if_missing(player.rank) for player in self._players]
        if rank[0] != rank[1]:
            return Match._index_of_min(rank)
        names = [player.last_name for player in self._players]
        return Match._index_of_min(names)

    @classmethod
    def _max_if_missing(cls, value):
        return 9999 if value is None else value

    @classmethod
    def _index_of_min(cls, values: list) -> int:
        return values.index(min(values))
