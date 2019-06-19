# バケット作成（例外処理を追加）

import boto3
from pprint import pprint
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')

try:
    result = s3.create_bucket(Bucket='test-2424323432', 
        CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-1'})
    pprint(result)
except ClientError as e:
    print(e)