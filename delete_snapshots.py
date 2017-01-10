import boto3
import datetime

profile = "default"
region = 'us-west-2'
today = datetime.date.today()
expiry = str(today)
tag = "Expiry"
tagValue = expiry
boto3.setup_default_session(profile_name=profile)
ec2 = boto3.resource('ec2', region_name=region)
filters = [{'Name': 'tag:' + tag, 'Values': [tagValue]}]
snapshots = list(ec2.snapshots.filter(Filters=filters))
print "deleting snapshots: " + str(snapshots)
[snapshot.delete() for snapshot in snapshots]
