https://github.com/awslabs/serverless-application-model

https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md

```sh
sudo pip install --upgrade pip
sudo pip install --upgrade aws-sam-cli

sam --version

sam init --runtime python3.6 --name myapp

cd myapp

# 主なファイル: 
# myapp/template.yaml ... テンプレートファイル。
# myapp/hello_world/app.py ... Lambda関数のコード
# myapp/hello_world/requirements.txt ... Lambda関数の依存関係

# ビルドする。myapp/.aws-samディレクトリが作られる。
sam build

# ローカルで関数を実行。
#「lambci/lambda:python3.6」というDocker Imageから作られたコンテナ内で実行される。
sam local invoke --no-event

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

