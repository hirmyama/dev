# React + Amplify (Cognito認証)



React: Facebook社によるJavaScriptフレームワーク
https://ja.reactjs.org/

AWS Amplify: モバイルアプリ/Webアプリ開発のフレームワーク
https://aws.amazon.com/jp/amplify/

Amplify CLI: Amplifyをコマンドから操作
https://github.com/aws-amplify/amplify-cli

Amazon Cognito: サインアップ・サインイン管理、アクセス権限管理
https://aws.amazon.com/jp/cognito/

npm: Node Package Manager
https://www.npmjs.com/

Yarn: Facebook社による依存性管理 / 開発用コマンド実行ツール
https://yarnpkg.com/lang/ja/



## コマンドの最新化

以下、Cloud9環境のTerminal内で実行。「$」以降から行末までを実行する。

下記の実行例よりも新しいバージョン番号が表示される場合があるが問題ない。

```
$ aws --version
aws-cli/1.16.169 Python/2.7.16 Linux/4.14.121-85.96.amzn1.x86_64 botocore/1.12.159

$ sudo pip install --upgrade awscli

$ aws --version
aws-cli/1.16.184 Python/2.7.16 Linux/4.14.121-85.96.amzn1.x86_64 botocore/1.12.174

$ npm --version
6.4.1

$ npm install -g npm

$ npm --version
6.9.0

$ npm install -g yarn

$ yarn --version
1.16.0
```

yarn global addでインストールされたアプリケーションを起動できるようにする
https://yarnpkg.com/en/docs/cli/global
Adding the install location to your PATH

```
$ echo 'export PATH="$(yarn global bin):$PATH"'>>~/.bashrc 
$ exec $SHELL -l
```

## create-react-appコマンドによるReactアプリの作成

```
# https://github.com/facebook/create-react-app
$ yarn global add create-react-app

$ create-react-app myapp
$ cd myapp

$ yarn start

# Preview > Preview Running Applicationでプレビューする
# Ctrl + C で止める

```

## AWS Amplifyの導入

```
$ yarn add aws-amplify aws-amplify-react

# Amplify CLI
# ちなみに @ がついているのは NPM の 'scoped packages'
$ yarn global add @aws-amplify/cli

# amplify initを実行する前にdefault のプロファイルのcredentialsとconfigを作る
# https://github.com/aws-amplify/amplify-cli/issues/1138
# 具体的には、cloud9の中では、aws configureを実行し、outputをjsonにセットすればよい
$ aws configure set default.region ap-northeast-1
$ aws configure set default.output json

# https://aws-amplify.github.io/docs/cli/init

# 下記の「:」以下を入力または選択する。
# デフォルト値が()内に表示され、それを使用する場合はEnterで進める。

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
import Amplify, { Auth } from 'aws-amplify';
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

