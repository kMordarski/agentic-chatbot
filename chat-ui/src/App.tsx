import { useState } from 'react'
import './App.css'
import type { Message } from "./types";

function MessageBubble({message} : {message: Message}) {
  const align = message.sender === "user" ? "justify-end" : "justify-start"
  return(
    <li className={`flex ${align}`}>
      <p>{message.content}</p>
    </li>

  )
}

function MessageList({messages} : {messages: Message[]}) {
  return(
    <ul>
      {messages.map((m) => (
        <MessageBubble key={m.msgID} message={m}/>
      ))}
    </ul>
  );
}

function App() {

  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("")

  function handleSubmit(e: React.FormEvent){

    e.preventDefault();
    const text = input.trim();
    if (!text) return;

    const userMsg: Message = {msgID: crypto.randomUUID(), sender: "user", content: text};
    setMessages(prev => [...prev, userMsg]);
    setInput("");

    // fake reply until backend exists

    setTimeout(() => {
      setMessages(prev => [
        ...prev, 
        {msgID: crypto.randomUUID(), sender: "chat", content: `Echo: ${text}`},
      ]);
    }, 500);
  }
  return (
    <div className = "flex flex-col h-screen max-w-2xl mx-auto p-4">
      <div className = "flex-1 overflow-y-auto">
        <MessageList messages={messages}/>
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          className="flex-1 border rounded px-2"
          placeholder='Type a message...'
        />
        <button type='submit'>Send</button>
      </form>
    </div>
  )
}

export default App
