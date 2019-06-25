https://github.com/awslabs/serverless-application-model

https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md

```sh

sudo pip install --upgrade aws-sam-cli

sam --version

sam init --runtime python3.6 --name myapp

cd myapp

# 主なファイル: 
# myapp/template.yaml ... テンプレートファイル。
# myapp/hello_world/app.py ... Lambda関数のコード
# myapp/hello_world/requirements.txt ... Lambda関数の依存関係

# package.yamlの検証
sam validate

# ビルドする。myapp/.aws-samディレクトリが作られる。
sam build

# サンプルイベントを生成
sam local generate-event s3 put > event.json

# ローカルで関数を実行。
#「lambci/lambda:python3.6」というDocker Imageから作られたコンテナ内で実行される。
sam local invoke --no-event
sam local invoke --event event.json
sam local generate-event s3 put | sam local invoke

# パッケージ用のバケットを作成。バケット名は適宜変更してください
aws s3 mb s3://deploy-1234

# packageにより、指定したバケットにリソースがアップロードされる。
# また、packaged.yamlに、template.yamlの内容が転記される。
# このときCodeUriがローカルからS3のパスに変更される。
sam package --s3-bucket deploy-1234 --output-template-file packaged.yaml  

# deployにより、Lambda関数、API Gateway、IAMロールが作られる。
sam deploy --template-file packaged.yaml --stack-name stack1 --capabilities CAPABILITY_IAM  

# ログを表示
sam logs -n HelloFunction --stack-name stack1
sam logs -n HelloFunction --stack-name stack1 --tail


```
コード例
```
import json
import boto3
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
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        labels = detect_labels(bucket, key)
        labels_str = ' '.join(['#' + label.replace('[', '').replace(']', '') for label in labels])
        dynamodb.Table('images').put_item(Item={'key': key, 'labels': labels_str})
    return {
        'statusCode': 200,
        'body': json.dumps(labels, ensure_ascii=False)
}
```

テンプレート例1: HelloWorld
```
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: myapp

Resources:
  HelloFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: hello/
      Handler: hello.lambda_handler
      Runtime: python3.6
```

テンプレート例2: S3との連動
```
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: myapp

Resources:
  HelloFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: hello/
      Handler: hello.lambda_handler
      Runtime: python3.6
      Events:
        PhotoUpload:
          Type: S3
          Properties:
            Bucket: !Ref PhotoBucket
            Events: s3:ObjectCreated:*
  PhotoBucket:
    Type: AWS::S3::Bucket
```

テンプレート例3: S3, DynamoDB連携。画像を認識して「#猫」といったハッシュタグをつける
```
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: myapp

Resources:
  HelloFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: hello/
      Handler: hello.lambda_handler
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
      TableName: images
      KeySchema:
        - AttributeName: key
          KeyType: HASH
      AttributeDefinitions:
        - AttributeName: key
          AttributeType: S
      ProvisionedThroughput:
        ReadCapacityUnits: 5
        WriteCapacityUnits: 5   
```

