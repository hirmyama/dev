DynamoDBテーブル`images`を作成。パーティションキー: `key`

```
sam init --runtime python3.6 --name list-images
cd list-images
```

template.yamlを一部書き換え
```
Globals:
  Api:
    Cors:
      AllowMethods: "'OPTIONS,POST,GET'"
      AllowHeaders: "'authorization,x-amz-date,x-amz-security-token'"
      AllowOrigin: "'*'"

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
            "Content-Type": "text/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(items, ensure_ascii=False)
    }
```

```
STACK_NAME='list-images'
CURRENT_DATETIME=`date +'%Y%m%d%H%M%S'`
DEPLOY_BUCKET="$STACK_NAME-$CURRENT_DATETIME"

aws s3 mb s3://$DEPLOY_BUCKET

sam build
sam package --output-template-file packaged.yaml --s3-bucket $DEPLOY_BUCKET
sam deploy --template-file packaged.yaml --stack-name $STACK_NAME --capabilities CAPABILITY_IAM
```

