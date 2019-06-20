# CodeDeploy

## CodeDeployサービスロールの作成

サービス→IAM→ロール→ロールの作成

このロールを使用するサービスを選択→CodeDeploy、

ユースケースの選択→CodeDeploy

次のステップ→次のステップ→次のステップ

ロール名: `code_deploy_service_role`、ロールの作成

## EC2のロールの作成

ロールの作成

このロールを使用するサービスを選択→EC2、次のステップ

「検索」に`codedeploy`と入力し、`AmazonEC2RoleforAWSCodeDeploy`にチェック

次のステップ→次のステップ

ロール名: `code_deploy_ec2_role`、ロールの作成

備考：このとき、ロール名と同名の「インスタンスプロファイル」ができる。

`aws iam list-instance-profiles`で確認できる。

ロールのARN：`arn:aws:iam::185909028061:role/code_deploy_ec2_role`

インスタンスプロファイルのARN：`arn:aws:iam::185909028061:instance-profile/code_deploy_ec2_role`

## デプロイ先のEC2インスタンスを立ち上げ

```
# セキュリティグループを作成
WEBSG_ID=$(aws ec2 create-security-group \
--group-name websg \
--description websg \
--query GroupId --output text)

# セキュリティグループにてHTTPのインバウンド通信を許可
aws ec2 authorize-security-group-ingress \
--group-id $WEBSG_ID \
--protocol tcp \
--port 80 \
--cidr 0.0.0.0/0

# 最新のAmazon Linux 2 AMI
AMI_ID='ami-084040f99a74ce8c3' 

# ユーザーデータのファイルを作成
cat <<EOF >userdata.sh
#!/bin/bash
yum update -y
yum install -y ruby wget
wget https://aws-codedeploy-ap-northeast-1.s3.ap-northeast-1.amazonaws.com/latest/install
chmod +x ./install
./install auto
yum install -y httpd
systemctl enable --now httpd.service
EOF

# インスタンスを起動
INSTANCE_ID=$(aws ec2 run-instances \
--image-id $AMI_ID \
--instance-type t2.micro \
--user-data file://userdata.sh \
--iam-instance-profile Name=code_deploy_ec2_role \
--query 'Instances[].InstanceId' \
--output text)

# インスタンスのセキュリティグループを更新
aws ec2 modify-instance-attribute \
--instance-id $INSTANCE_ID \
--groups $WEBSG_ID

# インスタンスにタグをつける
aws ec2 create-tags \
--resources $INSTANCE_ID \
--tags Key=Name,Value=web

# インスタンスのIPアドレスを調べる
IPADDR=$(aws ec2 describe-instances \
--instance-id $INSTANCE_ID \
--query 'Reservations[].Instances[].PublicIpAddress' \
--output text)

# HTTPで接続できるまで待つ(1分ほどかかる)
until curl --max-time 1 $IPADDR >/dev/null; do sleep 10; done
echo $IPADDR
echo '接続できました'

```

表示されたIPアドレスにアクセスして「Test Page」が表示されることを確認

### CodeDeployの設定

サービス→CodeDeploy→アプリケーション→アプリケーションの作成

アプリケーション名: `myapp`、

コンピューティングプラットフォーム: `EC2/オンプレミス`

[アプリケーションの作成]

デプロイグループ→[デプロイグループの作成]

デプロイグループ名の入力: `mydeploygroup`、

サービスロール: `code_deploy_service_role`

環境設定→[Amazon EC2インスタンス]をチェック、

キー`Name`、値:`web`

ロードバランサー: [ロードバランシングを有効にする]チェックを外す

[デプロイグループの作成]

## S3のアーティファクトのパスをコピー

S3の画面にて、myweb.zipをクリックして表示し、[コピーパス]をクリック

## デプロイ

[デプロイの作成]

デプロイグループ: `mydeploygroup`、

リビジョンの場所: (コピーしたパスを貼り付け)、[デプロイの作成]

