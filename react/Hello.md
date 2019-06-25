# SAM(API Gateway + Lambda) + Amplify API (REST)

```
sam init --runtime python3.6 --name hello
cd hello
```

`template.yaml`

```
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: >
  mybackend

  Sample SAM Template for mybackend

# More info about Globals: https://github.com/awslabs/serverless-application-model/blob/master/docs/globals.rst
Globals:
  Function:
    Timeout: 3
  Api:
    # Allows an application running locally on port 8080 to call this API
    Cors:
      AllowMethods: "'OPTIONS,POST,GET'"
      AllowHeaders: "'authorization,x-amz-date,x-amz-security-token'"
      AllowOrigin: "'*'"
Resources:
  HelloWorldFunction:
    Type: AWS::Serverless::Function # More info about Function Resource: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
    Properties:
      CodeUri: hello_world/
      Handler: app.lambda_handler
      Runtime: python3.6
      Events:
        HelloWorld:
          Type: Api # More info about API Event Source: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
          Properties:
            Path: /hello
            Method: get

Outputs:
  # ServerlessRestApi is an implicit API created out of Events key under Serverless::Function
  # Find out more about other implicit resources you can reference within SAM
  # https://github.com/awslabs/serverless-application-model/blob/master/docs/internals/generated_resources.rst#api
  HelloWorldApi:
    Description: "API Gateway endpoint URL for Prod stage for Hello World function"
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/hello/"
  HelloWorldFunction:
    Description: "Hello World Lambda Function ARN"
    Value: !GetAtt HelloWorldFunction.Arn
  HelloWorldFunctionIamRole:
    Description: "Implicit IAM Role created for Hello World function"
    Value: !GetAtt HelloWorldFunctionRole.Arn

```

`app.py`

```
import json

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    return {
        "statusCode": 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "authorization,x-amz-date,x-amz-security-token",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
```

ビルドとデプロイ
```
sam build
DEPLOY_BUCKET=`date +'deploy-%Y%m%d%H%M%S'`
aws s3 mb s3://$DEPLOY_BUCKET
sam package --output-template-file packaged.yaml --s3-bucket $DEPLOY_BUCKET
sam deploy --template-file packaged.yaml --stack-name stack1 --capabilities CAPABILITY_IAM 
```

Reactコンポーネント `Hello.js`

```
import React from 'react';
import Amplify from 'aws-amplify';
import { API } from 'aws-amplify';

Amplify.configure({
  API: {
    endpoints: [
      {
        name: "Hello",
        endpoint: "https://g2yjtqgv7j.execute-api.ap-northeast-1.amazonaws.com/Prod/hello/"
      },
    ]
  }
});

class Hello extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      message: null
    };
    API.get("Hello", "")
    .then(response => {
      this.setState({message: response.message});
    });
  }
  render() {
    if (this.state.message == null) {
      return <div>loading...</div>;
    } else {
      return <div>{this.state.message}</div>;
    }
  }
}

export default Hello;
```

描画部分

```
...

function App() {
  return (
    <div className="App">
      <Hello />
      <header className="App-header">

...
```
