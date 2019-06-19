import boto3
# バケット作成（クラス化）

from pprint import pprint
from botocore.exceptions import ClientError

class S3Util:
    s3 = boto3.resource('s3')
    def create_bucket(self, bucket_name, region='ap-northeast-1'):
        try:
            result = self.s3.create_bucket(Bucket=bucket_name, 
                CreateBucketConfiguration={'LocationConstraint': region})
            pprint(result)
        except ClientError as e:
            print(e)

util = S3Util()
util.create_bucket('test-2938729734d792333')