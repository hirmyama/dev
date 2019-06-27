# 画像一覧機能の作成

```
$ touch ~/environment/myapp/src/ImageTable.js
```

ImageTable.jsを開く。

下記の内容を記入する。`endpoint: `の部分には、前の工程で作成したAPIのURLを書き込む。

```
import React from 'react';
import Amplify from 'aws-amplify';
import { API } from 'aws-amplify';
import { S3Image } from 'aws-amplify-react';

Amplify.configure({
  API: {
    endpoints: [
      {
        name: "hello",
        endpoint: "https://6q5iyrihae.execute-api.ap-northeast-1.amazonaws.com/Prod/hello" // エンドポイントのURLを""内に記入
      },
    ]
  }
});

class ImageTable extends React.Component {
  state = {
    images: []
  };
  constructor(prop) {
    super(prop);
    
    API.get("hello", "").then(response => {
      console.log("response start");
      console.log(response);
      console.log("response end");
      this.setState({'images': response});
    }).catch(error => {
      console.log("err start");
      console.log(error);
      console.log("err end");
    });
    
  }
  render() {
    return (
      <table>
        <tbody>
        {this.state.images.map((entry)=><ImageRow ObjectKey={entry['ObjectKey'].replace('public/', '')} Tags={entry.Tags} />)}
        </tbody>
      </table>
    );
  }
}

class ImageRow extends React.Component {
  constructor(prop) {
    super(prop);
  }
  render() { 
    return (
      <tr>
        <td className='images'><S3Image imgKey={this.props.ObjectKey} />{this.props.ObjectKey}</td>
        <td className='image-tags'>{this.props.Tags}</td>
      </tr>
    );
  }
}

export default ImageTable;
```

ファイルを保存する。

確認：エンドポイントのURLをファイル内に書き込みましたか？

`App.js`を開く。ファイル先頭のimport部分に下記を追加
```
import ImageTable from './ImageTable';
```

`<ImageUpload/>` と `<header className="App-header">`の間に下記1行を追加

```
<ImageTable/>
```

`App.css`を開き、最下行に下記を追記

```
.images img {
  width: 400px;
  height: auto;
}

.image-tags {
  width: 400px;
}
```

Webアプリケーションにアクセスして、アップロードした画像が表示されていることを確認。
