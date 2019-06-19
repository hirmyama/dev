# バケット作成（関数化）

import boto3
from pprint import pprint
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')

def create_bucket(bucket_name, region='ap-northeast-1'):
    try:
        result = s3.create_bucket(Bucket=bucket_name, 
            CreateBucketConfiguration={'LocationConstraint': region})
        pprint(result)
    except ClientError as e:
        print(e)

create_bucket('test-29387239734792333')