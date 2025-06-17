import boto3
from datetime import datetime

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
    return findings

