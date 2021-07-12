import json
import sys

from loguru import logger

from snakeshot.response import Response

logger.info("Loading function")


def lambda_handler(event, context):
    # TODO : reimplement debug logging
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    slam = event.get("queryStringParameters", {}).get("slam", None)
    if slam is None:
        return Response.failure("slam is undefined")

    year = event.get("queryStringParameters", {}).get("year", None)
    if year is None:
        return Response.failure("year is undefined")

    response_type = str(
        event.get("queryStringParameters", {}).get("response_type", None)
    )

    logger.info(f"{slam} {year} event received")
    content = Response(slam, year)
    return content.as_json() if response_type == "json" else content.as_tables()


if __name__ == "__main__":
    lambda_handler(event={}, context={})
