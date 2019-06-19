# オブジェクト一覧

import boto3
from pprint import pprint

s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    for object in bucket.objects.all():
        pprint(object)
