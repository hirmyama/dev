# オブジェクトのGet

import boto3
from pprint import pprint

s3 = boto3.resource('s3')

bucket = s3.Bucket('test-223293879278334')
result = bucket.Object('hello.txt').get()

pprint(result)