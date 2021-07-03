from snakeshot.model.match import Match
from snakeshot.model.player import Player
from snakeshot.model.round import Round
from snakeshot.model.tournament import Tournament

standard_player: dict = {
    "_id": 1,
    "gender": "M",
    "first_name": "A",
    "last_name": "B",
    "full_name": "A B",
    "nationality": "ABC",
}


class TestPlayer:
    def test_odds(self):
        player = Player(**standard_player, rank=1)
        player.odds = 1.5
        player.odds = 3.0
        assert player.odds == 2.25

    def test_qualifier(self):
        player = Player.qualifier("M")
        assert player.first_name == "Q"
        assert player.last_name == "Q"
        assert player.full_name == "Q Q"
        assert player.nationality == "-Q-"
        assert player.rank == 999


class TestMatch:
    def test_winner_odds(self):
        p1 = Player(**standard_player, rank=1)
        p2 = Player(**standard_player, rank=2)
        p1.odds = 2
        p2.odds = 1
        assert Match([p1, p2]).winner_expected == p2

    def test_winner_odds_equal(self):
        p1 = Player(**standard_player, rank=1)
        p2 = Player(**standard_player, rank=2)
        p1.odds = 1
        p2.odds = 1
        assert Match([p1, p2]).winner_expected == p1

    def test_winner_rank(self):
        p1 = Player(**standard_player, rank=1)
        p2 = Player(**standard_player, rank=2)
        assert Match([p1, p2]).winner_expected == p1


class TestRound:
    # TODO : parameterize this
    def test_winners_1(self):
        p1 = Player(**standard_player, rank=1)
        p2 = Player(**standard_player, rank=2)
        p3 = Player(**standard_player, rank=3)
        p4 = Player(**standard_player, rank=4)
        assert Round([Match([p1, p2]), Match([p3, p4])]).winners == [p1, p3]


class TestTournament:
    def test_winner(self):
        players = [Player(**standard_player, rank=i + 1) for i in range(8)]
        assert Tournament(players).rounds[-1].winners == [players[0]]

    def test_number_of_rounds(self):
        players = [Player(**standard_player, rank=i + 1) for i in range(16)]
        assert Tournament(players)._n_rounds == 4
