# React Webアプリケーションの作成

## create-react-appコマンドによるReactアプリの作成

参考: https://github.com/facebook/create-react-app

```
$ yarn global add create-react-app

$ create-react-app myapp

$ cd myapp
```
「開発サーバー」を使用して、Webアプリケーションを起動する

```
$ yarn start
```

- Cloud9のメニュー ＞ Preview ＞ Preview Running Application でプレビューできる
- 「開発サーバー」を`Ctrl + C` (`Control`キーを押しながら`C`を押す)で止める

## AWS Amplifyの導入

https://aws-amplify.github.io/docs/cli/init

```
$ yarn add aws-amplify aws-amplify-react

```

## Amplifyのセットアップ

下記の「:」以下を入力または選択する。

2つ目の質問(environment)のみ`dev`と入力し、その他はすべてエンターキーで進めてよい。

```
$ amplify init
  ? Enter a name for the project: myapp
  ? Enter a name for the environment: dev
  ? Choose your default editor: None
  ? Choose the type of app that you're building: javascript
  ? What javascript framework are you using: react
  ? Source Directory Path: src
  ? Distribution Directory Path: build
  ? Build Command:  npm run-script build
  ? Start Command: npm run-script start
  ? Do you want to use an AWS profile? : Yes
  ? Please choose the profile you want to use: default
```

## Cognitoによる認証(auth)を追加

```
$ amplify auth add
  Do you want to use the default authentication and security configuration? Default configuration
  How do you want users to be able to sign in when using your Cognito User Pool? Username
  What attributes are required for signing up? Email

$ amplify push
```

`myapp/src/App.js`のimportとfunctionの間に以下を追記

```
import Amplify from 'aws-amplify';
import { withAuthenticator } from 'aws-amplify-react';
import awsconfig from './aws-exports';
Amplify.configure(awsconfig);
```

`myapp/src/App.js`の末尾のexport文を以下のように書き換え

```
export default withAuthenticator(App, {includeGreetings: true});
```

プレビュー

```
$ yarn start
# Preview > Preview Running Applicationでプレビューする
```

Cognitoによるログイン画面が表示される。

## 会員登録（サインアップ）

`Create account`をクリック

Username: `yamada`

Password: `Yamada3!`

Email: (実際に受信できるメールアドレスを入力。temp mailなどで作成できる)

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

