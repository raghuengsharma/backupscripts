import boto3
import datetime


def calculateExpirySeconds(expiry):
    """ Set snapshot expiry in seconds since epoch"""
    now = datetime.datetime.now()
    expirydate = now + datetime.timedelta(days=expiry)
    epoch = datetime.datetime(1970, 1, 1)
    return (expirydate - epoch).total_seconds()


def currentEpochTime():
    currentTime = datetime.datetime.now()
    epoch = datetime.datetime(1970, 1, 1)
    return (currentTime - epoch).total_seconds()


profile = "default"
region = 'us-west-2'

# Snapshots corresponding to AMIs will be tagged for expiry
snapshotTagKey = "Expiry"
expiry = 0
snapshotTagValue = str(calculateExpirySeconds(expiry))

currentTimeSeconds = currentEpochTime()

tag_key = "Expiry"

boto3.setup_default_session(profile_name=profile)
ec2 = boto3.resource('ec2', region_name=region)
filters = [{'Name': 'tag-key', 'Values': [tag_key]}]
amiList = list(ec2.images.filter(Filters=filters))
deregisterList = []

# Polulate AMI list to be deregistered.
for ami in amiList:
    expiry = [f["Value"] for f in ami.tags if f["Key"] == tag_key][0]
    if float(expiry) < currentTimeSeconds:
        deregisterList.append(ami)

print "Deregistering AMIs: " + str(deregisterList)

# Derigester AMIs
for ami in deregisterList:
    ami.deregister()
    amiSnapshotFilters = [{'Name': 'description', 'Values': ["Created by CreateImage*" + str(ami.id) + "*"]}]
    amiSnapshots = list(ec2.snapshots.filter(Filters=amiSnapshotFilters))
    print "Setting amisnapshot expiry: " + str(amiSnapshots)
    snapshot_tags = [{"Key": snapshotTagKey, "Value": snapshotTagValue}]
    [snapshot.create_tags(Tags=snapshot_tags) for snapshot in amiSnapshots]
