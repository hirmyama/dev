# S3 Select

import boto3
from pprint import pprint
import os
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')

bucket_name = 'select-923874792433233'
key = 'data.csv'

try:
    bucket = s3.create_bucket(Bucket=bucket_name, 
        CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-1'})
except ClientError as err:
    pass

object = s3.Object(bucket_name, key)
# このスクリプトファイルと同じディレクトリにあるdata.csvのフルパス
path = os.path.dirname(os.path.abspath(__file__)) + '/' + key
object.upload_file(Filename=path, ExtraArgs={'ContentType': 'text/plain;charset=utf-8'})

expression = 'select * from S3Object s'
# expression = 'select s.name from S3Object s'
# expression = "select s.price from S3Object s where s.id = '2'"
# expression = 'select avg(cast(s.price as int)) from S3Object s'

result = s3.meta.client.select_object_content(
    Bucket=bucket_name,
    Key=key,
    ExpressionType='SQL',
    Expression=expression,
    InputSerialization={'CSV': {
        'FileHeaderInfo': 'Use'
    }},
    OutputSerialization={'CSV': {}}
)

for event in result['Payload']:
    pprint(event)