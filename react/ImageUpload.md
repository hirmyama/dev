
S3バケットを作成


Corsの設定をバケットに追加

```
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>HEAD</AllowedMethod>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedMethod>PUT</AllowedMethod>
    <AllowedMethod>POST</AllowedMethod>
    <AllowedMethod>DELETE</AllowedMethod>
    <MaxAgeSeconds>3000</MaxAgeSeconds>
    <ExposeHeader>x-amz-server-side-encryption</ExposeHeader>
    <ExposeHeader>x-amz-request-id</ExposeHeader>
    <ExposeHeader>x-amz-id-2</ExposeHeader>
    <ExposeHeader>ETag</ExposeHeader>
    <AllowedHeader>*</AllowedHeader>
</CORSRule>
</CORSConfiguration>
```

IAMポリシーの「Auth_Role」に, S3FullAccessを追加。  

Storage カテゴリをインポート

```
import { Storage } from 'aws-amplify';
```

Stroageの設定(S3バケット情報)を追加
```
Amplify.configure({
  Storage: {
    AWSS3: {
      bucket: 'images-029382934', // S3バケット
      region: 'ap-northeast-1', // リージョン
    }
  }
});
```

画像アップロードコンポーネントを定義
```
class ImageUpload extends React.Component {
  upload() {
    let files = document.getElementById('file').files;
    if (files.length === 0) {
      alert('アップロードするファイルを指定してください');
      return;
    }
    Storage.put(files[0].name, files[0])
      .then(result=>alert('アップロード完了'))
      .catch(err=>alert(err));
  }
  render() {
    return <div>
      <input type="file" id="file" />
      <input type="button" value="画像をアップロード" onClick={()=>this.upload()} />
    </div>
  }
}
```
画像アップロードコンポーネントを function App() 内に追加
```
<ImageUpload />
```
