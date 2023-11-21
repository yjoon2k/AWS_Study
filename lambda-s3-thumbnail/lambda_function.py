import boto3
from PIL import Image
            
s3 = boto3.client('s3')
            
def lambda_handler(event, context):
  for record in event['Records']:
    bucket_upload = record['s3']['bucket']['name']
    bucket_save = bucket_upload[:14] + "after"
    key = record['s3']['object']['key']
    s3.download_file(bucket_upload, key, "/tmp/" + key)
    with Image.open("/tmp/" + key) as image:
        image.thumbnail(tuple(x / 2 for x in image.size))
        image.save("/tmp/" + key)
    s3.upload_file("/tmp/" + key, bucket_save, "/tmp/resized-" + key)