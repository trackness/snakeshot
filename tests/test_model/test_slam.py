from unittest.mock import MagicMock

from snakeshot.model.slam import Slam


class TestSlam:
    def test_init(self, mocker):
        mocker.patch("snakeshot.model.slam.Tournament", MagicMock())
        under_test: Slam = Slam("Wimbledon", 2021)
        assert len(under_test.tournaments) == 2
        for g in under_test.tournaments.keys():
            assert g in ["Mens", "Womens"]
