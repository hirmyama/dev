# 自動タグ付け機能の追加


Cloud9で操作する

開発サーバーをCtrl+Cで停止。

```
$ cd ~/environment
$ sam init --runtime python3.6 --name TagImage
$ cd TagImage
```

`template.yaml` を開き、中身を下記に置き換える

```
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: myapp

Resources:
  HelloFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: hello_world/
      Handler: app.lambda_handler
      Runtime: python3.6
      Timeout: 30
      Environment:
        Variables:
          TABLE_NAME: !Ref ImageTable
      Policies:
        - AmazonS3FullAccess
        - AmazonDynamoDBFullAccess
        - AmazonRekognitionFullAccess
        - TranslateFullAccess
        - AWSLambdaBasicExecutionRole
      Events:
        PhotoUpload:
          Type: SNS
          Properties:
            Topic: !ImportValue MyTopicArn
  PhotoBucket:
    Type: AWS::S3::Bucket
  ImageTable:
    Type: AWS::DynamoDB::Table
    Properties:
      KeySchema:
        - AttributeName: ObjectKey
          KeyType: HASH
      AttributeDefinitions:
        - AttributeName: ObjectKey
          AttributeType: S
      ProvisionedThroughput:
        ReadCapacityUnits: 20
        WriteCapacityUnits: 10
```
ファイルを保存。

hello_world/app.py を開き、中身を下記に置き換える

```
import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
rekognition = boto3.client('rekognition')
translate = boto3.client('translate')

def en_ja(text):
    return translate.translate_text(
        Text=text,
        SourceLanguageCode='en',
        TargetLanguageCode='ja'
    )['TranslatedText']

def detect_labels(bucket, key):
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        }
    )
    return [en_ja(label['Name']) for label in response['Labels']]

def lambda_handler(event, context):
    for record in event['Records']:
        s3event = json.loads(record['Sns']['Message'])
        for s3record in s3event['Records']:
            event_time = s3record['eventTime']
            bucket = s3record['s3']['bucket']['name']
            key = s3record['s3']['object']['key']
            labels = detect_labels(bucket, key)
            labels_str = ' '.join(['#' + label.replace('[', '').replace(']', '') for label in labels])
            table_name = os.environ.get('TABLE_NAME')
            dynamodb.Table(table_name).put_item(Item={'ObjectKey': key, 'EventTime': event_time, 'Tags': labels_str})
    return {
        'statusCode': 200,
        'body': json.dumps(labels)
    }
```

ファイルを保存する。

デプロイ用のバケットを作成する
```
$ STACK_NAME='tag-image'
$ CURRENT_DATETIME=`date +'%Y%m%d%H%M%S'`
$ DEPLOY_BUCKET="$STACK_NAME-$CURRENT_DATETIME"
$ aws s3 mb s3://$DEPLOY_BUCKET
```

ビルドする
```
$ sam build
```
パッケージ化する
```
$ sam package --output-template-file packaged.yaml --s3-bucket $DEPLOY_BUCKET
```
デプロイする
```
$ sam deploy --template-file packaged.yaml --stack-name $STACK_NAME --capabilities CAPABILITY_IAM
```
