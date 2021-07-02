class Player:

    def __init__(
            self,
            _id: int = None,
            gender: str = None,
            first_name: str = None,
            last_name: str = None,
            full_name: str = None,
            nationality: str = None,
            rank: int = None
    ):
        self._id = _id
        if gender in {"M", "H"}:
            self._gender = "M"
        if gender in {"W", "D"}:
            self._gender = "W"
        self._first_name: str = first_name
        self._last_name: str = last_name
        self._full_name: str = full_name
        self._nationality: str = nationality
        self._rank = rank

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

    @classmethod
    def qualifier(cls):
        return Player(first_name="Q", last_name="Q", full_name="Q Q", nationality="-Q-", rank=999)
