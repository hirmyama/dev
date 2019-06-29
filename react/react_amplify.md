# React Webアプリケーションの作成

## create-react-appコマンドによるReactアプリの作成

https://github.com/facebook/create-react-app

```
$ cd ~/environment

$ create-react-app myapp

$ cd myapp
```
「開発サーバー」を使用して、Webアプリケーションを起動する

```
$ yarn start
```

- Cloud9のメニュー ＞ Preview ＞ Preview Running Application でプレビューできる
- 「開発サーバー」を`Ctrl + C` (`Control`キーを押しながら`C`を押す)で止める

## WebアプリケーションにAmplifyを導入

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

