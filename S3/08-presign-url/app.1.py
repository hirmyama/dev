# 署名付きURL

import boto3
from pprint import pprint
import os
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')

bucket_name = 'presign-923874792433233'
key = 'test.txt'

try:
    bucket = s3.create_bucket(Bucket=bucket_name, 
        CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-1'})
except ClientError as err:
    pass

body = '''このオブジェクトは公開に設定されていませんが、
Presigned URL（署名付きURL）を使用すれば、指定された期限まではアクセスできます'''

object = s3.Object(bucket_name, key).put(Body=body, ContentType='text/plain;charset=utf-8')

url = s3.meta.client.generate_presigned_url(
    ClientMethod='get_object', 
    Params={'Bucket': bucket_name, 'Key': key}, 
    ExpiresIn=60, 
    HttpMethod='GET'
)

print(url)
