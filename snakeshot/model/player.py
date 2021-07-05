from decimal import Decimal


class Player:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        nationality: str,
        rank: int,
        seed: int = None,
        entry_type: str = None,
    ):
        self._first_name: str = first_name
        self._last_name: str = last_name
        self._nationality: str = nationality
        self._rank: int = rank
        self._seed: int = seed
        self._entry_type: str = entry_type
        self._odds: Decimal = Decimal(9999)

    @classmethod
    def qualifier(cls):
        return Player(
            first_name="Q",
            last_name="Q",
            nationality="-Q-",
            rank=9999,
        )

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def full_name(self) -> str:
        return f"{self._first_name} {self._last_name}"

    @property
    def nationality(self) -> str:
        return self._nationality

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def seed(self) -> int:
        return self._seed

    @property
    def entry_type(self) -> str:
        return self._entry_type

    @property
    def odds(self) -> Decimal:
        return self._odds

    @odds.setter
    def odds(self, value: Decimal):
        self._odds: Decimal = value
