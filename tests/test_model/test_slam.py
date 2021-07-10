from unittest import mock
from unittest.mock import patch, MagicMock

import pytest as pytest

from snakeshot.model.slam import Slam


class TestSlam:
    @pytest.fixture
    def patch_loc(self):
        return "snakeshot.model.slam"

    def test_init(self, mocker, patch_loc):
        mocker.patch(f"{patch_loc}.Tournament", MagicMock())
        under_test: Slam = Slam("Wimbledon", 2021)
        assert len(under_test.tournaments) == 2
        for g in under_test.tournaments.keys():
            assert g in ["Mens", "Womens"]

    @mock.patch("snakeshot.model.slam.Tournament")
    def test_dict(self, mock_tournament):
        expected = {"tournament": "rounds"}
        mock_tournament.return_value.as_dict.return_value = expected
        under_test: Slam = Slam("Wimbledon", 2021)
        assert under_test.as_dict() == {"Mens": expected, "Womens": expected}
