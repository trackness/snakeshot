from decimal import Decimal

import pytest as pytest

from snakeshot.model.player import Player


class TestPlayer:
    @pytest.fixture
    def basic_player_values(self) -> dict[str, str]:
        return {"first_name": "Nick", "last_name": "Kyrgios", "nationality": "AUS"}

    @pytest.fixture(params=["Alex", "Felix"])
    def first_name(self, request) -> str:
        return request.param

    @pytest.fixture(params=["De Minaur", "Auger-Aliassime"])
    def last_name(self, request) -> str:
        return request.param

    @pytest.fixture(params=["AUS", "CAN", "GBR"])
    def nationality(self, request) -> str:
        return request.param

    def test_init(self, first_name, last_name, nationality):
        player = Player(first_name, last_name, nationality)
        assert player.first_name == first_name
        assert player.last_name == last_name
        assert player.full_name == f"{first_name} {last_name}"
        assert player.nationality == nationality
        assert player.rank is None
        assert player.seed is None
        assert player.entry_type is None
        assert player.odds is None

    def test_dict(self, basic_player_values):
        player = Player(**basic_player_values, rank=5, seed=3, odds=Decimal(3.5))
        assert player.__dict__() == {
            "Nick Kyrgios": {
                "first_name": "Nick",
                "last_name": "Kyrgios",
                "nationality": "AUS",
                "rank": 5,
                "seed": 3,
                "entry_type": None,
                "odds": Decimal(3.5),
            }
        }

    class TestRank:
        @pytest.fixture(params=[[None, None], [1, 1], [-1, None], ["A", None]])
        def rank(self, request) -> pytest.param:
            return request.param

        def test_init(self, basic_player_values, rank):
            player = Player(**basic_player_values, rank=rank[0])
            assert player.rank is rank[1]

        def test_setter(self, basic_player_values, rank):
            player = Player(**basic_player_values)
            assert player.rank is None
            player.rank = rank[0]
            assert player.rank == rank[1]

    class TestSeed:
        @pytest.fixture(
            params=[[None, None], [1, 1], [-1, None], [33, None], ["A", None]]
        )
        def seed(self, request) -> pytest.param:
            return request.param

        def test_init(self, basic_player_values, seed):
            player = Player(**basic_player_values, seed=seed[0])
            assert player.seed is seed[1]

        def test_setter(self, basic_player_values, seed):
            player = Player(**basic_player_values)
            assert player.seed is None
            player.seed = seed[0]
            assert player.seed == seed[1]

    class TestEntryType:
        @pytest.fixture(
            params=[
                pytest.param([None, None], id="None"),
                pytest.param(["LL", "LL"], id="Lucky Loser"),
                pytest.param(["Q", "Q"], id="Qualifier"),
                pytest.param(["WC", "WC"], id="Wild Card"),
                pytest.param(["QQ", None], id="Invalid str"),
                pytest.param([1, None], id="Invalid type"),
            ]
        )
        def entry_type(self, request) -> pytest.param:
            return request.param

        def test_init(self, basic_player_values, entry_type):
            player = Player(**basic_player_values, entry_type=entry_type[0])
            assert player.entry_type is entry_type[1]

        def test_setter(self, basic_player_values, entry_type):
            player = Player(**basic_player_values)
            assert player.entry_type is None
            player.entry_type = entry_type[0]
            assert player.entry_type == entry_type[1]

    class TestOdds:
        @pytest.fixture(
            params=[
                pytest.param([None, None], id="None"),
                pytest.param([1, Decimal(1)], id="int"),
                pytest.param([3.5, Decimal(3.5)], id="float"),
                pytest.param([Decimal(4.1), Decimal(4.1)], id="Decimal"),
                pytest.param([Decimal(-1), None], id="Invalid value"),
                pytest.param(["1", None], id="Invalid type"),
            ]
        )
        def odds(self, request) -> pytest.param:
            return request.param

        def test_init(self, basic_player_values, odds):
            player = Player(**basic_player_values, odds=odds[0])
            assert player.odds.__eq__(odds[1])

        def test_setter(self, basic_player_values, odds):
            player = Player(**basic_player_values)
            assert player.odds is None
            player.odds = odds[0]
            assert player.odds == odds[1]

    def test_qualifier(self):
        player = Player.qualifier()
        assert player.first_name == "Q"
        assert player.last_name == "Q"
        assert player.full_name == "Q Q"
        assert player.nationality == "-Q-"
        assert player.rank == 9999
        assert player.seed is None
        assert player.entry_type is None
        assert player.odds is None
