import boto3
import json
from checks import s3_checks, ec2_checks, ebs_checks, rds_checks
from utils.notifier import send_alert

def lambda_handler(event, context):
    resource_type = identify_resource_type(event)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('SecurityFindings')

    findings = []

    if resource_type == "s3":
        findings += s3_checks.check_s3(event)
    if resource_type == "ebs":
        findings += ebs_checks.check_ebs(event)
    if resource_type == "ec2":
        findings += ec2_checks.check_ec2(event)
    if resource_type == "rds":
        findings += rds_checks.check_rds(event)

    for finding in findings:
        table.put_item(Item=finding)
        if not finding['Passed']:
            send_alert(finding)
    print("Received event", json.dumps(event))

    return {"statusCode":200, "body": "Check completed"}


def identify_resource_type(event):
    source = event.get("source", "")
    event_name = event.get("detail", {}).get("eventName", "").lower()

    if "s3" in source:
        return "s3"
    if "ec2" in source:
        if any(x in event_name for x in ["createvolume", "deletevolume", "modifyvolume", "attachvolume", "detachvolume"]):
            return "ebs"
        else:
            return "ec2"
    if "rds" in source:
        return "rds"
    return None