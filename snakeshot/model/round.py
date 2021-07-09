from snakeshot.model.match import Match
from snakeshot.model.player import Player


class Round:
    def __init__(self, matches: list[Match]):
        self._matches: list[Match] = matches
        self._winners: list[Player] = [match.winner_expected for match in self._matches]

    def as_dict(self) -> dict[int, dict]:
        return {idx: m.as_dict() for idx, m in enumerate(self._matches)}

    @property
    def winners(self) -> list:
        return self._winners

    @property
    def matches(self) -> list:
        return self._matches
