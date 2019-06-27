# S3バケットの作成

「開発サーバー」を停止(Ctrl+C)

Cloud9のenvironmentの中に`PhotoBucket`フォルダを作成する。

また、PhotoBucket内部に、CloudFormationが使用するtemplate.ymlを作成する

```
$ mkdir ~/environment/PhotoBucket
$ touch ~/environment/PhotoBucket/template.yml
```

注意：作成したフォルダやファイルがCloud9画面左のファイル一覧に反映されない場合は、最上位のenvironmentをダブルクリックで開閉する。

template.ymlを開き、以下を記入

```
Resources:
  PhotoBucket:
    Type: AWS::S3::Bucket
    Properties:
      CorsConfiguration:
        CorsRules:
          - AllowedOrigins: [ '*' ]
            AllowedHeaders: [ '*' ]
            AllowedMethods: [ HEAD, GET, PUT, POST, DELETE ]
            ExposedHeaders:
              - x-amz-server-side-encryption
              - x-amz-request-id
              - x-amz-id-2
            MaxAge: 3000
      NotificationConfiguration:
        TopicConfigurations:
          - Event: 's3:ObjectCreated:*'
            Topic: !Ref MyTopic
  MyTopic:
    Type: AWS::SNS::Topic

  ProcessUploadTopicPolicy:
    Type: AWS::SNS::TopicPolicy
    Properties:
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
        - Sid: AllowUploadBucketToPushNotificationEffect
          Effect: Allow
          Principal:
            Service: s3.amazonaws.com
          Action: sns:Publish
          Resource: "*"
      Topics: 
       - !Ref MyTopic
Outputs:
  MyTopic:
    Value: !Ref MyTopic
    Export:
      Name: MyTopicArn
```

ファイルを保存する。

CloudFormationを使用してバケットを作成する
```
$ aws cloudformation create-stack --template-body file://~/environment/PhotoBucket/template.yml --stack-name photo-bucket

```
スタックの作成の完了を待つ（下記コマンドを打ち込むとしばらく待機状態になる。次の`$`が表示されてコマンドが打ち込める状態になるまで待つ）
```
$ aws cloudformation wait stack-create-complete --stack-name photo-bucket
```

