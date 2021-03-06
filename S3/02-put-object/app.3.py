# オブジェクトのPut（サーバーサイド暗号化）

import boto3
from pprint import pprint

s3 = boto3.resource('s3')

bucket = s3.Bucket('test-223293879278334')
result = bucket.put_object(
    Key='hello.txt', 
    Body='こんにちは', 
    ContentType='text/plain;charset=utf-8', 
    ServerSideEncryption='AES256')

pprint(result)