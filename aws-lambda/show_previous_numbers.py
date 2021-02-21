import boto3
import pprint


def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb')
    # records = dynamodb.scan(TableName="random_numbers")

    results = [{
        "id": r["id"],
        "number": r["number"],
        "timestamp": r["timestamp"],
        "max_range": r["max_range"]
        }
        for r in dynamodb.scan(TableName="random_numbers")["Items"]
    ]

    # Print the results to console
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(results)

    return results


if __name__ == "__main__":
    # only required during local dev
    from os import environ
    environ["AWS_PROFILE"] = "infrastructureci"
    environ["AWS_DEFAULT_REGION"] = "eu-west-2"

    print("Calling handler")
    resp = lambda_handler(event={}, context=None)
    print(resp)     # print the returned object as well it already being displayed in the console
