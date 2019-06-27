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

スタックの作成の完了を待つ（下記コマンドを打ち込むとしばらく待機状態になる。次の$が表示されてコマンドが打ち込める状態になるまで待つ）
```
$ aws cloudformation wait stack-create-complete --stack-name $STACK_NAME
```

作成されたAPIのURLを確認する。
```
$ aws cloudformation describe-stacks --stack-name $STACK_NAME --query 'Stacks[].Outputs[]'
[
    {
        "Description": "Implicit IAM Role created for Hello World function", 
        "OutputKey": "HelloWorldFunctionIamRole", 
        "OutputValue": "arn:aws:iam::328243927296:role/list-images-HelloWorldFunctionRole-12XND8Z3FN6W0"
    }, 
    {
        "Description": "API Gateway endpoint URL for Prod stage for Hello World function", 
        "OutputKey": "HelloWorldApi", 
        "OutputValue": "https://6q5iyrihae.execute-api.ap-northeast-1.amazonaws.com/Prod/hello/"
    }, 
    {
        "Description": "Hello World Lambda Function ARN", 
        "OutputKey": "HelloWorldFunction", 
        "OutputValue": "arn:aws:lambda:ap-northeast-1:328243927296:function:list-images-HelloWorldFunction-1SJF79FIQSBGB"
    }
]
```
上記出力中の中央部分に、`https://`で始まるURLがある。

URLをクリックして、`Open`を選択すると、別タブでそのURLが開かれる。アップロードされた画像の情報をJSON形式で取得することができる。
