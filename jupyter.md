# IAMロールの作成

- サービス＞IAM
- ロール＞ロールの作成
- 信頼されたエンティティの種類を選択: `EC2`
- アタッチするアクセス権限ポリシー: `AdministratorAccess`
- タグ: なし
- ロール名: `EC2_admin_role`

# EC2インスタンスの起動

- サービス＞EC2
- インスタンスの作成
- AMI: `Amazon Linux 2 64ビット(x86)`
- インスタンスタイプ: `t2.micro`
- インスタンスの詳細: 
  - IAMロール: `EC2_admin_role`
  - 画面下部「高度な詳細」を開き「ユーザーデータ」に以下を貼り付け
  
```
#!/bin/bash
yum update -y
yum install -y git
amazon-linux-extras install -y python3
python3 -m pip install --upgrade pip
python3 -m pip install jupyterlab boto3 awscli
aws configure set default.region ap-northeast-1
cd /home/ec2-user
jupyter lab --ip='0.0.0.0' --allow-root --port=80 --NotebookApp.token='Yamada3!'
```

- ストレージの追加: 変更なし
- タグの追加: キー `Name`  値 `jupyter`
- セキュリティグループの設定: 「ルールの追加」、タイプ: HTTP、ソース: 任意の場所
- あとは全てデフォルト値で起動。

- 起動から3分ほど経過したら、インスタンスの「IPv4パブリックIP」をコピーし、新しいタブで開く。
- Jupyterのパスワードに `Yamada3!` と入力して `Log in` をクリック。

- なお、このインスタンスを再起動・停止すると、再び接続することはできなくなるので注意。
