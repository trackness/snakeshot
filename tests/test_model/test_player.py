from decimal import Decimal

import pytest as pytest
from pytest import param

from snakeshot.model.player import Player


@pytest.fixture
def basic_player_values() -> dict[str, str]:
    return {"first_name": "Nick", "last_name": "Kyrgios", "nationality": "AUS"}


class TestPlayer:
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
        assert player.as_dict() == {
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

    class TestRank:
        @pytest.fixture(params=[[None, None], [1, 1], [-1, None], ["A", None]])
        def rank(self, request) -> param:
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
        def seed(self, request) -> param:
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
                param([None, None], id="None"),
                param(["LL", "LL"], id="Lucky Loser"),
                param(["Q", "Q"], id="Qualifier"),
                param(["WC", "WC"], id="Wild Card"),
                param(["QQ", None], id="Invalid str"),
                param([1, None], id="Invalid type"),
            ]
        )
        def entry_type(self, request) -> param:
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
                param([None, None], id="None"),
                param([1, Decimal(1)], id="int"),
                param([3.5, Decimal(3.5)], id="float"),
                param([Decimal(4.1), Decimal(4.1)], id="Decimal"),
                param([Decimal(-1), None], id="Invalid value"),
                param(["1", None], id="Invalid type"),
            ]
        )
        def odds(self, request) -> param:
            return request.param

        def test_init(self, basic_player_values, odds):
            player = Player(**basic_player_values, odds=odds[0])
            assert player.odds.__eq__(odds[1])

        def test_setter(self, basic_player_values, odds):
            player = Player(**basic_player_values)
            assert player.odds is None
            player.odds = odds[0]
            assert player.odds == odds[1]

    class TestSummary:
        @pytest.mark.parametrize(
            "seed, entry_type, expected",
            [
                param(None, None, "     Nick Kyrgios", id="unseeded, normal"),
                param(1, None, "( 1) Nick Kyrgios", id="seeded, normal"),
                param(None, "Q", "( Q) Nick Kyrgios", id="unseeded, qualifier"),
            ],
        )
        def test_draw(self, basic_player_values, seed, entry_type, expected):
            player = Player(**basic_player_values, seed=seed, entry_type=entry_type)
            assert player.summary("draw") == expected

        @pytest.mark.parametrize(
            "rank, expected",
            [
                param(None, "      Nick Kyrgios", id="unranked"),
                param(1, "(  1) Nick Kyrgios", id="ranked"),
            ],
        )
        def test_tour(self, basic_player_values, rank, expected):
            player = Player(**basic_player_values, rank=rank)
            assert player.summary("tour") == expected

        @pytest.mark.parametrize(
            "odds, expected",
            [
                param(None, "         Nick Kyrgios", id="without odds "),
                param(Decimal(123.4567), "(123.46) Nick Kyrgios", id="with odds"),
            ],
        )
        def test_odds(self, basic_player_values, odds, expected):
            player = Player(**basic_player_values, odds=odds)
            assert player.summary("odds") == expected

        @pytest.mark.parametrize(
            "details, expected",
            [
                param({}, "     AUS Nick Kyrgios", id="unseeded"),
                param({"seed": 1}, "( 1) AUS Nick Kyrgios", id="seeded"),
                param({"entry_type": "LL"}, "(LL) AUS Nick Kyrgios", id="lucky loser"),
            ],
        )
        def test_table(self, basic_player_values, details, expected):
            under_test = Player(**dict(basic_player_values), **dict(details))
            assert under_test.summary("table") == expected
