import pytest as pytest

from snakeshot.model.match import Match
from snakeshot.model.player import Player
from snakeshot.model.round import Round


class TestRound:
    # TODO : refactor this down to minimum
    @pytest.fixture
    def players(self) -> list:
        return [
            Player("A", "B", "ABC", 1),
            Player("A", "B", "ABC", 2),
            Player("A", "B", "ABC", 3),
            Player("A", "B", "ABC", 4),
        ]

    def test_winners(self, players):
        m1: Match = Match(players[0], players[1])
        m2: Match = Match(players[2], players[3])
        assert Round([m1, m2]).winners == [players[0], players[2]]

    def test_dict(self, players):
        m1: Match = Match(players[0], players[1])
        m2: Match = Match(players[2], players[3])
        assert Round([m1, m2]).as_dict() == {
            0: m1.as_dict(),
            1: m2.as_dict(),
        }

    def test_matches(self, players):
        m1: Match = Match(players[0], players[1])
        m2: Match = Match(players[2], players[3])
        assert Round([m1, m2]).matches == [m1, m2]
