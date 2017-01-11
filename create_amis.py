import boto3
import datetime


def calculateExpirySeconds(expiry):
    """ Set snapshot expiry in seconds since epoch"""
    now = datetime.datetime.now()
    expirydate = now + datetime.timedelta(days=expiry)
    epoch = datetime.datetime(1970, 1, 1)
    return (expirydate - epoch).total_seconds()


def createAMIs(tag_key, tag_value, expiry):
    profile = "default"
    region = 'us-west-2'

    backupTagKey = "Backup"
    backupTagValue = "True"

    amiTagKey = "Expiry"
    amiTagValue = str(calculateExpirySeconds(expiry))

    boto3.setup_default_session(profile_name=profile)
    ec2 = boto3.resource('ec2', region_name=region)
    # Set filters according to envronment
    filters = [{'Name': 'tag:' + backupTagKey, 'Values': [backupTagValue]},
               {'Name': 'tag:' + tag_key, 'Values': [tag_value]}]
    prodinstances = list(ec2.instances.filter(Filters=filters))
    for instance in prodinstances:
        instanceName = [f["Value"] for f in instance.tags if f["Key"] == "Name"][0]
        print instanceName
        amiName = instanceName + "_ami"
        amiDescription = "AMI for instance - " + instanceName
        ami = instance.create_image(Name=amiName, Description=amiDescription)
        amiTags = [{"Key": amiTagKey, "Value": amiTagValue}]
        ami.create_tags(Tags=amiTags)


env = "production"
tag_key = "Environment"
tag_value = env
expiry = 60
createAMIs(tag_key, tag_value, expiry)
