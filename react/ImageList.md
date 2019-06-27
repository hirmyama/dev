# 画像情報を取得するAPIの作成


## プロジェクトを作成
```
cd ~/environment
sam init --runtime python3.6 --name ListImages
cd ListImages
```

`template.yaml` を開き、中身を下記に置き換える

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

ファイルを保存。

hello_world/app.py を開き、中身を下記に置き換える

注意：imagesの部分は、前工程で生成されたDynamoDBテーブル名にする

```
import json
import boto3

dynamodb = boto3.resource('dynamodb')
def lambda_handler(event, context):
    image_table = 'tag-image-ImageTable-1RVWX4MZLSBNP' // DynamoDBのテーブル名を''内に記入
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
ファイルを保存する。

デプロイ用のバケットを作成する
```
$ STACK_NAME='list-images'
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

