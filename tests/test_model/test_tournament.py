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
    def test_rounds(self, mocker):
        mocker.patch(
            "snakeshot.model.tournament.Wimbledon.players", dict(**p1, **p2, **p3, **p4)
        )
        under_test: Tournament = Tournament("Wimbledon", 2021, "Mens", depth=1000)
        assert len(under_test.rounds) == 2

    def test_incorrect_player_count(self, mocker, loguru_caplog):
        mocker.patch(
            "snakeshot.model.tournament.Wimbledon.players", {0: {}, 1: {}, 2: {}}
        )
        under_test: Tournament = Tournament("Wimbledon", 2021, "Mens", depth=1000)
        assert under_test.rounds == []
        assert (
            "2021 Wimbledon Mens draw player count is not a power of 2: 3"
            in loguru_caplog.text
        )

    def test_dict(self, mocker):
        mocker.patch(
            "snakeshot.model.tournament.Wimbledon.players", dict(**p1, **p2, **p3, **p4)
        )
        under_test: Tournament = Tournament("Wimbledon", 2021, "Mens", depth=1000)
        assert under_test.__dict__() == {
            0: {
                0: {
                    "players": {
                        0: {
                            "Novak Djokovic": {
                                "entry_type": None,
                                "first_name": "Novak",
                                "last_name": "Djokovic",
                                "nationality": "SRB",
                                "odds": 1.28,
                                "rank": 1,
                                "seed": 1,
                            }
                        },
                        1: {
                            "Jack Draper": {
                                "entry_type": "WC",
                                "first_name": "Jack",
                                "last_name": "Draper",
                                "nationality": "GBR",
                                "odds": None,
                                "rank": 253,
                                "seed": None,
                            }
                        },
                    },
                    "winner": {
                        "Novak Djokovic": {
                            "entry_type": None,
                            "first_name": "Novak",
                            "last_name": "Djokovic",
                            "nationality": "SRB",
                            "odds": 1.28,
                            "rank": 1,
                            "seed": 1,
                        }
                    },
                },
                1: {
                    "players": {
                        0: {
                            "Marcelo Tomas Barrios Vera": {
                                "entry_type": "Q",
                                "first_name": "Marcelo Tomas",
                                "last_name": "Barrios Vera",
                                "nationality": "CHI",
                                "odds": None,
                                "rank": 209,
                                "seed": None,
                            }
                        },
                        1: {
                            "Kevin Anderson": {
                                "entry_type": None,
                                "first_name": "Kevin",
                                "last_name": "Anderson",
                                "nationality": "RSA",
                                "odds": 770.0,
                                "rank": 102,
                                "seed": None,
                            }
                        },
                    },
                    "winner": {
                        "Kevin Anderson": {
                            "entry_type": None,
                            "first_name": "Kevin",
                            "last_name": "Anderson",
                            "nationality": "RSA",
                            "odds": 770.0,
                            "rank": 102,
                            "seed": None,
                        }
                    },
                },
            },
            1: {
                0: {
                    "players": {
                        0: {
                            "Novak Djokovic": {
                                "entry_type": None,
                                "first_name": "Novak",
                                "last_name": "Djokovic",
                                "nationality": "SRB",
                                "odds": 1.28,
                                "rank": 1,
                                "seed": 1,
                            }
                        },
                        1: {
                            "Kevin Anderson": {
                                "entry_type": None,
                                "first_name": "Kevin",
                                "last_name": "Anderson",
                                "nationality": "RSA",
                                "odds": 770.0,
                                "rank": 102,
                                "seed": None,
                            }
                        },
                    },
                    "winner": {
                        "Novak Djokovic": {
                            "entry_type": None,
                            "first_name": "Novak",
                            "last_name": "Djokovic",
                            "nationality": "SRB",
                            "odds": 1.28,
                            "rank": 1,
                            "seed": 1,
                        }
                    },
                },
            },
        }
