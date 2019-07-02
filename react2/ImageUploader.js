// https://github.com/aws-amplify/amplify-js/blob/master/packages/aws-amplify-react/src/Widget/PhotoPicker.js
// を参考に。

import React, {useState} from 'react';
import logo from './logo.svg';
import './App.css';
import Amplify, { Auth, Storage } from 'aws-amplify';
import { PhotoPicker, S3Album, S3Image } from 'aws-amplify-react';
import awsconfig from './aws-exports';
Amplify.configure(awsconfig);


const ImageUpload = () => {
  const [url, setUrl] = useState(null);
  const [file, setFile] = useState(null);
  
  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    console.log(file);
    setFile(()=>file);
    const reader = new FileReader();
    reader.onload = function(e) {
      const url = e.target.result;
      setUrl(()=>url);
    };
    reader.readAsDataURL(file);
  };
  
  const handleFileUpload = () => {
    Storage.put(file.name, file).then(data=>console.log(data)).catch(err=>alert(err));
  };
  
  return <React.Fragment>
    <input type="file" onChange={handleFileSelect}/>
    <img src={url}/>
    <button type="button" onClick={handleFileUpload}>アップロード</button>
  </React.Fragment>;

};

const ImageList = () => {
  return <S3Album path=""/>;
};

const App = () => {
  
  
  return (
    <React.Fragment>
      <ImageUpload/>
      <ImageList/>
    </React.Fragment>
  );
};

export default App;
