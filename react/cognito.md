
# Cognitoによる認証(auth)を追加

https://aws.amazon.com/jp/cognito/

> Cognito を使用すれば、ウェブアプリケーションおよびモバイルアプリに
> 素早く簡単にユーザーのサインアップ/サインインおよびアクセスコントロールの機能を追加できます。

## 認証機能の追加

質問はすべてエンターキーで進めてよい

```
$ amplify auth add
  Do you want to use the default authentication and security configuration? Default configuration
  How do you want users to be able to sign in when using your Cognito User Pool? Username
  What attributes are required for signing up? Email

$ amplify push
? Are you sure you want to continue? (Y/n) Yes
```

`myapp/src/App.js`のimportとfunctionの間に以下を追記

```
import Amplify from 'aws-amplify';
import { withAuthenticator } from 'aws-amplify-react';
import awsconfig from './aws-exports';
Amplify.configure(awsconfig);
```

`myapp/src/App.js`の末尾の`export default App;`部分を以下のように書き換え

```
// export default App;
export default withAuthenticator(App, {includeGreetings: true});
```

開発サーバーを起動

```
$ yarn start
```

Preview > Preview Running Applicationでプレビューする

Cognitoによるログイン画面が表示される。

## メールアドレスの準備

開発用の一時的なメールアドレスは https://temp-mail.org/ja/ で入手できる。

表示されたメールアドレスをコピーしておく。

## 会員登録（サインアップ）

`Create account`をクリック

Username: `yamada`

Password: `Yamada3!`

Email: (メールアドレスをペースト)

Phone Number: `123`

[Create Account]

上記で入力したメールアドレスに、
`Your verification code is 815481`といったメールが送信される。
数字の部分（認証コード）をコピー

Confirmation Code: (認証コードを貼り付け)

[Confirm]

## ログイン（サインイン）

Username: `yamada`

Password: `Yamada3!`

[Sign in]

以上でWebアプリにログインすることができる。画面右上のボタンでログアウトできる。
