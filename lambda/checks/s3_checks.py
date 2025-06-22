import boto3
from datetime import datetime
import json

s3 = boto3.client('s3')

def check_s3(event):
    buckets = s3.list_buckets().get("Buckets", [])
    findings = []

    for bucket in buckets:
        bucket_name = bucket['Name']
    
        try:
            pab = s3.get_public_access_block(Bucket=bucket_name)
            config = pab['PublicAccessBlockConfiguration']
            passed = all(config.values())
        except s3.exceptions.ClientError as e:
            passed = False
            config = {}
        
        findings.append({
            "ResourceId": bucket_name,
            "CheckType": "S3PublicAccessBlock",
            "Passed": passed,
            "Details": str(config),
            "Timestamp": datetime.utcnow().isoformat()
        })

        policy = s3.get_bucket_policy(Bucket=bucket_name)
        policy_doc = json.loads(policy['Policy'])
        for statement in policy_doc['Statement']:
            if statement['Effect'] == 'Allow' and statement['Principal'] == "*":
                findings.append({
                    "ResourceId": bucket_name,
                    "CheckType": "S3PublicPolicy",
                    "Passed": False,
                    "Details": str(statement),
                    "Timestamp": datetime.utcnow().isoformat()
                })
        versioning = s3.get_bucket_versioning(Bucket=bucket_name)
        if versioning.get("Status") != "Enabled":
            findings.append({
                "ResourceId": bucket_name,
                "CheckType": "S3Versioning",
                "Passed": False,
                "Details": "Versioning is not enabled",
                "Timestamp": datetime.utcnow().isoformat()
            })

    return findings

