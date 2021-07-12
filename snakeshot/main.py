import json
from datetime import date
import sys

from loguru import logger

from snakeshot.response import Response

logger.info("Loading function")


def lambda_handler(event, context):
    # TODO : reimplement debug logging
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    # slam = validate_slam(event)
    # if not slam:
    #     return Response.failure("slam is undefined")

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(event, indent=4),
    }

    # content = Response(slam, validate_year(event))
    # return content.as_json() if validate_json(event) else content.as_tables()


def validate_slam(event: dict) -> str:
    slam = event.get("queryStringParameters", {}).get(
        "slam", event.get("rawPath", False)
    )
    return (
        slam if slam in ["aus_open", "roland_garros", "wimbledon", "us_open"] else False
    )


def validate_year(event: dict):
    return int(event.get("queryStringParameters", {}).get("year", date.today().year))


def validate_json(event: dict) -> bool:
    return bool(event.get("queryStringParameters", {}).get("json", False))


if __name__ == "__main__":
    lambda_handler(event={}, context={})
