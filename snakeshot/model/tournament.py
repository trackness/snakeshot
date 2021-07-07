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
            raise Exception("more than one winner")

    def __dict__(self) -> dict[int, Round]:
        return {idx: rnd.__dict__ for idx, rnd in enumerate(self._rounds)}

    @classmethod
    def _players_to_matches(cls, players: list[Player]) -> list[Match]:
        # return [Match(list(pair)) for pair in zip(players[0::2], players[1::2])]
        return [
            Match(i, [players[i * 2], players[i * 2 + 1]])
            for i in range(round(len(players) / 2))
        ]

    @property
    def rounds(self) -> list[Round]:
        return self._rounds
