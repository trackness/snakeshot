import logging

import pytest as pytest
from _pytest.logging import caplog
from loguru import logger

from snakeshot.model.tournament import Tournament

print(caplog)


@pytest.fixture
def loguru_caplog(caplog):
    class PropagateHandler(logging.Handler):
        def emit(self, record):
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropagateHandler(), format="{message} {extra}")
    yield caplog
    logger.remove(handler_id)


p1 = {
    "Novak Djokovic": {
        "first_name": "Novak",
        "last_name": "Djokovic",
        "nationality": "SRB",
        "seed": 1,
        "entry_type": None,
    }
}

p2 = {
    "Jack Draper": {
        "first_name": "Jack",
        "last_name": "Draper",
        "nationality": "GBR",
        "seed": None,
        "entry_type": "WC",
    }
}

p3 = {
    "Marcelo Tomas Barrios Vera": {
        "first_name": "Marcelo Tomas",
        "last_name": "Barrios Vera",
        "nationality": "CHI",
        "seed": None,
        "entry_type": "Q",
    }
}

p4 = {
    "Kevin Anderson": {
        "first_name": "Kevin",
        "last_name": "Anderson",
        "nationality": "RSA",
        "seed": None,
        "entry_type": None,
    }
}


class TestTournament:
    @pytest.fixture
    def patch_loc(self):
        return "snakeshot.model.tournament"

    def test_rounds(self, mocker, patch_loc):
        mocker.patch(f"{patch_loc}.Wimbledon.players", dict(**p1, **p2, **p3, **p4))
        under_test: Tournament = Tournament("Wimbledon", 2021, "Mens", depth=1000)
        assert len(under_test.rounds) == 2

    def test_incorrect_player_count(self, mocker, patch_loc, loguru_caplog):
        mocker.patch(f"{patch_loc}.Wimbledon.players", {0: {}, 1: {}, 2: {}})
        under_test: Tournament = Tournament("Wimbledon", 2021, "Mens", depth=1000)
        assert under_test.rounds == []
        assert (
            "2021 Wimbledon Mens draw player count is not a power of 2: 3"
            in loguru_caplog.text
        )

    def test_dict(self, mocker, patch_loc):
        r_1 = {
            0: {"players": {0: dict(**p1), 1: dict(**p2)}, "winner": dict(**p1)},
            1: {"players": {0: dict(**p3), 1: dict(**p4)}, "winner": dict(**p4)},
        }
        r_2 = {
            0: {"players": {0: dict(**p1), 1: dict(**p4)}, "winner": dict(**p1)},
        }
        mocker.patch(f"{patch_loc}.Wimbledon.players", dict(**p1, **p2, **p3, **p4))
        mocker.patch(f"{patch_loc}.Tour.rankings", {})
        mocker.patch(f"{patch_loc}.Odds.odds", {})
        mocker.patch(f"{patch_loc}.Round.as_dict", side_effect=[r_1, r_2])
        under_test: Tournament = Tournament("Wimbledon", 2021, "Mens", depth=1000)
        assert under_test.as_dict() == {0: r_1, 1: r_2}
