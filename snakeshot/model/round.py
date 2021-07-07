from snakeshot.model.match import Match
from snakeshot.model.player import Player


class Round:
    def __init__(self, idx: int, matches: list[Match]):
        self._idx = idx
        self._matches: list[Match] = matches
        self._winners: list[Player] = [match.winner_expected for match in self._matches]

    def __dict__(self):
        return {self._idx: [match.__dict__ for match in self._matches]}

    @property
    def idx(self) -> int:
        return self._idx

    @property
    def winners(self) -> list[Player]:
        return self._winners

    @property
    def matches(self) -> list[Match]:
        return self._matches
