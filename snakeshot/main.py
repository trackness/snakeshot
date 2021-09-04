import webbrowser
from datetime import date
import sys
from pathlib import Path

from loguru import logger

from snakeshot.response import Response

logger.info("Loading function")


def lambda_handler(event: dict, context):
    # TODO : reimplement debug logging
    logger.remove()
    logger.add(sys.stderr, level="DEBUG", enqueue=False)

    params: dict = event.get("queryStringParameters")
    if not params:
        return Response.failure("No query parameters provided (e.g.: /?slam=wimbledon)")

    year = validate_year(params)
    slam = validate_slam(params)
    if not slam:
        return Response.failure("Slam is undefined (e.g.: /?slam=wimbledon)")

    content = Response(slam, year)
    return content.as_json() if validate_json(params) else content.as_tables()


def validate_slam(params: dict) -> str:
    slam = params.get("slam", "").replace("/", "")
    return (
        slam if slam in ["aus_open", "roland_garros", "wimbledon", "us_open"] else False
    )


def validate_year(params: dict):
    return int(params.get("year", date.today().year))


def validate_json(params: dict) -> bool:
    return bool(params.get("json", False))


if __name__ == "__main__":
    r: dict = lambda_handler(
        event={"queryStringParameters": {"slam": "us_open"}}, context={}
    )
    output = Path(__file__).parent.resolve().joinpath("test.html")
    with open(output, "w") as f:
        f.write(r.get("body"))
    webbrowser.open(f"file:{output}")
