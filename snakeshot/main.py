import json

from loguru import logger

from snakeshot.model.slam import Slam
from snakeshot.utils.printer import Printer

logger.info("Loading function")


def lambda_handler(event, context):
    # TODO : reimplement debug logging
    # logger.remove()
    # logger.add(sys.stderr, level="INFO")
    slam_name = str(event.get("slam", "Wimbledon"))
    year = int(event.get("year", 2021))
    logger.info(f"message received: Slam={slam_name}, Year={year}")
    slam = Slam(slam_name, year, depth=1000)
    try:
        response = {"statusCode": 200}
        if event.get("type") == "table":
            logger.info(f"Generating tables for {slam_name} {year}")
            tables = Printer.table(slam.tournaments)
            for t in tables.values():
                for row in t:
                    print(row)
            response.update({"headers": {"Content-Type": "text/html"}})
            response.update({"body": tables})
        else:
            logger.info(f"Generating json for {slam_name} {year}")
            response.update({"headers": {"Content-Type": "application/json"}})
            response.update({"body": json.dumps(slam.__dict__())})
        return response
    except Exception as e:
        logger.error(f"Unable to process event: {e}")
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": {"error": e},
        }


if __name__ == "__main__":
    # json_outcome = lambda_handler({}, {}).get("body")
    table = lambda_handler({"type": "table"}, {}).get("body")
