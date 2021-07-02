from snakeshot.model.match import Match
from snakeshot.model.player import Player


class Round:
    def __init__(self, i: int = None, matches: list[Match] = None):
        self._i = i,
        self._matches: list[Match] = matches

    @property
    def i(self):
        return self._i

    @property
    def matches(self):
        return self._matches

    @matches.setter
    def matches(self, value: list[Match]):
        self._matches = value

    def winners(self) -> list[Player]:
        return [match.winner_expected for match in self.matches]
