import pytest as pytest

from snakeshot.model.match import Match
from snakeshot.model.player import Player
from snakeshot.model.round import Round
from snakeshot.model.tournament import Tournament, PlayerCountNotValid


class TestTournament:
    def test_rounds(self):
        players = [Player("Nick", "Kyrgios", "AUS", rank=i + 1) for i in range(8)]
        assert len(Tournament(players).rounds) == 3

    def test_incorrect_player_count(self):
        players = [Player("Nick", "Kyrgios", "AUS", rank=i) for i in range(6)]
        with pytest.raises(PlayerCountNotValid) as e:
            Tournament(players)
        assert "Player count not a power of 2: 6" in str(e.value)

    def test_dict(self):
        players = [Player("Nick", "Kyrgios", "AUS", rank=i + 1) for i in range(8)]
        r1 = Round(
            [
                Match(players[0], players[1]),
                Match(players[2], players[3]),
                Match(players[4], players[5]),
                Match(players[6], players[7]),
            ]
        )
        r2 = Round(
            [
                Match(players[0], players[2]),
                Match(players[4], players[6]),
            ]
        )
        r3 = Round(
            [
                Match(players[0], players[4]),
            ]
        )
        tournament = Tournament(players)
        assert tournament.__dict__() == {
            0: r1.__dict__(),
            1: r2.__dict__(),
            2: r3.__dict__(),
        }
