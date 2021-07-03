from decimal import Decimal
from statistics import mean

from snakeshot.data import player


class Player(player.Player):
    def __init__(
            self,
            p: player.Player,
            seed: int = None,
            entry_type: str = None,
            rank: int = None,
    ):
        super().__init__(**p.__dict__)
        self._seed: int = seed
        self._entry_type: str = entry_type
        self._odds: list[Decimal] = []
        self._rank: int = rank

    @property
    def seed(self):
        return self._seed

    @property
    def entry_type(self):
        return self._entry_type

    @property
    def odds(self) -> Decimal:
        return mean(self._odds)

    @odds.setter
    def odds(self, value):
        self._odds.append(Decimal(value))
