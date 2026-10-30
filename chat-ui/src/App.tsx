import { useState } from 'react'
import './App.css'
import type { Message } from "./types";
import { streamChat } from './api/chat';


function MessageBubble({message} : {message: Message}) {
  const isUser = message.sender === "user";
  const align = isUser ? "justify-end" : "justify-start"
  const colors = isUser 
    ? "bg-blue-600 text-white"
    : "bg-gray-100 text-gray-900";
  return(
    <li className={`flex ${align} my-1`}>
      <p className={`${colors} rounded-2xl px-4 py-2 max-w-[75%] whitespace-pre-wrap`}>
        {message.content}
      </p>
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
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  async function handleSubmit(e: React.FormEvent){

    e.preventDefault();
    const text = input.trim();
    if (!text || isLoading) return;

    const userMsg: Message = {msgID: crypto.randomUUID(), sender: "user", content: text};
    const history = [...messages, userMsg]
    const assistantID = crypto.randomUUID();
    setMessages([...history, { msgID: assistantID, sender: "chat", content: ""}]);
    setInput("");
    setIsLoading(true);
    setError(null);
    
    try {
      await streamChat(history, (t) =>
        setMessages(prev => prev.map(m => m.msgID === assistantID ? { 
          ...m, content: m.content + t } : m
        )))
    } catch {
      setError("Could not reach the server. Is the backend running?")
    } finally {
      setIsLoading(false)
    }
  }
  return (
    <div className = "flex flex-col h-screen max-w-2xl mx-auto p-4">
      <div className = "flex-1 overflow-y-auto">
        <MessageList messages={messages}/>
      </div>
      {error && <p className="text-red-600">{error}</p>}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          className="flex-1 border rounded px-2"
          placeholder='Type a message...'
        />
        <button type='submit' disabled={isLoading}>Send</button>
      </form>
    </div>
  )
}

export default App
