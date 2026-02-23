'use client';

import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { v4 as uuidv4 } from 'uuid';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const SESSION_ID = uuidv4();

export default function ChatPage() {
  const [backendOnline, setBackendOnline] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: "SYSTEM ONLINE. I'm your AI game scout — tell me what kind of game you're hunting for and I'll pull the best matches from the Steam database.",
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`);
        setBackendOnline(res.ok);
      } catch {
        setBackendOnline(false);
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: SESSION_ID,
          message: { role: 'user', content: input },
        }),
      });

      const data = await res.json();
      setMessages((prev) => [...prev, { role: 'assistant', content: data.message.content }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'CONNECTION ERROR. Please try again.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-root">
      <div className="scanlines" />

      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-bracket">[</span>
            <span className="logo-text">STEAM<span className="logo-accent">SCOUT</span></span>
            <span className="logo-bracket">]</span>
          </div>
          <div className="status">
            <span className="status-dot" style={{ background: backendOnline ? '#00ff80' : '#ff3060', boxShadow: `0 0 8px ${backendOnline ? '#00ff80' : '#ff3060'}` }} />
            <span className="status-text">{backendOnline ? 'DATABASE CONNECTED' : 'BACKEND OFFLINE'}</span>
          </div>
        </div>
      </header>

      <main className="messages-area">
        <div className="messages-inner">
          {messages.map((msg, i) => (
            <div key={i} className={`message-row ${msg.role}`}>
              <div className="message-label">{msg.role === 'user' ? 'YOU' : 'SCOUT_AI'}</div>
              <div className={`message-bubble ${msg.role}`}>
                <div className="message-text"><ReactMarkdown>{msg.content}</ReactMarkdown></div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="message-row assistant">
              <div className="message-label">SCOUT_AI</div>
              <div className="message-bubble assistant">
                <span className="typing-dots">
                  <span />
                  <span />
                  <span />
                </span>
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      </main>

      <footer className="input-area">
        <div className="input-inner">
          <div className="input-wrapper">
            <span className="input-prefix">&gt;_</span>
            <input
              className="input-field"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Describe the game you're looking for..."
              disabled={loading}
            />
            <button className="send-btn" onClick={sendMessage} disabled={loading}>
              <span>SEND</span>
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M2 8H14M14 8L9 3M14 8L9 13" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>
          </div>
        </div>
      </footer>

    </div>
  );
}