# import os
#
from snakeshot.model.slams.wimbledon import Wimbledon
from snakeshot.utils.printer import Printer

print("Loading function")


def lambda_handler(event, context):
    try:
        response = {"statusCode": 200}
        if event.get("type") == "table":
            response.update({"headers": {"Content-Type": "text/html"}})
            response.update({"body": Printer.table(Wimbledon(2021).tournaments)})
        else:
            response.update({"headers": {"Content-Type": "application/json"}})
            response.update({"body": Printer.json(Wimbledon(2021).tournaments)})
        return response

    except Exception as e:
        raise Exception(f"Something went wrong: {e}")
