from snakeshot.sources.tour import Tour


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
