import pytest as pytest

from snakeshot.model.match import Match
from snakeshot.model.player import Player
from snakeshot.sources.tour import Tour
from snakeshot.model.round import Round
from snakeshot.model.slam import Slam
from snakeshot.model.tournament import Tournament


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


class TestRound:
    def test_winners(self):
        p1 = Player("A", "B", "ABC", 1)
        p2 = Player("A", "B", "ABC", 2)
        p3 = Player("A", "B", "ABC", 3)
        p4 = Player("A", "B", "ABC", 4)
        assert Round([Match([p1, p2]), Match([p3, p4])]).winners == [p1, p3]


class TestTournament:
    def test_winner(self):
        players = [Player("A", "B", "ABC", i + 1) for i in range(8)]
        assert Tournament(players).rounds[-1].winners == [players[0]]

    def test_number_of_rounds(self):
        players = [Player("A", "B", "ABC", i + 1) for i in range(16)]
        assert Tournament(players)._n_rounds == 4


class TestSlam:
    def test_player_pool(self):
        slam: Slam = Slam({"slam": "wimbledon", "tour": "mens"}, 300)
        assert len(slam._player_pools.get("M")) == 300
        assert len(slam._player_pools.get("W")) == 300

    def test_scrape_odds_list(self):
        pass


class TestTour:
    def test_atp(self):
        tour: Tour = Tour("ATP")
        assert len(tour.players) == 1000

    def test_wta(self):
        tour: Tour = Tour("WTA")
        assert len(tour.players) == 1000

    def test_index_by(self):
        inputs = [
            {"player_id": "0", "this": "a", "that": "b"},
            {"player_id": "1", "this": "c", "that": "d"},
            {"player_id": "2", "this": "e", "that": "f"},
        ]
        expected = {
            "0": {"this": "a", "that": "b"},
            "1": {"this": "c", "that": "d"},
            "2": {"this": "e", "that": "f"},
        }
        actual = Tour._index_by("player_id", inputs)
        assert actual == expected

    def test_limit_rankings(self):
        inputs = {
            "0": {"player_id": "1", "that": "a"},
            "1": {"player_id": "2", "that": "b"},
            "2": {"player_id": "3", "that": "c"},
        }
        expected = {0: "1", 1: "2", 2: "3"}
        actual = Tour._limit_rankings(inputs, 3)
        assert actual == expected
