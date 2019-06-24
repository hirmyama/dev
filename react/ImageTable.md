App.jsに,import文と、ListImages APIの設定を追記

```
import { API } from 'aws-amplify';
import { S3Image } from 'aws-amplify';

Amplify.configure({
  API: {
    endpoints: [
      {
        name: "hello",
        endpoint: "https://hq9ps9iptk.execute-api.ap-northeast-1.amazonaws.com/Prod"
      },
    ]
  }
});
```

App.jsに,画像を表示するコンポーネントを追加
```
class ImageTable extends React.Component {
  state = {
    images: []
  };
  constructor(prop) {
    super(prop);
    
    
    API.get("hello", "/hello").then(response => {
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
        {this.state.images.map(entry=><ImageRow objkey={entry.key} tags={entry.tags} />)}
      </tbody>
    </table>
  )}
}

class ImageRow extends React.Component {
  
  render() { 
    return <tr>
      <td className='images'><S3Image imgKey={this.props.objkey} /></td>
      <td className='image-tags'>{this.props.tags}</td>
    </tr>;
  }
}
```

ImageTableの描画部分をAppに追加
```
function App() {
  ...
        <ImageUpload />
        <ImageTable />
  ...
}
```

App.cssへ下記を追記

```

.images img {
  width: 400px;
  height: auto;
}

.image-tags {
  width: 400px;
}
```

