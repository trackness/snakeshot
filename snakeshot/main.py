import os

print("Loading function")


def lambda_handler(event, context):
    try:
        # print(f"Received event: {json.dumps(event, indent=2)}")
        # [print(f"value = {value}") for value in event]
        # return event["key1"]  # Echo back the first key value
        json_region = os.environ["AWS_REGION"]
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": f"[{json_region}] Anwar just seems like such an odd name for a girl dog. "
            f"Best girl on the island regardless.",
            # TODO : Body goes here as json
        }

    except Exception as e:
        raise Exception(f"Something went wrong: {e}")
