# ファイルのマルチパートアップロード
# 通常、オブジェクトサイズが 100 MB 以上の場合に使用。

# 参照: https://aws.amazon.com/jp/premiumsupport/knowledge-center/s3-multipart-upload-cli/
# 参照: https://gist.github.com/teasherm/bb73f21ed2f3b46bc1c2ca48ec2c1cf5
# 参照: https://docs.aws.amazon.com/cli/latest/topic/s3-config.html

import boto3
from pprint import pprint
import os

s3 = boto3.resource('s3')
s3client = s3.meta.client

bucket_name = 'test-223293879278334'
key = 'bigfile.txt'

upload = s3client.create_multipart_upload(Bucket=bucket_name, Key=key)
upload_id = upload['UploadId']

print('part1のデータを作成しています(各パートは約84MBの文字列です)')
body1 = str(list(range(10000000))) 
print('part2のデータを作成しています')
body2 = str(list(range(10000000)))
print('part3のデータを作成しています')
body3 = str(list(range(10000000)))

print('part1 をアップロードしています...');
part1 = s3client.upload_part(Bucket=bucket_name, Key=key, UploadId=upload_id, Body=body1, PartNumber=1)
print('part2 をアップロードしています...');
part2 = s3client.upload_part(Bucket=bucket_name, Key=key, UploadId=upload_id, Body=body2, PartNumber=2)
print('part3 をアップロードしています...');
part3 = s3client.upload_part(Bucket=bucket_name, Key=key, UploadId=upload_id, Body=body3, PartNumber=3)


parts = [
    {"PartNumber": 1, "ETag": part1["ETag"]},
    {"PartNumber": 2, "ETag": part2["ETag"]},
    {"PartNumber": 3, "ETag": part3["ETag"]},
]
print('各パートのETag（エンティティタグ）')
pprint(parts)

print('結合しています...')
result = s3client.complete_multipart_upload(
    Bucket=bucket_name, 
    Key=key, 
    UploadId=upload_id, 
    MultipartUpload={'Parts': parts}
)

pprint(result)
print('完了')
