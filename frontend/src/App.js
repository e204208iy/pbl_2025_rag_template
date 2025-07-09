import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(scrollToBottom, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    // ユーザーのメッセージと、AIの空の応答をセット
    setMessages((prev) => [...prev, userMessage, { role: 'assistant', content: '' }]);
    setInput('');

    try {
      console.log('リクエストを送信します:', JSON.stringify({ text: input }));
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input }),
      });

      console.log('レスポンスヘッダーを受信しました:', response);

      if (!response.ok) {
        console.error('サーバーエラー:', response.status, response.statusText);
        const errorText = await response.text();
        console.error('エラー内容:', errorText);
        throw new Error(`サーバーエラー: ${response.status}`);
      }

      if (!response.body) {
        console.error('レスポンスにボディがありません。');
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let done = false;

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;

        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          console.log('%c[受信したチャンク]', 'color: green; font-weight: bold;', chunk); // ★最重要★

          // --- パフォーマンス改善案 ---
          // 毎回全メッセージをmapするのではなく、最後の要素だけを効率的に更新します。
          setMessages((prev) => {
            const newMessages = [...prev];
            const lastMessageIndex = newMessages.length - 1;
            newMessages[lastMessageIndex] = {
              ...newMessages[lastMessageIndex],
              content: newMessages[lastMessageIndex].content + chunk,
            };
            return newMessages;
          });
        }
      }
      console.log('ストリームの受信が完了しました。');

    } catch (error) {
      console.error('%c[エラー]', 'color: red; font-weight: bold;', 'ストリーミングのフェッチに失敗しました:', error);
      setMessages((prev) => {
        const newMessages = [...prev];
        const lastMessageIndex = newMessages.length - 1;
        if (newMessages[lastMessageIndex].content === '') {
           newMessages[lastMessageIndex] = {
            ...newMessages[lastMessageIndex],
            content: 'エラーが発生しました。詳細はコンソールを確認してください。',
          };
        }
        return newMessages;
      });
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            {/* 改行を<br>に変換して表示 */}
            {msg.content.split('\n').map((line, i) => (
              <React.Fragment key={i}>
                {line}
                <br />
              </React.Fragment>
            ))}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="メッセージを入力..."
        />
        <button type="submit">送信</button>
      </form>
    </div>
  );
}

export default App;