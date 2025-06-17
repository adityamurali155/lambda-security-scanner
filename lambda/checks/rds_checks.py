import boto3
from datetime import datetime

rds = boto3.client('rds')

def check_rds(event):
    findings = []

    response = rds.describe_db_instances()

    for db in response['DBInstances']:
        db_id = db['DBInstanceIdentifier']
        is_public = db.get('PubliclyAccessible', False)

        findings.append({
            "ResourceId": db_id,
            "CheckType": "RDSPublicAccess",
            "Passed": not is_public,
            "Details": "Publicly accessible" if is_public else "Not publicly accessible",
            "Timestamp": datetime.utcnow().isoformat()
        })

    return findings
