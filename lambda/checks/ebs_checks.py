import boto3
from datetime import datetime
ec2 = boto3.client('ec2')

def check_ebs(event):

    response = ec2.describe_volumes()
    findings = []

    for volume in response['Volumes']:
        volume_id = volume['VolumeId']
        encrypted = volume['Encrypted']
        az = volume['AvailabilityZone']
        attachments = volume.get('Attachments', [])
        instance_id = attachments[0]['InstanceId'] if attachments else "Not attached"

        if not encrypted:
            finding = findings.append({
                "ResourceId": volume_id,
                "CheckType": "EBSNotEncrypted",
                "Passed": False,
                "Details": f"Volume {volume_id} is not encrypted",
                "Timestamp": datetime.utcnow().isoformat()
            })
        findings.append(finding)
        
    return findings