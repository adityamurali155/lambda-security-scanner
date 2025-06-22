import boto3
from datetime import datetime

rds = boto3.client('rds')

def check_rds(event):
    findings = []

    response = rds.describe_db_instances()

    for db in response['DBInstances']:
        db_id = db['DBInstanceIdentifier']

        if db['PubliclyAccessible']:
            findings.append({
                "ResourceId": db_id,
                "CheckType": "RDSPublicAccess",
                "Passed": False,
                "Details": "Publicly accessible database",
                "Timestamp": datetime.utcnow().isoformat()
            })
        if not db['StorageEncrypted']:
            findings.append({
                "ResourceId": db_id,
                "CheckType": "RDSEncryption",
                "Passed": False,
                "Details": "Storage encryption is not enabled",
                "Timestamp": datetime.utcnow().isoformat()
            })
        if not db.get('IAMDatabaseAuthenticationEnabled', False):
            findings.append({
                "ResourceId": db_id,
                "CheckType": "RDSIAMAuth",
                "Passed": False,
                "Details": "IAM DB authentication is not enabled",
                "Timestamp": datetime.utcnow().isoformat()
            })

    return findings
