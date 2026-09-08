import boto3
import os
import json
import logging

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("inventory")

sns = boto3.client("sns")
topic_arn = os.environ["SNS_TOPIC_ARN"]

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    if "body" in event:
        event = json.loads(event["body"])

    logger.info(f"Processing inventory item: {event.get('item')}")

    required_fields = ["item", "quantity", "unit", "minimum_stock"]

    for field in required_fields:
        if field not in event:
            return {
                "statusCode": 400,
                "body": f"Missing required field: {field}"
            }
    if event["quantity"] < 0:
        return {
            "statusCode": 400,
            "body": "Quantity cannot be negative"
        }

    if event["minimum_stock"] < 0:
        return {
            "statusCode": 400,
            "body": "Minimum stock cannot be negative"
        }

    table.put_item(
        Item={
            "item": event["item"],
            "quantity": event["quantity"],
            "unit": event["unit"],
            "minimum_stock": event["minimum_stock"]
        }
    )
    if event["quantity"] <= event["minimum_stock"]:
        stock_status = "LOW STOCK"
        logger.info(f"Stock status: {stock_status}")

        sns.publish(
            TopicArn=topic_arn,
            Subject=f"Low stock alert: {event['item']}",
            Message=f"{event['item']} is low on stock. Current quantity: {event['quantity']} {event['unit']}. Minimum stock: {event['minimum_stock']}."
        )

    else:
        stock_status = "STOCK OK"

        logger.info(f"Stock status: {stock_status}")
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": f"{event['item']} added to inventory",
            "status": stock_status
        })
    }
