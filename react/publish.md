

```
$ amplify hosting add
? Select the environment setup: DEV (S3 only with HTTP)
? hosting bucket name myapp-20190627042100-hostingbucket
? index doc for the website index.html
? error doc for the website index.html
```


```
$ amplify publish

Current Environment: dev

| Category | Resource name   | Operation | Provider plugin   |
| -------- | --------------- | --------- | ----------------- |
| Hosting  | S3AndCloudFront | Create    | awscloudformation |
| Auth     | myapp4d066d9c   | No Change | awscloudformation |
? Are you sure you want to continue? Yes
```
