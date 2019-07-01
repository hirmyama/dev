// minimal todo application

import React, { useState } from 'react';
// https://github.com/robcalcroft/react-use-input
// yarn add react-use-input
import useInput from 'react-use-input';

const App = () => {
  // 2個のTodoを使っても正しく動作するように
  return <div><Todo/><Todo/></div>;
};

const Todo = () => {
  // Todoリスト
  const [list, updateList] = useState([]);
  
  // 新しいTodoを追加
  const add = (text) => {
    // pushやunshiftを使うのではなく、
    // 関数を使って、新しい状態を返す
    updateList(list=>[text, ...list]);
  };
  
  // 子のコンポーネントに親コンポーネントの内部の関数を渡す
  return <div>
    <Input add={add}/>
    <List list={list}/>
  </div>;
};

// 入力用のコンポーネント。Todoの子供のコンポーネント。
// propsとして、親コンポーネントに新しいTodoテキストを渡すための
// 関数addを取る。
const Input = ({add}) => {
  // テキストボックスの状態（入力された文字列）。
  // useInputの内部ではuseStateを使用している。
  const [text, setTextFromEvent, setText] = useInput("");
  // addボタンクリック時の処理
  const clicked = () => {
    add(text);
    setText("");
  };
  
  return <form>
    <input value={text} onChange={setTextFromEvent} />
    { /* type=buttonをつけないとsubmitになってしまう */ }
    <button type="button" onClick={clicked}>add</button>
  </form>;
};

// Todo一覧のコンポーネント。Todoの子供のコンポーネント。
// 引数としてTodo一覧（state）を受け取る
const List = ({list}) => {
  // key, refはpropとして受け取ることができない
  // https://reactjs.org/warnings/special-props.html
  const ListItem = ({text}) => {
    return <li>{text}</li>;
  };
  // 配列内の要素の識別のため、keyを渡す
  // https://ja.reactjs.org/docs/lists-and-keys.html
  const items = list.map(text => <ListItem key={text} text={text}/>);
  return <ul>{items}</ul>;
};

export default App;
