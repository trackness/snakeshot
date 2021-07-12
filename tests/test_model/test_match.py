from decimal import Decimal

import pytest as pytest
from pytest import param

from snakeshot.model.match import Match
from snakeshot.model.player import Player


class TestMatch:
    @pytest.fixture
    def patch_loc(self):
        return "snakeshot.model.match"

    @pytest.mark.parametrize(
        "p1_stats, p2_stats, expected",
        [
            param([1, None], [2, None], 0, id="rank only"),
            param([1, 2], [2, 1], 1, id="odds"),
            param([1, 2], [2, 2], 0, id="equal odds"),
            param([1, 1], [1, 1], 0, id="equal odds and rank"),
        ],
    )
    def test_winner_expected(self, p1_stats, p2_stats, expected):
        p1 = Player("Nick", "Kyrgios", "AUS", rank=p1_stats[0], odds=p1_stats[1])
        p2 = Player("Dennis", "Shapovalov", "CAN", rank=p2_stats[0], odds=p2_stats[1])
        under_test: Match = Match(p1, p2)
        assert under_test.winner_expected == under_test.players[expected]

    def test_dict(self, mocker, patch_loc):
        p1 = {
            "Nick Kyrgios": {
                "entry_type": None,
                "first_name": "Nick",
                "last_name": "Kyrgios",
                "nationality": "AUS",
                "odds": 2.0,
                "rank": 1,
                "seed": None,
            }
        }
        p2 = {
            "Dennis Shapovalov": {
                "entry_type": None,
                "first_name": "Dennis",
                "last_name": "Shapovalov",
                "nationality": "CAN",
                "odds": 1.0,
                "rank": 2,
                "seed": None,
            }
        }
        mocker.patch(f"{patch_loc}.Player.as_dict", side_effect=[p1, p2])
        under_test: Match = Match(
            Player("Nick", "Kyrgios", "AUS", rank=1, odds=Decimal(2)),
            Player("Dennis", "Shapovalov", "CAN", rank=2, odds=Decimal(1)),
        )
        assert under_test.as_dict() == {"players": {0: p1, 1: p2}, "winner": p2}
