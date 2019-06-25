```
sam init --runtime python3.6 --name tag-image
cd tag-image
```

`template.yaml`

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
          Type: S3
          Properties:
            Bucket: !Ref PhotoBucket
            Events: s3:ObjectCreated:*
  PhotoBucket:
    Type: AWS::S3::Bucket
  ImageTable:
    Type: AWS::DynamoDB::Table
    Properties:
      KeySchema:
        - AttributeName: ObjectKey
          KeyType: HASH
        - AttributeName: EventTime
          KeyType: RANGE
      AttributeDefinitions:
        - AttributeName: ObjectKey
          AttributeType: S
        - AttributeName: EventTime
          AttributeType: S
      ProvisionedThroughput:
        ReadCapacityUnits: 20
        WriteCapacityUnits: 10
```

hello_world/app.py

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
        event_time = record['eventTime']
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        labels = detect_labels(bucket, key)
        labels_str = ' '.join(['#' + label.replace('[', '').replace(']', '') for label in labels])
        table_name = os.environ.get('TABLE_NAME')
        dynamodb.Table(table_name).put_item(Item={'ObjectKey': key, 'EventTime': event_time, 'Tags': labels_str})
    return {
        'statusCode': 200,
        'body': json.dumps(labels)
    }
```

ビルドとデプロイ
```
STACK_NAME='tag-image'
CURRENT_DATETIME=`date +'%Y%m%d%H%M%S'`
DEPLOY_BUCKET="$STACK_NAME-$CURRENT_DATETIME"

aws s3 mb s3://$DEPLOY_BUCKET

sam build
sam package --output-template-file packaged.yaml --s3-bucket $DEPLOY_BUCKET
sam deploy --template-file packaged.yaml --stack-name $STACK_NAME --capabilities CAPABILITY_IAM
```
