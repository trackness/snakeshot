import json
import os

from jinja2 import Template, Environment, FileSystemLoader
from loguru import logger

from snakeshot.model.slam import Slam

html = "text/html"


class Response:
    def __init__(self, name: str, year: int):
        self._name = name
        self._year = year
        self._slam = Slam(name, year, depth=500)

    def as_json(self) -> dict:
        try:
            slam_dict = self._slam.as_dict()
        except Exception as e:
            return Response._failure(
                e, f"Unable to generate {self._name} {self._year} dict"
            )
        try:
            logger.info(f"Generating {self._name} {self._year} json")
            return Response._success("application/json", json.dumps(slam_dict))
        except Exception as e:
            return Response._failure(
                e, f"Unable to generate {self._name} {self._year} json"
            )

    def as_tables(self) -> dict:
        try:
            return Response._success(html, self._write())
        except Exception as e:
            return Response._failure(
                e, f"Unable to generate {self._name} {self._year} html tables"
            )

    def _write(self, local=False) -> str:
        logger.info(f"Generating {self._name} {self._year} html tables")

        logger.info("Loading template")
        template: Template = Environment(
            loader=FileSystemLoader(
                os.path.join(os.path.dirname(__file__), "templates")
            ),
            autoescape=True,
        ).get_template("tables.html")

        logger.info("Making template substitutions")
        subs = template.render(title=f"{self._name} {self._year}", slam=self._slam)
        if local:
            with open("index.html", "w") as f:
                f.write(subs)
        return subs

    @classmethod
    def _success(cls, content_type, body) -> dict:
        return {
            "statusCode": 200,
            "headers": {"Content-Type": content_type},
            "body": body,
        }

    @classmethod
    def _failure(cls, e: Exception, message: str) -> dict:
        logger.error(f"{message}: {type(e)} - {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": html},
            "body": str(e),
        }

    @classmethod
    def failure(cls, message: str) -> dict:
        logger.error(f"{message}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": html},
            "body": message,
        }
