# Cloud9

公式サイト
https://aws.amazon.com/jp/cloud9/

AWSマンガ
https://aws.amazon.com/jp/campaigns/manga/vol2-3/

1. マネジメントコンソールにログイン
1. 画面右上のリージョン表示（[サポート]の左）が[東京]になっていなければ、クリックして[アジアパシフィック（東京）]に設定
1. サービス＞Cloud9
1. [Create Environment]
1. Name: `environment`, [Next Step]
1. Instance Type: `t2.small`,  [Next Step]
1. [Create Environment]
1. We are creating...と表示される。1分ほど待つ
1. 画面左側の Environment には、ファイルの一覧が表示される。
1. README.mdをダブルクリックすると、エディタが表示される。適当に編集して保存してみよう
1. 画面下部のbashと書かれたタブでは、Linuxのコマンドを実行することができる。`mkdir test`と打ち込んでみよう
1. 画面上部のメニュー＞AWS Cloud9＞Go to your dashboardとすると、別タブでマネジメントコンソールが表示される。
