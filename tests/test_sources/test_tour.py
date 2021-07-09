import pytest as pytest

from snakeshot.sources.tour import Tour

import responses

import pkg_resources


def url(target: str, assoc: str) -> str:
    return (
        f"https://raw.githubusercontent.com/JeffSackmann/tennis_"
        f"{assoc}/master/{assoc}_{target}.csv"
    )


def file_to_str(file_name):
    with open(
        pkg_resources.resource_filename("tests.fixtures.sources.tour", file_name)
    ) as f:
        return f.read()


def response_setup(r, assoc, target):
    rankings = file_to_str(f"{assoc}_{target}.csv")
    r.add(
        responses.GET,
        url(target, assoc),
        body=rankings,
        status=200,
        content_type="text/html",
        stream=True,
    )


class TestTour:
    @pytest.fixture(params=["atp", "wta"])
    def assoc(self, request):
        return request.param

    @pytest.fixture(params=[500, 1000])
    def depth(self, request):
        return request.param

    @responses.activate
    def test_init(self, assoc, depth):
        response_setup(responses, assoc, "players")
        response_setup(responses, assoc, "rankings_current")

        under_test: Tour = Tour(assoc, depth)
        for rank in under_test.players.values():
            assert rank <= depth
