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

      <style jsx>{`
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

        .chat-root {
          height: 100vh;
          background: #070b0f;
          display: flex;
          flex-direction: column;
          font-family: 'Share Tech Mono', monospace;
          color: #e0ffe0;
          position: relative;
          overflow: hidden;
        }

        .chat-root::before {
          content: '';
          position: fixed;
          inset: 0;
          background:
            radial-gradient(ellipse 80% 50% at 50% -10%, rgba(0, 255, 128, 0.08) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 100% 100%, rgba(180, 0, 255, 0.06) 0%, transparent 50%);
          pointer-events: none;
          z-index: 0;
        }

        .scanlines {
          position: fixed;
          inset: 0;
          background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0, 0, 0, 0.08) 2px,
            rgba(0, 0, 0, 0.08) 4px
          );
          pointer-events: none;
          z-index: 10;
        }

        .header {
          border-bottom: 1px solid rgba(0, 255, 128, 0.2);
          background: rgba(7, 11, 15, 0.95);
          backdrop-filter: blur(10px);
          position: sticky;
          top: 0;
          z-index: 5;
        }

        .header-inner {
          max-width: 860px;
          margin: 0 auto;
          padding: 18px 24px;
          display: flex;
          align-items: center;
          justify-content: space-between;
        }

        .logo {
          font-family: 'Orbitron', monospace;
          font-size: 22px;
          font-weight: 900;
          letter-spacing: 0.1em;
        }

        .logo-bracket { color: rgba(0, 255, 128, 0.4); }
        .logo-text { color: #fff; }
        .logo-accent {
          color: #00ff80;
          text-shadow: 0 0 20px rgba(0, 255, 128, 0.8), 0 0 40px rgba(0, 255, 128, 0.4);
        }

        .status {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 11px;
          letter-spacing: 0.15em;
          color: rgba(0, 255, 128, 0.6);
        }

        .status-dot {
          width: 7px;
          height: 7px;
          border-radius: 50%;
          background: #00ff80;
          box-shadow: 0 0 8px #00ff80;
          animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.4; }
        }

        .messages-area {
          flex: 1;
          overflow-y: auto;
          position: relative;
          z-index: 1;
        }

        .messages-area::-webkit-scrollbar { width: 4px; }
        .messages-area::-webkit-scrollbar-track { background: transparent; }
        .messages-area::-webkit-scrollbar-thumb {
          background: rgba(0, 255, 128, 0.2);
          border-radius: 2px;
        }

        .messages-inner {
          max-width: 860px;
          margin: 0 auto;
          padding: 32px 24px;
          display: flex;
          flex-direction: column;
          gap: 24px;
        }

        .message-row { display: flex; flex-direction: column; gap: 6px; }
        .message-row.user { align-items: flex-end; }
        .message-row.assistant { align-items: flex-start; }

        .message-label {
          font-size: 10px;
          letter-spacing: 0.2em;
          color: rgba(255, 255, 255, 0.3);
          padding: 0 4px;
        }

        .message-row.user .message-label { color: rgba(180, 0, 255, 0.6); }
        .message-row.assistant .message-label { color: rgba(0, 255, 128, 0.6); }

        .message-bubble {
          max-width: 72%;
          padding: 14px 18px;
          border-radius: 2px;
          font-size: 14px;
          line-height: 1.7;
          position: relative;
        }

        .message-bubble.user {
          background: rgba(180, 0, 255, 0.1);
          border: 1px solid rgba(180, 0, 255, 0.3);
          color: #e8d0ff;
          border-top-right-radius: 0;
        }

        .message-bubble.user::after {
          content: '';
          position: absolute;
          top: 0; right: -1px;
          width: 3px; height: 100%;
          background: rgba(180, 0, 255, 0.5);
          box-shadow: 0 0 8px rgba(180, 0, 255, 0.5);
        }

        .message-bubble.assistant {
          background: rgba(0, 255, 128, 0.05);
          border: 1px solid rgba(0, 255, 128, 0.2);
          color: #c8ffd8;
          border-top-left-radius: 0;
        }

        .message-bubble.assistant::before {
          content: '';
          position: absolute;
          top: 0; left: -1px;
          width: 3px; height: 100%;
          background: rgba(0, 255, 128, 0.5);
          box-shadow: 0 0 8px rgba(0, 255, 128, 0.5);
        }

        .typing-dots {
          display: flex;
          gap: 5px;
          align-items: center;
          height: 20px;
        }

        .typing-dots span {
          width: 6px; height: 6px;
          border-radius: 50%;
          background: #00ff80;
          animation: blink 1.2s ease-in-out infinite;
        }

        .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
        .typing-dots span:nth-child(3) { animation-delay: 0.4s; }

        @keyframes blink {
          0%, 100% { opacity: 0.2; transform: scale(0.8); }
          50% { opacity: 1; transform: scale(1.1); box-shadow: 0 0 6px #00ff80; }
        }

        .input-area {
          border-top: 1px solid rgba(0, 255, 128, 0.15);
          background: rgba(7, 11, 15, 0.98);
          backdrop-filter: blur(10px);
          position: sticky;
          bottom: 0;
          z-index: 5;
        }

        .input-inner {
          max-width: 860px;
          margin: 0 auto;
          padding: 20px 24px;
        }

        .input-wrapper {
          display: flex;
          align-items: center;
          border: 1px solid rgba(0, 255, 128, 0.25);
          background: rgba(0, 255, 128, 0.03);
          transition: border-color 0.2s, box-shadow 0.2s;
        }

        .input-wrapper:focus-within {
          border-color: rgba(0, 255, 128, 0.6);
          box-shadow: 0 0 20px rgba(0, 255, 128, 0.1), inset 0 0 20px rgba(0, 255, 128, 0.03);
        }

        .input-prefix {
          padding: 0 14px;
          color: rgba(0, 255, 128, 0.5);
          font-size: 15px;
          user-select: none;
        }

        .input-field {
          flex: 1;
          background: transparent;
          border: none;
          outline: none;
          color: #e0ffe0;
          font-family: 'Share Tech Mono', monospace;
          font-size: 14px;
          padding: 16px 0;
          caret-color: #00ff80;
        }

        .input-field::placeholder { color: rgba(0, 255, 128, 0.25); }
        .input-field:disabled { opacity: 0.5; }

        .send-btn {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 16px 20px;
          background: rgba(0, 255, 128, 0.1);
          border: none;
          border-left: 1px solid rgba(0, 255, 128, 0.2);
          color: #00ff80;
          font-family: 'Orbitron', monospace;
          font-size: 11px;
          font-weight: 700;
          letter-spacing: 0.15em;
          cursor: pointer;
          transition: background 0.2s, box-shadow 0.2s;
        }

        .send-btn:hover:not(:disabled) {
          background: rgba(0, 255, 128, 0.2);
          box-shadow: inset 0 0 20px rgba(0, 255, 128, 0.1);
        }

        .send-btn:disabled { opacity: 0.4; cursor: not-allowed; }
      `}</style>
    </div>
  );
}