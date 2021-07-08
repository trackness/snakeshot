import pytest as pytest
from pytest import param

from snakeshot.sources.odds import Odds


def url(slam: str, tour: str) -> str:
    return (
        f"https://www.oddschecker.com/tennis/"
        f"{slam.lower()}/{tour.lower()}/"
        f"{tour.lower()}-{slam.lower()}/winner"
    )


class TestOdds:
    @pytest.mark.parametrize(
        "slam, tour, expected",
        [
            param("Wimbledon", "Mens", 3),
            param("Wimbledon", "Womens", 2),
        ],
    )
    def test_odds(self, requests_mock, slam, tour, expected):
        with open(f"odds/{tour.lower()}-{slam.lower()}.htm") as f:
            contents = f.read()
        requests_mock.get(url(slam, tour), text=contents)
        assert len(Odds(slam, tour).odds) == expected

    @pytest.mark.parametrize("inp", [param(None), param(""), param("foo")])
    def test_empty_response(self, requests_mock, inp):
        requests_mock.get(url("Wimbledon", "Mens"), text=inp)
        assert len(Odds("Wimbledon", "Mens").odds) == 0

    def test_request_errors(self, requests_mock):
        requests_mock.get(url("Wimbledon", "Mens"), text=None)
        # with pytest.raises(HTTPError) as e:
        content = Odds("Wimbledon", "Mens").odds
        # assert "HTTP error: abc" in str(e.value)
        assert content == {}
