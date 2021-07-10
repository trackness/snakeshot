import json

from loguru import logger

from snakeshot.model.slam import Slam
from snakeshot.html import Renderer
from snakeshot.utils.printer import Printer

logger.info("Loading function")


def lambda_handler(event, context):
    # TODO : reimplement debug logging
    # logger.remove()
    # logger.add(sys.stderr, level="INFO")
    slam_name = str(event.get("slam", "Wimbledon"))
    year = int(event.get("year", 2021))
    logger.info(f"event received: Slam={slam_name}, Year={year}")
    response = {"statusCode": 200}
    try:
        slam = Slam(slam_name, year, depth=1000)
    except Exception as e:
        logger.error(f"Unable to generate slam from event event: {e}")
        response.update({"headers": {"Content-Type": "text/html"}})
        response.update({"body": e})
        return response
    try:
        if event.get("type") == "json":
            logger.info(f"Generating json for {slam_name} {year}")
            response.update({"headers": {"Content-Type": "application/json"}})
            response.update({"body": json.dumps(slam.as_dict())})
        else:
            logger.info(f"Generating tables for {slam_name} {year}")
            try:
                tables = Renderer.write(
                    slam_name, year, Printer.table(slam.tournaments)
                )
            except Exception as e:
                tables = e
            response.update({"headers": {"Content-Type": "text/html"}})
            response.update({"body": tables})
    except Exception as e:
        logger.error(f"Unable to process event: {e}")
        response.update({"headers": {"Content-Type": "text/html"}})
        response.update({"body": e})
    return response


# if __name__ == "__name___main__":
#     table = lambda_handler({}, {}).get("body")
#     json_outcome = lambda_handler({"type": "table"}, {}).get("body")
#     print(json.dumps(json_outcome, indent=2))
