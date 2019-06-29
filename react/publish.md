# 一般公開

公開用のバケットを作る。

質問はすべてエンターで進める。

```
$ cd ../myapp
$ amplify hosting add
? Select the environment setup: DEV (S3 only with HTTP)
? hosting bucket name myapp-20190627042100-hostingbucket
? index doc for the website index.html
? error doc for the website index.html
```

公開する

```
$ amplify publish

Current Environment: dev

| Category | Resource name   | Operation | Provider plugin   |
| -------- | --------------- | --------- | ----------------- |
| Hosting  | S3AndCloudFront | Create    | awscloudformation |
| Auth     | myapp4d066d9c   | No Change | awscloudformation |
? Are you sure you want to continue? Yes
```

下記のようなURLが表示される。スマホ等でアクセスしてみよう。

```
Your app is published successfully.
http://myapp-20190627042100-hostingbucket-dev.s3-website-ap-northeast-1.amazonaws.com
```

