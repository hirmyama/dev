# バケット一覧

import boto3
from pprint import pprint

s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    pprint(bucket)

