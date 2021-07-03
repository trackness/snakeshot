from decimal import Decimal
from statistics import mean


class Player:
    def __init__(
        self,
        _id: int,
        gender: str,
        first_name: str,
        last_name: str,
        full_name: str,
        nationality: str,
        rank: int,
        seed: int = None,
        entry_type: str = None,
    ):
        self._id = _id
        if gender in {"M", "MS"}:
            self._gender = "M"
        if gender in {"W", "WS", "L", "LS"}:
            self._gender = "W"
        self._first_name: str = first_name
        self._last_name: str = last_name
        self._full_name: str = full_name
        self._nationality: str = nationality
        self._rank: int = rank
        self._seed: int = seed
        self._entry_type: str = entry_type
        self._odds: list[Decimal] = []

    @classmethod
    def qualifier(cls, gender: str):
        return Player(
            _id=0,
            gender=gender,
            first_name="Q",
            last_name="Q",
            full_name="Q Q",
            nationality="-Q-",
            rank=999,
        )

    @property
    def id(self) -> int:
        return self._id

    @property
    def gender(self) -> str:
        return self._gender

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def nationality(self) -> str:
        return self._nationality

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def seed(self):
        return self._seed

    @property
    def entry_type(self):
        return self._entry_type

    @property
    def odds(self) -> Decimal:
        return mean(self._odds) if len(self._odds) != 0 else Decimal(999)

    @odds.setter
    def odds(self, value):
        self._odds.append(Decimal(value))
