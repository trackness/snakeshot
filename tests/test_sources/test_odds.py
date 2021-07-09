from collections import Mapping
from urllib.error import HTTPError

import responses

from pytest import param

from snakeshot.sources.odds import Odds

import logging
import pytest
from _pytest.logging import caplog
from loguru import logger
import pkg_resources


print(caplog)


def url(slam: str = "Wimbledon", tour: str = "Mens") -> str:
    return (
        f"https://www.oddschecker.com/tennis/"
        f"{slam.lower()}/{tour.lower()}/"
        f"{tour.lower()}-{slam.lower()}/winner"
    )


@pytest.fixture
def loguru_caplog(caplog):
    class PropagateHandler(logging.Handler):
        def emit(self, record):
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropagateHandler(), format="{message} {extra}")
    yield caplog
    logger.remove(handler_id)


class TestOdds:
    @responses.activate
    @pytest.mark.parametrize(
        "slam, tour, expected",
        [
            param("Wimbledon", "Mens", 4),
            param("Wimbledon", "Womens", 2),
        ],
    )
    def test_odds(self, slam, tour, expected):

        with open(
            pkg_resources.resource_filename(
                "tests.fixtures.sources.odds", f"{tour.lower()}-{slam.lower()}.htm"
            )
        ) as f:
            contents = f.read()
        responses.add(
            responses.GET,
            url(slam, tour),
            body=contents,
            status=200,
            content_type="text/html",
        )
        assert len(Odds(slam, tour).odds) == expected

    class TestRequests:
        @responses.activate
        @pytest.mark.parametrize(
            "inp",
            [param(None, id="None"), param("", id="empty"), param("foo", id="invalid")],
        )
        def test_empty_response(self, inp):
            responses.add(
                responses.GET, url(), body=inp, status=200, content_type="text/html"
            )
            assert Odds("Wimbledon", "Mens").odds == {}

        @responses.activate
        @pytest.mark.parametrize(
            "exc, text",
            [
                param(
                    HTTPError(
                        msg="HTTP", fp=None, code=500, hdrs=Mapping["", ""], url=""
                    ),
                    "HTTP",
                    id="HTTPError",
                ),
                param(Exception("non-HTTP"), "non-HTTP", id="non-HTTPError"),
            ],
        )
        def test_request_errors(self, loguru_caplog, exc, text):
            responses.add(responses.GET, url(), body=exc)
            assert Odds("Wimbledon", "Mens").odds == {}
            assert text in loguru_caplog.text

    class TestBeautifulSoup:
        pass
