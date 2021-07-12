import json
import sys

from loguru import logger

from snakeshot.response import Response

logger.info("Loading function")


def lambda_handler(event=None, _context=None):
    # TODO : reimplement debug logging
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.info("### queryStringParameters ###")
    [logger.info(f"{k}: {v}") for k, v in event.get("queryStringParameters", {})]
    logger.info("### pathParameters ###")
    [logger.info(f"{k}: {v}") for k, v in event.get("pathParameters", {})]
    slam = str(event.get("slam", "Wimbledon"))
    # slam = str(event.get("queryStringParameters", {}).get("slam", None))
    year = int(event.get("year", 2021))
    response_type = str(event.get("response_type"))
    logger.info(f"{slam} {year} event received")
    content = Response(slam, year)
    return content.as_json() if response_type == "json" else content.as_tables()


if __name__ == "__main__":
    lambda_handler(event={})
