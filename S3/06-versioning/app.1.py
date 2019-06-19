# バージョニングを有効化したバケットを作成

import boto3
from pprint import pprint

s3 = boto3.resource('s3')

bucket = s3.create_bucket(Bucket='test-2232938373933278334', 
    CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-1'})

result = bucket.Versioning().enable()
pprint(result)