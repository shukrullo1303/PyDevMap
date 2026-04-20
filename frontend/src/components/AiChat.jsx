import React, { useState, useRef, useEffect } from 'react';
import api from '../services/api';

export default function AiChat({ lessonId }) {
  const [open, setOpen]       = useState(false);
  const [input, setInput]     = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [history]);

  const send = async () => {
    const msg = input.trim();
    if (!msg || loading) return;
    setInput('');
    const newHistory = [...history, { role: 'user', content: msg }];
    setHistory(newHistory);
    setLoading(true);
    try {
      const res = await api.post('/ai/chat/', {
        message: msg,
        lesson_id: lessonId,
        history: newHistory.slice(-6),
      });
      setHistory(h => [...h, { role: 'assistant', content: res.data.reply }]);
    } catch {
      setHistory(h => [...h, { role: 'assistant', content: 'Xatolik yuz berdi. Qaytadan urinib ko\'ring.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Floating button */}
      <button
        onClick={() => setOpen(o => !o)}
        style={{
          position: 'fixed', bottom: 28, right: 28, zIndex: 999,
          width: 56, height: 56, borderRadius: '50%',
          background: 'linear-gradient(135deg, #6366f1, #a855f7)',
          border: 'none', cursor: 'pointer',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 24, boxShadow: '0 4px 20px rgba(99,102,241,0.5)',
          transition: 'transform 0.2s',
        }}
        title="AI Tutor"
      >
        {open ? '✕' : '🤖'}
      </button>

      {/* Chat window */}
      {open && (
        <div style={{
          position: 'fixed', bottom: 96, right: 28, zIndex: 998,
          width: 360, height: 480,
          background: 'var(--surface)', border: '1px solid var(--border)',
          borderRadius: 20, display: 'flex', flexDirection: 'column',
          boxShadow: '0 16px 48px rgba(0,0,0,0.4)',
          overflow: 'hidden',
        }}>
          {/* Header */}
          <div style={{
            padding: '14px 18px',
            background: 'linear-gradient(135deg, rgba(99,102,241,0.2), rgba(168,85,247,0.2))',
            borderBottom: '1px solid var(--border)',
            display: 'flex', alignItems: 'center', gap: 10,
          }}>
            <span style={{ fontSize: 20 }}>🤖</span>
            <div>
              <div style={{ fontWeight: 700, fontSize: 14 }}>AI Python Tutor</div>
              <div style={{ fontSize: 11, color: 'var(--text-tertiary)' }}>
                Savol bering — javob beraman
              </div>
            </div>
          </div>

          {/* Messages */}
          <div style={{ flex: 1, overflowY: 'auto', padding: '16px 14px' }}>
            {history.length === 0 && (
              <div style={{ textAlign: 'center', color: 'var(--text-tertiary)', fontSize: 13, marginTop: 40 }}>
                <div style={{ fontSize: 36, marginBottom: 12 }}>💬</div>
                <p>Python bo'yicha savolingiz bormi?</p>
                <p style={{ fontSize: 11 }}>Masalan: "list va tuple farqi nima?"</p>
              </div>
            )}
            {history.map((h, i) => (
              <div key={i} style={{
                display: 'flex',
                justifyContent: h.role === 'user' ? 'flex-end' : 'flex-start',
                marginBottom: 10,
              }}>
                <div style={{
                  maxWidth: '85%',
                  padding: '10px 14px', borderRadius: h.role === 'user' ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
                  background: h.role === 'user'
                    ? 'linear-gradient(135deg, #6366f1, #a855f7)'
                    : 'var(--surface-2, #1e2035)',
                  color: 'var(--text-primary)', fontSize: 13, lineHeight: 1.6,
                  border: h.role === 'user' ? 'none' : '1px solid var(--border)',
                  whiteSpace: 'pre-wrap',
                }}>
                  {h.content}
                </div>
              </div>
            ))}
            {loading && (
              <div style={{ display: 'flex', justifyContent: 'flex-start', marginBottom: 10 }}>
                <div style={{
                  padding: '10px 16px', borderRadius: '16px 16px 16px 4px',
                  background: 'var(--surface-2, #1e2035)', border: '1px solid var(--border)',
                  fontSize: 18, letterSpacing: 2,
                }}>
                  ···
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div style={{
            padding: '12px 14px', borderTop: '1px solid var(--border)',
            display: 'flex', gap: 8,
          }}>
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && !e.shiftKey && send()}
              placeholder="Savol yozing..."
              style={{
                flex: 1, padding: '9px 14px', borderRadius: 12,
                background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border)',
                color: 'var(--text-primary)', fontSize: 13, outline: 'none',
              }}
            />
            <button
              onClick={send}
              disabled={loading || !input.trim()}
              style={{
                width: 38, height: 38, borderRadius: 10, border: 'none',
                background: 'linear-gradient(135deg, #6366f1, #a855f7)',
                color: '#fff', cursor: 'pointer', fontSize: 16,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                opacity: loading || !input.trim() ? 0.5 : 1,
              }}
            >
              ➤
            </button>
          </div>
        </div>
      )}
    </>
  );
}
