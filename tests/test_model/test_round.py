from snakeshot.model.match import Match
from snakeshot.model.player import Player
from snakeshot.model.round import Round


class TestRound:
    def test_winners(self):
        p1 = Player("A", "B", "ABC", 1)
        p2 = Player("A", "B", "ABC", 2)
        p3 = Player("A", "B", "ABC", 3)
        p4 = Player("A", "B", "ABC", 4)
        assert Round([Match(p1, p2), Match(p3, p4)]).winners == [p1, p3]
