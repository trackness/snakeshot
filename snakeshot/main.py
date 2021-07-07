import json

from snakeshot.model.slams.wimbledon import Wimbledon
from snakeshot.utils.printer import Printer

print("Loading function")


def lambda_handler(event, context):
    slams = {
        # "australian_open": AustralianOpen,
        # "roland_garros", RolandGarros,
        "wimbledon": Wimbledon,
        # "us_open": USOpen
    }
    slam = slams.get(str(event.get("slam")).lower(), Wimbledon)(2021)
    # print(slam.tournaments.keys())
    try:
        response = {"statusCode": 200}
        if event.get("type") == "table":
            response.update({"headers": {"Content-Type": "text/html"}})
            response.update({"body": Printer.table(slam.tournaments)})
        else:
            response.update({"headers": {"Content-Type": "application/json"}})
            response.update({"body": json.dumps(slam.__dict__())})
        return response
    except Exception as e:
        raise Exception(f"Something went wrong: {e}")
