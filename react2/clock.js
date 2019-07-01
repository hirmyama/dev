// minimal clock application

import React, { useState, useEffect } from 'react';

const App = () => {
  return <div><Clock/></div>;
};

const Clock = () => {
  // 2019/7/1 21:53:31 のような日時文字列を返す
  const currentTime = () => new Date().toLocaleString('ja-JP');
  
  // time: 現在の日時
  // setTime(): 日時を更新
  const [time, setTime] = useState(currentTime());
  
  // 副作用
  // componentDidMountの代わりとなる
  // https://ja.reactjs.org/docs/hooks-effect.html
  useEffect(() => {
    // 1秒ごとに日時を更新する
    setInterval(
      () => setTime(currentTime()),
      1000
    );
  });
  
  return <div>{time}</div>;
};

export default App;
