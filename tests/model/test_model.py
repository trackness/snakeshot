import pytest as pytest

from snakeshot.model.match import Match
from snakeshot.model.player import Player
from snakeshot.model.Tour import Tour
from snakeshot.model.round import Round
from snakeshot.model.slam import Slam
from snakeshot.model.tournament import Tournament


class TestPlayer:
    def test_odds(self):
        player = Player(1, "M", "A", "B", "A B", "ABC", 1)
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
    @pytest.fixture
    def p1(self):
        return Player(1, "M", "A", "B", "A B", "ABC", 1)

    @pytest.fixture
    def p2(self):
        return Player(1, "M", "A", "B", "A B", "ABC", 2)

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


class TestRound:
    def test_winners(self):
        p1 = Player(1, "M", "A", "B", "A B", "ABC", 1)
        p2 = Player(2, "M", "A", "B", "A B", "ABC", 2)
        p3 = Player(3, "M", "A", "B", "A B", "ABC", 3)
        p4 = Player(4, "M", "A", "B", "A B", "ABC", 4)
        assert Round([Match([p1, p2]), Match([p3, p4])]).winners == [p1, p3]


class TestTournament:
    def test_winner(self):
        players = [Player(i + 1, "M", "A", "B", "A B", "ABC", i + 1) for i in range(8)]
        assert Tournament(players).rounds[-1].winners == [players[0]]

    def test_number_of_rounds(self):
        players = [Player(i + 1, "M", "A", "B", "A B", "ABC", i + 1) for i in range(16)]
        assert Tournament(players)._n_rounds == 4


@pytest.mark.skip
class TestSlam:
    def test_mens_200(self):
        assert len(Slam._mens_200()) == 1

    def test_womens_200(self):
        assert len(Slam._womens_200()) == 200

    def test_scrape_odds_list(self):
        pass


class TestRankedPlayers:
    def test_atp(self):
        atp: Tour = Tour("ATP")
        # assert len(atp.players) == 100
        [print(f"{player.rank} {player.full_name}") for player in atp.players]
