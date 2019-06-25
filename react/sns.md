バケット

- アップされたらSNSトピックに通知
- CORS設定

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

SNSをトリガーとするSAM関数

```
Resources:
  HelloFunction:
    Type: AWS::Serverless::Function
    Properties:
      Events:
        PhotoUpload:
          Type: SNS
          Properties:
            Topic: !ImportValue MyTopicArn

```

SAM関数でSNSメッセージからS3イベントを取り出す例

```
def lambda_handler(event, context):
    pprint('***')
    pprint(event)
    for record in event['Records']:
        s3event = json.loads(record['Sns']['Message'])
        pprint('***')
        pprint(s3event)
        for s3record in s3event['Records']:
            bucket = s3record['s3']['bucket']['name']
            key = s3record['s3']['object']['key']
            pprint('***')
            pprint(bucket)
            pprint('***')
            pprint(key)
            
```
