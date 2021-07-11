import json
import sys

from loguru import logger

from snakeshot.model.slam import Slam
from snakeshot.response import Renderer

logger.info("Loading function")


def lambda_handler(event, context):
    # TODO : reimplement debug logging
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    slam = str(event.get("slam", "Wimbledon"))
    year = int(event.get("year", 2021))
    logger.info(f"{slam} {year} event received")
    return snakeshot(slam, year, str(event.get("response_type", "table")))


def snakeshot(name: str, year: int, response_type: str) -> dict:
    try:
        slam = Slam(name, year, depth=1000)
    except Exception as e:
        return failure(e, f"Unable to generate {name} {year} slam")

    try:
        slam_dict = slam.as_dict()
    except Exception as e:
        return failure(e, f"Unable to generate {name} {year} dict")

    if response_type == "json":
        try:
            logger.info(f"Generating {name} {year} json")
            return success("application/json", json.dumps(slam_dict))
        except Exception as e:
            return failure(e, f"Unable to generate {name} {year} json")
    else:
        try:
            return success("text/html", Renderer.write(name, year, slam_dict))
        except Exception as e:
            return failure(e, f"Unable to generate {name} {year} html tables")


def success(content_type, body) -> dict:
    return {"statusCode": 200, "headers": {"Content-Type": content_type}, "body": body}


def failure(e: Exception, message: str) -> dict:
    logger.error(f"{message}: {type(e)} - {e}")
    return {"statusCode": 500, "headers": {"Content-Type": "text/html"}, "body": str(e)}


if __name__ == "__main__":
    lambda_handler(event={}, context={})
