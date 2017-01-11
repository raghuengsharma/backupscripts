import boto3
import datetime

profile = "default"
region = 'us-west-2'

def currentEpochTime():
    currentTime = datetime.datetime.now()
    epoch = datetime.datetime(1970, 1, 1)
    return (currentTime - epoch).total_seconds()


currentTimeSeconds = currentEpochTime

tag_key = "Expiry"

boto3.setup_default_session(profile_name=profile)
ec2 = boto3.resource('ec2', region_name=region)
filters = [{'Name': 'tag-key', 'Values': [tag_key]}]
snapshotList = list(ec2.snapshots.filter(Filters=filters))

removeList = []
for snapshot in snapshotList:
    expiry = [f["Value"] for f in snapshot.tags if f["Key"] == tag_key][0]
    if float(expiry) < currentTimeSeconds:
        removeList.append(snapshot)

print removeList

print "deleting snapshots: " + str(removeList)
[snapshot.delete() for snapshot in removeList]
