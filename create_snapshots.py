import boto3
import datetime

profile = "default"
region = 'us-west-2'

tag_key = "Environment"
tag_value = "production"

# Set snapshot expiry in days
expiry = 60
today = datetime.date.today()
expirydate = str(today + datetime.timedelta(days=expiry))

snapshotTagKey = "Expiry"
snapshotTagValue = expirydate

boto3.setup_default_session(profile_name=profile)
ec2 = boto3.resource('ec2', region_name=region)
# Set filters according to envronment
filters = [{'Name': 'tag:' + tag_key, 'Values': [tag_value]}]
prodinstances = list(ec2.instances.filter(Filters=filters))
for instance in prodinstances:
    instanceName = [f["Value"] for f in instance.tags if f["Key"] == "Name"][0]
    vollist = list(instance.volumes.all())
    for vol in vollist:
        description = "Snapshot for instance - " + instanceName + ", Volume - " + vol.id
        snapshot = vol.create_snapshot(Description=description)
        snapshot_tags = [{"Key": snapshotTagKey, "Value": snapshotTagValue}]
        snapshot.create_tags(Tags=snapshot_tags)
