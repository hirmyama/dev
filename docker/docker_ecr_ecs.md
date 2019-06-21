# Docker/ECR/ECS

## Dockerイメージの開発

Cloud9を起動

Dockerfileを作成

```
FROM ubuntu
RUN apt-get update -y \
&& apt-get install httpd \
&& rm -r /var/lib/apt/lists/*
RUN echo hello! > /var/www/html/index.html
EXPOSE 80
CMD ["apachectl", "-D", "FOREGROUND"]
```

イメージをビルド

```
docker build -t web .
```

コンテナを実行

注：--name webでコンテナにwebという名前をつける。末尾のwebはイメージ名。

```
docker run -d -p 8080:80 --name web web
```

Cloud9のメニュー→Preview→Preview Running Applicationを中クリックで開いて動作確認。

コンテナを停止

```
docker stop web
```



## ECRにイメージをプッシュ

ECRリポジトリの作成

```
aws ecr create-repository --repository-name webapp
```

表示されたURIをコピーしておく。

Dockerコマンドを使用してECRにログイン

```
$(aws ecr get-login --no-include-email)
```

ECRのレポジトリにイメージをプッシュ

```
docker tag web （URIを貼り付け）
docker push （URIを貼り付け）
```



## ECSによるサービスの起動

### クラスターの作成

サービス→ECS→クラスター→[クラスターの作成]

クラスターテンプレートの選択→[ネットワーキングのみ]、[次のステップ]

クラスター名: `mycluster`、[作成]、[クラスターの表示]

### タスクの定義

タスク定義→[新しいタスク定義の作成]

起動タイプの互換性の選択→[FARGATE]、[次のステップ]

タスク定義名: `web`、タスクメモリ: `0.5GB`、タスクCPU: `0.25 vCPU`

[コンテナの追加]→コンテナ名`web`、イメージ: （ECRのリポジトリURIを貼り付け）、

ポートマッピング: `80`、[追加]、[作成]、[タスク定義の表示]

### サービスの作成

[アクション]→[サービスの作成]、起動タイプ: `FARGATE`、

サービス名: `web`、タスクの数: `1`、[次のステップ]、

クラスターVPC: （DEFAULTのVPCを選択）、サブネット: （いずれかを1つ選択）、

サービスの検出の統合の有効化: （チェックを外す）、[次のステップ]、

[次のステップ]、[サービスの作成]、[サービスの表示]

[タスク]タブ内の表の[タスク]列のリンクをクリック、

前回のステータス（原文：Last status）がRUNNINGになるまで待つ。

NetworkのPublic IPに表示されたIPアドレスをコピーし、別タブで開いて確認。



