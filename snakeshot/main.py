import json

from loguru import logger

from snakeshot.model.slam import Slam
from snakeshot.response import Renderer
from snakeshot.utils.printer import Printer

logger.info("Loading function")


def lambda_handler(event, context):
    # TODO : reimplement debug logging
    # logger.remove()
    # logger.add(sys.stderr, level="INFO")
    slam_name = str(event.get("slam", "Wimbledon"))
    year = int(event.get("year", 2021))
    logger.info(f"event received: Slam={slam_name}, Year={year}")
    response = {"statusCode": 200, "headers": {"Content-Type": "text/html"}}
    try:
        slam = Slam(slam_name, year, depth=1000)
    except Exception as e:
        logger.error(f"Unable to generate slam from event event: {e}")
        response.update({"body": e})
        return response
    try:
        if event.get("type") == "json":
            logger.info(f"Generating json for {slam_name} {year}")
            response.update({"headers": {"Content-Type": "application/json"}})
            response.update({"body": json.dumps(slam.as_dict())})
        else:
            try:
                body = Renderer.write(slam_name, year, slam.as_dict())
            except Exception as e:
                logger.error(f"Unable to generate html: {e}")
                body = e
            response.update({"body": body})
    except Exception as e:
        logger.error(f"Unable to process event: {e}")
        response.update({"body": e})
    return response


if __name__ == "__main__":
    lambda_handler(event={}, context={})
