# CodeCommit

サービス＞CodeCommit、リポジトリ＞リポジトリの作成

リポジトリ名: `myrepo`、作成

サービス＞Cloud9、Create Enviroment、Name＞`myenv`

Next Step、Next Step、Create Environment

Cloud9環境が立ち上がったら画面下ターミナルで下記を入力

```
ssh-keygen -f ~/.ssh/codecommit_rsa -P ''
```

生成されたSSHパブリックキーをIAMユーザーに対してアップロードして登録

```
CURRENT_IAM_USER=$(aws iam get-user --query 'User.UserName' --output text)
PUBLIC_KEY_ID=$(aws iam upload-ssh-public-key \
--user-name $CURRENT_IAM_USER \
--ssh-public-key-body file://~/.ssh/codecommit_rsa.pub \
--query 'SSHPublicKey.SSHPublicKeyId')
```

CodeCommitに接続できるようにする

```
echo 'HOST git-codecommit.*.amazonaws.com' >> ~/.ssh/config
echo "  User $PUBLIC_KEY_ID" >> ~/.ssh/config
echo '  IdentityFile ~/.ssh/codecommit_rsa' >> ~/.ssh/config
chmod 600 ~/.ssh/config
```

接続をチェック（Are you sure ... ? と出たらyesと入力してenter）

```
ssh git-codecommit.ap-northeast-1.amazonaws.com
```

Gitリポジトリを作成、index.htmlをコミット・プッシュ

```
mkdir myrepo
cd myrepo
git init .
echo 'hello' > index.html
git add index.html
git commit -m 'initial commit'
```

CodeCommitの `myrepo` の「URLのクローン」列で「SSH」をクリック

下記を実行（XXX部分には上記手順でコピーされた「URL」を貼り付け）

```
git remote add origin XXX
git push -u origin master
```

CodeCommit画面をリロードし、`myrepo`に`index.html`が格納されていることを確認。

