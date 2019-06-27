
S3 Corsの設定

```
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>HEAD</AllowedMethod>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedMethod>PUT</AllowedMethod>
    <AllowedMethod>POST</AllowedMethod>
    <AllowedMethod>DELETE</AllowedMethod>
    <MaxAgeSeconds>3000</MaxAgeSeconds>
    <ExposeHeader>x-amz-server-side-encryption</ExposeHeader>
    <ExposeHeader>x-amz-request-id</ExposeHeader>
    <ExposeHeader>x-amz-id-2</ExposeHeader>
    <ExposeHeader>ETag</ExposeHeader>
    <AllowedHeader>*</AllowedHeader>
</CORSRule>
</CORSConfiguration>
```

Cloud9ではAWS managed temporary credentialsを使用する。この権限ではIAMの一部の操作が制限される。

```
AUTH_ROLE_ARN=$(aws iam list-roles --query 'Roles[?contains(to_string(RoleName),`-authRole`)].RoleName' --output text)
```

# マネジメントコンソール側でDynamoDBテーブル、AppSync APIを作成した場合

codegenを実行する。

## DynamoDBテーブルを作成
images
キー: id

## AppSync APIを作成
My AppSync App

## Amplifyプロジェクトを作成
create-react-app myimageapp
cd myimageapp
yarn add aws-amplify aws-amplify-react
amplify init

## この時点でのstatus
$ amplify status

Current Environment: dev

| Category | Resource name | Operation | Provider plugin |
| -------- | ------------- | --------- | --------------- |


## AppSyncのページ内の記述よりコマンドをコピーして、実行
amplify add codegen --apiId uii3atc3q5cz7cphxxf3g4htga

src以下にaws-exports.js、graphql/*.js が作成される

## status
$ amplify status

Current Environment: dev

| Category | Resource name  | Operation | Provider plugin |
| -------- | -------------- | --------- | --------------- |
| Api      | My AppSync App | No Change |                 |

GraphQL endpoint: https://wos3hh6gk5hvbkfknqmwfemea4.appsync-api.ap-northeast-1.amazonaws.com/graphql
GraphQL API KEY: da2-mikpdi4dy5a3xcywq6frnojqma


Apiカテゴリが追加されているのが確認できる

pushも必要ない。


## GraphQL statements の自動生成

https://aws-amplify.github.io/docs/js/api#query-declarations

The Amplify CLI codegen automatically generates all possible GraphQL statements 
(queries, mutations and subscriptions) and for JavaScript applications saves it in src/graphql folder


# プロジェクト内でadd apiした場合

```
$ amplify add api
? Please select from one of the below mentioned services GraphQL
? Provide API name: myimageapp2
? Choose an authorization type for the API API key
? Do you have an annotated GraphQL schema? No
? Do you want a guided schema creation? Yes
? What best describes your project: Single object with fields (e.g., “Todo” with ID, name, description)
? Do you want to edit the schema now? No

GraphQL schema compiled successfully.
Edit your schema at /home/ec2-user/environment/myimageapp2/amplify/backend/api/myimageapp2/schema.graphql or place .graphql files in a directory at /home/ec2-user/environment/myimageapp2/amplify/backend/api/myimageapp2/schema
Successfully added resource myimageapp2 locally

Some next steps:
"amplify push" will build all your local backend resources and provision it in the cloud
"amplify publish" will build all your local backend and frontend resources (if you have hosting category added) and provision it in the cloud

```

さらにpushしたときにcodegen するか聞いてくる。
```
$ amplify push

Current Environment: dev

| Category | Resource name | Operation | Provider plugin   |
| -------- | ------------- | --------- | ----------------- |
| Api      | myimageapp2   | Create    | awscloudformation |
? Are you sure you want to continue? Yes

GraphQL schema compiled successfully.
Edit your schema at /home/ec2-user/environment/myimageapp2/amplify/backend/api/myimageapp2/schema.graphql or place .graphql files in a directory at /home/ec2-user/environment/myimageapp2/amplify/backend/api/myimageapp2/schema
? Do you want to generate code for your newly created GraphQL API Yes
? Choose the code generation language target javascript
? Enter the file name pattern of graphql queries, mutations and subscriptions src/graphql/**/*.js
? Do you want to generate/update all possible GraphQL operations - queries, mutations and subscriptions Yes
? Enter maximum statement depth [increase from default if your schema is deeply nested] 2
⠦ Updating resources in the cloud. This may take a few minutes...
```

backendに、apiフォルダがある。
ここにschema.graphqlが入っている。
これをカスタマイズしてamplify pushすることができる。

https://aws-amplify.github.io/docs/js/api#updating-your-graphql-schema

# まとめ

存在するテーブル、AppSync APIがあるときはcodegen。
このときテーブルやAppSyncの管理はプロジェクトの対象外となる。

Amplifyに、テーブル、AppSync APIを作らせ、管理させる場合はadd apiとする。
amplify/backend/api/プロジェクト名/schema.graphqlに定義ファイルがあり、
Amplifyプロジェクト側からスキーマの更新ができる。

