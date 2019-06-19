# バケット作成

import boto3
from pprint import pprint

s3 = boto3.resource('s3')

result = s3.create_bucket(Bucket='test-2232938739278334', 
    CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-1'})

pprint(result)
