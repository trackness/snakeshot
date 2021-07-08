import math

from snakeshot.model.match import Match
from snakeshot.model.player import Player
from snakeshot.model.round import Round


class Tournament:
    def __init__(self, players: list[Player]):
        self._rounds: list[Round] = []
        try:
            self._n_rounds: int = round(math.log2(len(players)))
            self._rounds.insert(0, Round(Tournament._players_to_matches(players)))
            for i in range(1, self._n_rounds):
                winners: list[Player] = self._rounds[i - 1].winners
                self._rounds.insert(i, Round(Tournament._players_to_matches(winners)))
        except Exception:
            raise PlayerCountNotValid(len(players))

    def __dict__(self) -> dict[int, dict]:
        return {idx: r.__dict__() for idx, r in enumerate(self._rounds)}

    @classmethod
    def _players_to_matches(cls, players: list[Player]) -> list[Match]:
        return [
            Match(players[i * 2], players[i * 2 + 1])
            for i in range(round(len(players) / 2))
        ]

    @property
    def rounds(self) -> list[Round]:
        return self._rounds


class PlayerCountNotValid(Exception):
    def __init__(self, player_count: int):
        self._message = f"Player count not a power of 2: {player_count}"
        super().__init__(self._message)
