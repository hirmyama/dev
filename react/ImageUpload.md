# アップロード機能の追加

## IAMロールの修正(ログインしたユーザーがS3に画像をアップロードできるようにする)

マネジメントコンソールのタブで操作

- マネジメントコンソール＞サービス＞IAM
- ロール
- 「IAM ロールの概要」が表示された場合は、右上のバツをクリックして閉じる
- 検索に `-auth` と入力。1件のロールが検索結果に表示される。
- ロールをクリック
- [ポリシーをアタッチします]
- 検索に `s3full` と入力。1件のポリシーが検索結果に表示される。
- ポリシーにチェックを付け、[ポリシーのアタッチ]

## Webアプリにアップロード機能を追加

Cloud9で操作


画像アップロード用のバケット名を調べる。
```
$ aws s3 ls |grep photo-bucket
2019-06-27 01:48:14 photo-bucket-photobucket-1qiugw0k9dq86
```

`ImageUpload.js` を作成

```
$ touch ~/environment/myapp/src/ImageUpload.js
```

`ImageUpload.js` を開き、下記を入力する。バケット名の部分は上記手順で調べたバケット名に書き換える。

```
import React from 'react';
import Amplify from 'aws-amplify';
import { Storage } from 'aws-amplify';

Amplify.configure({
  Storage: {
    AWSS3: {
      bucket: 'photo-bucket-photobucket-1qiugw0k9dq86', // S3バケット名を''内に記入
      region: 'ap-northeast-1',
    }
  }
});

class ImageUpload extends React.Component {
  upload() {
    let files = document.getElementById('file').files;
    if (files.length === 0) {
      alert('アップロードするファイルを指定してください');
      return;
    }
    Storage.put(files[0].name, files[0])
      .then(result=>alert('アップロード完了。リロードしてください'))
      .catch(err=>alert(err));
  }
  render() {
    return <div>
      <input type="file" id="file" />
      <input type="button" value="画像をアップロード" onClick={()=>this.upload()} />
    </div>;
  }
}

export default ImageUpload;
```

ファイルを保存する。

確認：バケット名の部分を書き換えましたか？

`App.js`を開く。ファイル先頭のimport部分に下記を追加
```
import ImageUpload from './ImageUpload';
```

`<div className="App">` と `<header className="App-header">`の間に下記1行を追加
     
```
<ImageUpload />
```

ファイルを保存する。

開発サーバーを起動
```
$ yarn start
```

プレビューでWebアプリケーションを表示。

ログイン後、ファイル選択ボタンで画像を選択し、アップロード。

アップロードした画像がS3バケットに格納されることを確認

注意：ページ内に画像を表示する機能は今後の手順で作成する。
