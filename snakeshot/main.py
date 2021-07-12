from datetime import date
import sys

from loguru import logger

from snakeshot.response import Response

logger.info("Loading function")


def lambda_handler(event, context):
    # TODO : reimplement debug logging
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    slam = slam_name(event)
    if not slam_name:
        return Response.failure("slam is undefined")

    content = Response(slam, year(event))
    return content.as_json() if resp_json(event) else content.as_tables()


def slam_name(event: dict) -> str:
    slam = event.get("queryStringParameters", {}).get(
        "slam", event.get("http", {}).get("path", False)
    )
    return (
        slam if slam in ["aus_open", "roland_garros", "wimbledon", "us_open"] else False
    )


def year(event: dict):
    return int(event.get("queryStringParameters", {}).get("year", date.today().year))


def resp_json(event: dict) -> bool:
    return bool(event.get("queryStringParameters", {}).get("json", False))


if __name__ == "__main__":
    lambda_handler(event={}, context={})
