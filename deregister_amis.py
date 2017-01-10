import boto3
import datetime

profile = "default"
region = 'us-west-2'
today = datetime.date.today()
expiryAMI = str(today)
tag = "Expiry"
tagValue = expiryAMI

# Expire snapshots corresponding to AMI tomorrow
expirySnapshot = str(today + datetime.timedelta(days=1))

snapshotTagKey = "Expiry"
snapshotTagValue = expirySnapshot

boto3.setup_default_session(profile_name=profile)
ec2 = boto3.resource('ec2', region_name=region)
filters = [{'Name': 'tag:' + tag, 'Values': [tagValue]}]
amis = list(ec2.images.filter(Filters=filters))
print "Deregistering AMIs: " + str(amis)
for ami in amis:
    ami.deregister()
    amiSnapshotFilters = [{'Name': 'description', 'Values': ["Created by CreateImage*" + str(ami.id) + "*"]}]
    amiSnapshots = list(ec2.snapshots.filter(Filters=amiSnapshotFilters))
    print "Setting amisnapshot deletion for tomorrow: " + str(amiSnapshots)
    snapshot_tags = [{"Key": snapshotTagKey, "Value": snapshotTagValue}]
    [snapshot.create_tags(Tags=snapshot_tags) for snapshot in amiSnapshots]
