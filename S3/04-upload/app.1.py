# ファイルのアップロード

import boto3
from pprint import pprint
import os

s3 = boto3.resource('s3')

object = s3.Object('test-223293879278334', 'test.txt')
# このスクリプトファイルと同じディレクトリにあるtest.txtのフルパス
path = os.path.dirname(os.path.abspath(__file__)) + '/test.txt'
result = object.upload_file(Filename=path, ExtraArgs={'ContentType': 'text/plain;charset=utf-8'})

pprint(result)