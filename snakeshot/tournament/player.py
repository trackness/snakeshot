from decimal import Decimal
from statistics import mean


class Player:

    __slots__ = "_name_abbreviated", "_name_full", "_nationality", "_seed", "_entry_type", "_odds"

    def __init__(
            self,
            name_abbreviated: str = None,
            name_full: str = None,
            nationality: str = None,
            seed: int = None,
            entry_type: str = None,
    ):
        self._name_abbreviated: str = name_abbreviated
        self._name_full: str = name_full
        self._nationality: str = nationality
        self._seed: int = seed
        self._entry_type: str = entry_type
        self._odds: list[Decimal] = []

    @classmethod
    def qualifier(cls):
        return Player(name_abbreviated="Q", name_full="Q", nationality="-Q-")

    @property
    def name_abbreviated(self):
        return self._name_abbreviated

    @property
    def name_full(self):
        return self._name_full

    @property
    def nationality(self):
        return self._nationality

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
