# オブジェクトをGetし、内容を表示

import boto3
from pprint import pprint

s3 = boto3.resource('s3')

bucket = s3.Bucket('test-223293879278334')
body = bucket.Object('hello.txt').get()['Body']
pprint(body)

bytes = body.read()
pprint(bytes)

pprint(bytes.decode())
