# CodeBuild

`buildspec.yml`ファイルを作成(index.htmlと同じ場所)

```
version: 0.2
phases:
  build:
    commands:
      date >> index.html
artifacts:
  files:
    - index.html
    - appspec.yml
```

`appspec.yml`ファイルを作成(index.htmlと同じ場所)

```
version: 0.0
os: linux
files:
  - source: /index.html
    destination: /var/www/html
```

Gitリポジトリに追加

```
git add buildspec.yml appspec.yml
git commit -m 'add buildspec and appspec'
git push
```

アーティファクトを格納するバケットを作成（バケット名は修正すること）

```
aws s3 mb s3://artifact-1234
```

サービス→CodeBuild→ビルドプロジェクト→[ビルドプロジェクトを作成する]

プロジェクトの設定→プロジェクト名: `myproj`

送信元→リポジトリ: `myrepo`

環境→オペレーティングシステム: `Ubuntu`、ランタイム: `Standard`、

イメージ: `aws/codebuild/standard:1.0`

アーティファクト→タイプ：`Amazon S3`、

バケット名：(上記で作成したバケット名を指定)、

名前：`myweb.zip`、アーティファクトのパッケージ化: [Zip]

[ビルドプロジェクトを作成する]

備考：このとき `codebuild-myproj-service-role`のような「サービスロール」と、そのサービスロールにアタッチされる`CodeBuildBasePolicy-myproj-ap-northeast-1`のようなIAMポリシーが自動的に作成される。プロジェクトを削除する際、これらは手動で削除する必要がある。

[ビルドの開始]、[ビルドの開始]

ステータスが「進行中」から「成功」に変わるまで待つ

Cloud9のターミナルで以下を実行し、生成されたアーティファクトの内容を確認

```
cd
mkdir myweb
cd myweb
aws s3 cp s3://artifact-1234/myweb.zip .
unzip myweb.zip
ls -l
cat index.html
```



