import pytest as pytest

from snakeshot.model.match import Match
from snakeshot.model.player import Player


class TestMatch:
    @pytest.fixture
    def p1(self):
        return Player("A", "B", "ABC", 1)

    @pytest.fixture
    def p2(self):
        return Player("A", "B", "ABC", 2)

    def test_winner_odds(self, p1, p2):
        p1.odds = 2
        p2.odds = 1
        assert Match([p1, p2]).winner_expected == p2

    def test_winner_odds_equal(self, p1, p2):
        p1.odds = 1
        p2.odds = 1
        assert Match([p1, p2]).winner_expected == p1

    def test_winner_rank(self, p1, p2):
        assert Match([p1, p2]).winner_expected == p1
