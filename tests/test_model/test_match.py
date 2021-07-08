from decimal import Decimal

import pytest as pytest
from pytest import param

from snakeshot.model.match import Match
from snakeshot.model.player import Player


class TestMatch:
    @pytest.mark.parametrize(
        "p1_stats, p2_stats, expected",
        [
            param([1, None], [2, None], 0, id="rank only"),
            param([1, 2], [2, 1], 1, id="odds"),
            param([1, 2], [2, 2], 0, id="equal odds"),
        ],
    )
    def test_winner_expected(self, p1_stats, p2_stats, expected):
        p1 = Player("Nick", "Kyrgios", "AUS", rank=p1_stats[0], odds=p1_stats[1])
        p2 = Player("Dennis", "Shapovalov", "CAN", rank=p2_stats[0], odds=p2_stats[1])
        match: Match = Match(p1, p2)
        assert match.winner_expected == match.players[expected]

    def test_dict(self):
        p1 = Player("Nick", "Kyrgios", "AUS", rank=1, odds=Decimal(2))
        p2 = Player("Dennis", "Shapovalov", "CAN", rank=2, odds=Decimal(1))
        match: Match = Match(p1, p2)
        assert match.__dict__() == {
            "players": {0: p1.__dict__(), 1: p2.__dict__()},
            "winner": p2.__dict__(),
        }
