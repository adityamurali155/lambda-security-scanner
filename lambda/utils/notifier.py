import boto3
import json
import os

sns = boto3.client('sns')

sns_topic_arn = os.environ['SNS_TOPIC_ARN']

def publish_alert(finding):
    message = {
        "Alert": "Security Alert!",
        "Resource": finding["ResourceId"],
        "Check": finding["CheckType"],
        "Details": finding["Details"],
        "Timestamp": finding["Timestamp"]
    }

    response = sns.publish(
        TopicArn=sns_topic_arn,
        Subject="AWS Security Alert",
        Message=json.dumps(message, indent=2)
    )
    print("SNS Alert Published:", response)