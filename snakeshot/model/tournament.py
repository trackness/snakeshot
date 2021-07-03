from math import sqrt

from snakeshot.model.match import Match
from snakeshot.model.player import Player
from snakeshot.model.round import Round


class Tournament:
    def __init__(self, players: list[Player]):
        self._n_rounds: int = round(sqrt(len(players)/2))
        self._rounds: list[Round] = [Round(Tournament.players_to_matches(players))]

        for i in range(1, self._n_rounds):
            winners: list[Player] = self._rounds[i-1].winners
            self._rounds[i] = Round(Tournament.players_to_matches(winners))

        print(self._rounds[-1].winners[0].full_name)

    @classmethod
    def players_to_matches(cls, players: list[Player]) -> list[Match]:
        return [Match(list(pair)) for pair in zip(players[0::2], players[1::2])]
