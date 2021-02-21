import boto3
from datetime import datetime
from time import time
from random import randrange
import json


def lambda_handler(event, context):

    try:
        # Pull max range from event
        max_range = event.get("queryStringParameters", {}).get("max_range") or 30
        max_range = int(max_range)
        current_date_time = str(datetime.utcnow())

        # Generate a random number from the max range.
        # Check a positive value has been passed
        if max_range >= 1:
            # Start count from 1 and ensure the range goes up to the max_range value (can include it)
            random_number = randrange(1, max_range + 1)

            # Generate a unique value from the epoc time and random number to use as the database hash key
            hash_key = str(time() + random_number)

            # Build response object
            db_object = {
                "id": hash_key,
                "number": random_number,
                "timestamp": current_date_time,
                "max_range": max_range
            }

            # Write to DB
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('random_numbers')
            table.put_item(Item=db_object)

            response_object = {
                'statusCode': 201,
                'body': json.dumps(db_object)
            }

            return response_object

        else:
            function_error = "ERR: 'max_range' must be an integer and >= 1"
            return False, function_error, 400

    except ValueError:
        function_error = "ERR: parameter must be cast-able to an integer"
        return False, function_error, 400


if __name__ == "__main__":
    # only required during local dev
    from os import environ
    environ["AWS_PROFILE"] = "infrastructureci"
    environ["AWS_DEFAULT_REGION"] = "eu-west-2"

    # Simulate a Lambda event
    print("Calling handler")
    dummy_event = {
        "queryStringParameters": {
            "max_range": 55
        }
    }
    resp = lambda_handler(event=dummy_event, context=None)
    print(resp)
