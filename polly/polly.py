# Lambda関数 (Python 3.7)用
# 「#」以降はコメントなので、打ち込む必要はありません。

import boto3
import os
from contextlib import closing

# PollyとS3を操作するためのオブジェクトを生成。
# 「実行コンテキスト」（Lambda関数を実行する「コンテナ」）が
# 生きている間は、これらのグローバル変数も生き残り、再利用される。
polly = boto3.client('polly')  # PollyはクライアントAPIのみ使用可能。
s3 = boto3.resource('s3')  # S3はリソースAPIを使用可能。

def lambda_handler(event, context):
    # 音声にするテキストをクエリパラメータ(...?text=hello)から取得
    text = event['queryStringParameters']['text']
    # Lambda環境変数からバケット名を取得
    bucket_name = os.environ['MP3_BUCKET_NAME']
    # 音声のファイル名
    file_name = 'test.mp3'

    # テキストを音声（mp3）化。
    response = polly.synthesize_speech(
        OutputFormat='mp3', Text = text,
        VoiceId = 'Mizuki'  # or 'Takumi'
    )

    # 音声ファイルをLambda関数のテンポラリディスク（/tmp）に保存
    if 'AudioStream' in response:
        with closing(response['AudioStream']) as stream:
            output = os.path.join('/tmp/', file_name)
            with open(output, 'wb') as file:
                file.write(stream.read())

    # 音声ファイルファイルをS3バケットにアップロード
    s3.Bucket(bucket_name).upload_file(output, file_name)

    # 音声ファイル（S3オブジェクト）の署名付きURLを生成。
    url = s3.meta.client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': file_name},
        ExpiresIn=3600,  # 1時間(3600秒)有効
        HttpMethod='GET'  # GETリクエストを許可
    )

    # レスポンスを返す
    return {'statusCode': 200, 'body': url}
