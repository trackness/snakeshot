class Round:
    def __init__(self, matches: list):
        self._matches: list = matches
        self._winners: list = [match.winner_expected for match in self._matches]

    def as_dict(self) -> dict:
        return {idx: m.as_dict() for idx, m in enumerate(self._matches)}

    @property
    def winners(self) -> list:
        return self._winners

    @property
    def matches(self) -> list:
        return self._matches
