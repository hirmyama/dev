# 画像一覧機能の作成

## AppSyncのセットアップ

サービス＞AWS AppSync

[Create API]

[Import DynamoDB table]を選択（右上の丸をクリック）,その右上の[Start]をクリック

Table name: TODO, [Import]

[Add Field]をクリックし、Name: `EventTime` と入力。その他はデフォルトのまま。

[Add Field]をクリックし、Name: `Tags` と入力。その他はデフォルトのまま。

[Create], [Create]

Your API is almost ready...と表示される。10秒ほど待つ。

[My AppSync App]

`Integrate with your app`の`JavaScript`をクリック

`amplify add codegen --apiId do7xqd2xmjfhdozj7exsta77r4`のようなものが書かれたテキストボックスの右側の[Copy]をクリック

## AppSyncを使用するようにWebアプリケーションをセットアップ

上記手順でコピーしたコマンドをターミナルに貼り付けて実行。

すべてエンターキーで進めてよい。

```
$ amplify add codegen --apiId do7xqd2xmjfhdozj7exsta77r4
✔ Getting API details
Successfully added API My AppSync App to your Amplify project
? Choose the code generation language target javascript
? Enter the file name pattern of graphql queries, mutations and subscriptions src/graphql/**/*.js
? Do you want to generate/update all possible GraphQL operations - queries, mutations and subscriptions Yes
? Enter maximum statement depth [increase from default if your schema is deeply nested] 2
✔ Downloaded the schema
✔ Generated GraphQL operations successfully and saved at src/graphql
```

