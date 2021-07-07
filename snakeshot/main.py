import json

from snakeshot.model.slams.wimbledon import Wimbledon
from snakeshot.utils.printer import Printer

from loguru import logger

logger.info("Loading function")


def lambda_handler(event, context):
    slam_name = str(event.get("slam", "Wimbledon"))
    year = int(event.get("year", 2021))
    logger.info(f"message received: Slam={slam_name}, Year={year}")
    slams = {
        # "australian_open": AustralianOpen,
        # "roland_garros", RolandGarros,
        "wimbledon": Wimbledon,
        # "us_open": USOpen
    }
    slam = slams.get(slam_name.lower())(year)
    try:
        response = {"statusCode": 200}
        if event.get("type") == "table":
            logger.info(f"Generating table for {slam_name} {year}")
            response.update({"headers": {"Content-Type": "text/html"}})
            response.update({"body": Printer.table(slam.tournaments)})
        else:
            logger.info(f"Generating json for {slam_name} {year}")
            response.update({"headers": {"Content-Type": "application/json"}})
            response.update({"body": json.dumps(slam.__dict__())})
        return response
    except Exception as e:
        logger.error(f"Unable to process event: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": {"error": e},
        }
