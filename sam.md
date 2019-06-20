```sh
sudo pip install --update aws-sam-cli

sam --version

sam init --runtime python3.6 --name myapp

cd myapp

# myapp/hello_world/app.pyを確認（編集）

sam build

aws s3 mb s3://deploy-123456

sam package --s3-bucket deploy-123456 --output-template-file packaged.yml   

sam deploy --template-file packaged.yml --stack-name stack1 --capabilities CAPABILITY_IAM  
```

