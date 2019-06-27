# 使用するソフトウェアの概要

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


# 使用するコマンドの最新化

以下、Cloud9環境のTerminal(bash)内で実行。「$」以降から行末までをコピー・ペーストして実行する。

下記の実行例よりも新しいバージョン番号が表示される場合があるが問題ない。

## AWS CLI
```
$ aws --version
aws-cli/1.16.169 Python/2.7.16 Linux/4.14.121-85.96.amzn1.x86_64 botocore/1.12.159

$ sudo pip install --upgrade awscli

$ aws --version
aws-cli/1.16.184 Python/2.7.16 Linux/4.14.121-85.96.amzn1.x86_64 botocore/1.12.174
```

注意：このとき`You should consider upgrading via the 'pip install --upgrade pip' command.`と表示されるが、pipのupgradeは実行しないこと。

## npm

```
$ npm --version
6.4.1

$ npm install -g npm

$ npm --version
6.9.0
```

## yarn

```
$ curl --silent --location https://dl.yarnpkg.com/rpm/yarn.repo | sudo tee /etc/yum.repos.d/yarn.repo

$ sudo yum install -y yarn

$ yarn --version
1.16.0
```

## yarn global addでインストールされたアプリケーションを起動できるようにする

https://yarnpkg.com/en/docs/cli/global
Adding the install location to your PATH

```
$ echo 'export PATH="$PATH:$(yarn global bin)"' >> ~/.bash_profile

$ bash -l
```

## create-react-app
```
$ yarn global add create-react-app

$ create-react-app --version
3.0.1
```
