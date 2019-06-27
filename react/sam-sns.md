
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
