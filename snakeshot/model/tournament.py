import math

from snakeshot.model.match import Match
from snakeshot.model.player import Player
from snakeshot.model.round import Round


class Tournament:
    def __init__(self, players: list[Player]):
        self._n_rounds: int = round(math.log2(len(players)))
        self._rounds: list[Round] = []
        self._rounds.insert(0, Round(0, Tournament._players_to_matches(players)))
        for i in range(1, self._n_rounds):
            winners: list[Player] = self._rounds[i - 1].winners
            self._rounds.insert(i, Round(i, Tournament._players_to_matches(winners)))
        if len(self._rounds[-1].winners) != 1:
            raise TournamentWinnerCountException(self._rounds[-1])

    def __dict__(self) -> dict[int, dict]:
        return {idx: r.__dict__() for idx, r in enumerate(self._rounds)}

    @classmethod
    def _players_to_matches(cls, players: list[Player]) -> list[Match]:
        return [
            Match(i, [players[i * 2], players[i * 2 + 1]])
            for i in range(round(len(players) / 2))
        ]

    @property
    def rounds(self) -> list[Round]:
        return self._rounds


class TournamentWinnerCountException(Exception):
    def __init__(self, final_round: Round):
        self._winner_count = len(final_round.winners)
        self._message = f"Expected 1 winner, instead got {self._winner_count}"
        super().__init__(self._message)
