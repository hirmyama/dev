DynamoDBテーブル`images`を作成。パーティションキー: `key`

```
sam init --runtime python3.6 --name list-images
cd list-images
```

template.yamlを一部書き換え
```
Globals:
  Api:
    # Corsを追加
    Cors:
      AllowMethods: "'*'"
      AllowHeaders: "'*'"
      AllowOrigin: "'*'"
      AllowCredentials: "'true'"

Resources:
  HelloWorldFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: hello_world/
      Handler: app.lambda_handler
      Runtime: python3.6
      # ポリシーを追加
      Policies:
        - AmazonDynamoDBReadOnlyAccess
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get
```

hello_world/app.pyを次のように変更

```
import json
import boto3

dynamodb = boto3.resource('dynamodb')
def lambda_handler(event, context):
    items = dynamodb.Table('images').scan()['Items']

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(items, ensure_ascii=False)
    }
```
