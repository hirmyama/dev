import boto3
# バケット作成（Block Public Accessを有効化。バケット内のオブジェクトをpublicに設定できなくなる）

from pprint import pprint

s3 = boto3.resource('s3')

bucket_name = 'private-92387927483273'

bucket = s3.create_bucket(
    Bucket=bucket_name, 
    CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-1'}
)

response = s3.meta.client.put_public_access_block(
    Bucket=bucket_name,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': True,
        'RestrictPublicBuckets': True
    }
)
