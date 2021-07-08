from snakeshot.model.slam import Slam


class TestSlam:
    def test_player_pool(self):
        slam: Slam = Slam({"slam": "wimbledon", "tour": "mens"}, 300)
        assert len(slam._player_pools.get("M")) == 300
        assert len(slam._player_pools.get("W")) == 300

    def test_scrape_odds_list(self):
        pass
