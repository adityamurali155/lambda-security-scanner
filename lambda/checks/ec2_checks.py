import boto3
import datetime

ec2 = boto3.client('ec2')

def check_ec2(event):
    sg_response = ec2.describe_security_groups()
    instance_response = ec2.describe_instances()
    print(sg_response)
    print("***********")
    print(instance_response)

    findings = []
    sg_to_instance = {}

    for reservation in instance_response['Reservations']:
        for instance in reservation['Instances']:
           instance_id = instance['InstanceId']
           instance_name = ''
        for tag in instance.get('Tags',[]):
             if tag['Key'] == 'Name':
                instance_name = tag['Value']
        for sg in instance.get('SecurityGroups', []):
                sg_id = sg['GroupId']
                if sg_id not in sg_to_instance:
                    sg_to_instance[sg_id] = []
                sg_to_instance[sg_id].append({
                    "Instance ID": instance_id, 
                    "Instance Name": instance_name
                })

    for sg in sg_response['SecurityGroups']:
        sg_id = sg['GroupId']
        sg_name = sg.get('GroupName', "Unnamed")
        open = False

        for perm in sg['IpPermissions']:
            from_port = perm.get('FromPort')
            to_port = perm.get('ToPort')
            if from_port == 22 and to_port == 22:
                for ip_range in perm.get('IpRanges', []):
                    if ip_range.get('CidrIp') == '0.0.0.0/0':
                        open = True
                        attached_instances = sg_to_instance.get(sg_id, [])
                        for i in attached_instances:
                            findings.append({
                                "ResourceId": sg_id,
                                "CheckType": "SSHOpenToInternet",
                                "Passed": False,
                                "Details": f"Open to Internet: {i['Instance ID']}",
                                "Timestamp": datetime.datetime.utcnow().isoformat()
                            })
    return findings 