import boto3

s3 = boto3.resource('s3')

def clean_objects(bucket):
    s3.Bucket(bucket).objects.delete()
