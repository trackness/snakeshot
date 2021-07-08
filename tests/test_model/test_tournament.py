from snakeshot.model.player import Player
from snakeshot.model.tournament import Tournament


class TestTournament:
    def test_winner(self):
        players = [Player("A", "B", "ABC", i + 1) for i in range(8)]
        assert Tournament(players).rounds[-1].winners == [players[0]]

    def test_number_of_rounds(self):
        players = [Player("A", "B", "ABC", i + 1) for i in range(16)]
        assert Tournament(players)._n_rounds == 4
