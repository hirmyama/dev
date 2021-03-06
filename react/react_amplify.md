# React Webアプリケーションの作成

## create-react-appコマンドによるReactアプリの作成

https://github.com/facebook/create-react-app

```
create-react-app myapp
cd myapp
```
「開発サーバー」を使用して、Webアプリケーションを起動する

```
yarn start
```

- Cloud9のメニュー ＞ Preview ＞ Preview Running Application でプレビューできる
- 「開発サーバー」を`Ctrl + C` (`Control`キーを押しながら`C`を押す)で止める

## WebアプリケーションにAmplifyライブラリを導入

https://aws-amplify.github.io/docs/js/react#add-auth

```
yarn add aws-amplify aws-amplify-react
```

## Amplifyのセットアップ

https://aws-amplify.github.io/docs/js/react#installation

```
amplify init
```
2つ目の質問(environment)のみ`dev`と入力し、その他はすべてエンターキーで進めてよい。

(実行例)
```
$ amplify init
  ? Enter a name for the project: myapp      <---- エンターキーを押す
  ? Enter a name for the environment: dev    <---- 2つ目の質問(environment)で dev と入力
  ? Choose your default editor: None         <---- エンターキーを押す。以下同様
  ? Choose the type of app that you're building: javascript
  ? What javascript framework are you using: react
  ? Source Directory Path: src
  ? Distribution Directory Path: build
  ? Build Command:  npm run-script build
  ? Start Command: npm run-script start
  ? Do you want to use an AWS profile? : Yes
  ? Please choose the profile you want to use: default
  
Initializing project in the cloud...         <---- しばらく待つ

Initialized your environment successfully.   <---- この表示が出ればOK

Your project has been successfully initialized and connected to the cloud!

Some next steps:
"amplify status" will show you what you've added already and if it's locally configured or deployed
"amplify <category> add" will allow you to add features like user login or a backend API
"amplify push" will build all your local backend resources and provision it in the cloud
"amplify publish" will build all your local backend and frontend resources (if you have hosting category added) and provision it in the cloud

Pro tip:
Try "amplify add api" to create a backend API and then "amplify publish" to deploy everything

```

# ポイント

- すべてのコマンドを順に実行する
  - 複数のコマンドには前後関係がある場合がある。その場合、先の手順を先に実行することはできない
  - 複数行をコピーしてターミナルに貼り付けすると、最終の行が実行されない場合がある。貼り付け後エンターを押す
- 各コマンドを正しいディレクトリで実行する
  - 新しくターミナルを開いた場合、カレントディレクトリが ~/environment となる
  - cd コマンドを実行すると、カレントディレクトリが ~/ となる
  - `yarn add`や`amplify init`は、`myapp` 以下で実行する必要がある。
- コマンドを実行したときのふるまい
  - 処理が成功した場合は何も表示しないコマンドが多い。
  - 処理が失敗した場合はなんらかしらのエラーメッセージが表示されるので、それをよく見て対処する
- yarn startを実行して、開発サーバーを立ち上げてから、プレビューする
  - 多重で実行しない
  - プレビューウィンドウを閉じてもyarn start（開発サーバー）は終了しない。
  - 開発サーバー実行中は、そのターミナルではコマンドを実行できない
    - 別のターミナルを新たに立ち上げてコマンドを打ち込むことができる。
      - その際は cd myapp と実行して、myappのディレクトリに移動することを忘れないこと
- プレビューウィンドウを閉じる際に、そのタブのバツボタンではなく、右端のバツボタンを押してしまう
  - Ctrl + ESCで復活できる
- ターミナル
  - Window ＞ New Terminal で新しいターミナルを開くことができる

# トラブルシューティング
- `myapp`ディレクトリがない場合
  - create-react-appを正しく実行していない
- `grep aws-amplify yarn.lock` で何も表示されない場合
  - yarn addを正しく実行していない
- `myapp/src/aws-exports.js`がない場合
  - yarn initを正しく実行していない
