from decimal import Decimal


class Player:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        nationality: str,
        rank: int = None,
        seed: int = None,
        entry_type: str = None,
        odds: Decimal = None,
    ):
        self._first_name: str = first_name
        self._last_name: str = last_name
        self._nationality: str = nationality
        self._rank: int = Player._validate_rank(rank)
        self._seed: int = Player._validate_seed(seed)
        self._entry_type: str = Player._validate_entry_type(entry_type)
        self._odds: Decimal = Player._validate_odds(odds)

    def __dict__(self) -> dict:
        return {
            self.full_name: {
                "first_name": self._first_name,
                "last_name": self._last_name,
                "nationality": self._nationality,
                "rank": self._rank,
                "seed": self._seed,
                "entry_type": self._entry_type,
                "odds": self._odds,
            }
        }

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

    @rank.setter
    def rank(self, value: int):
        self._rank = Player._validate_rank(value)

    @classmethod
    def _validate_rank(cls, value) -> int:
        return value if isinstance(value, int) and value >= 1 else None

    @property
    def seed(self) -> int:
        return self._seed

    @seed.setter
    def seed(self, value: int):
        self._seed = Player._validate_seed(value)

    @classmethod
    def _validate_seed(cls, value) -> int:
        return value if isinstance(value, int) and 1 <= value <= 32 else None

    @property
    def entry_type(self) -> str:
        return self._entry_type

    @entry_type.setter
    def entry_type(self, value: str):
        self._entry_type = Player._validate_entry_type(value)

    @classmethod
    def _validate_entry_type(cls, value) -> str:
        return value if isinstance(value, str) and value in ["LL", "Q", "WC"] else None

    @property
    def odds(self) -> Decimal:
        return self._odds

    @odds.setter
    def odds(self, value):
        self._odds: Decimal = Player._validate_odds(value)

    @classmethod
    def _validate_odds(cls, value):
        if isinstance(value, Decimal):
            return value if value > 0 else None
        elif isinstance(value, float):
            return Decimal.from_float(value) if value > 0 else None
        elif isinstance(value, int):
            return Decimal(value) if value > 0 else None
        else:
            return None

    def summary(self, t: str) -> str:
        return {
            "draw": self._summary_draw,
            "tour": self._summary_tour,
            "odds": self._summary_odds,
        }.get(t)()

    def _summary_draw(self) -> str:
        if self._seed is not None:
            prefix = f"({self._seed:2})"
        elif self._entry_type is not None:
            prefix = f"({self._entry_type:>2})"
        else:
            prefix = "    "
        return f"{prefix} {self.full_name}"

    def _summary_tour(self) -> str:
        prefix = f"({self._rank:3})" if self._rank is not None else "     "
        return f"{prefix} {self.full_name}"

    def _summary_odds(self) -> str:
        prefix = f"({self._odds:6.2f})" if self._odds is not None else "        "
        return f"{prefix} {self.full_name}"
