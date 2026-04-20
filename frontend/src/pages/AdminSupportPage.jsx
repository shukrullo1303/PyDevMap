import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function AdminSupportPage() {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [messages, setMessages]     = useState([]);
    const [loading, setLoading]       = useState(true);
    const [selected, setSelected]     = useState(null);  // selected message
    const [replyText, setReplyText]   = useState('');
    const [sending, setSending]       = useState(false);
    const [toast, setToast]           = useState(null);
    const [filter, setFilter]         = useState('all'); // all | unread | replied

    const showToast = (msg, ok = true) => {
        setToast({ msg, ok });
        setTimeout(() => setToast(null), 3000);
    };

    const load = async () => {
        try {
            const res = await api.get('/support/admin/');
            setMessages(res.data);
        } catch {
            showToast('Xabarlarni yuklashda xatolik', false);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (!user?.is_staff) { navigate('/'); return; }
        load();
    }, [user]);

    const handleReply = async () => {
        if (!replyText.trim() || !selected || sending) return;
        setSending(true);
        try {
            const res = await api.post('/support/' + selected.id + '/reply/', { reply: replyText });
            setMessages(m => m.map(msg => msg.id === selected.id ? res.data : msg));
            setSelected(res.data);
            setReplyText('');
            showToast('Javob yuborildi!');
        } catch {
            showToast('Xatolik yuz berdi', false);
        } finally {
            setSending(false);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm('Xabarni o\'chirishni xohlaysizmi?')) return;
        try {
            await api.delete('/support/' + id + '/reply/');
            setMessages(m => m.filter(msg => msg.id !== id));
            if (selected?.id === id) setSelected(null);
            showToast('Xabar o\'chirildi');
        } catch {
            showToast('O\'chirishda xatolik', false);
        }
    };

    const filtered = messages.filter(m => {
        if (filter === 'unread') return !m.is_read;
        if (filter === 'replied') return !!m.reply;
        return true;
    });

    const unreadCount = messages.filter(m => !m.is_read).length;

    if (!user?.is_staff) return null;

    return (
        <div className="site-container" style={{ maxWidth: 1100, margin: '0 auto', paddingTop: 24 }}>
            {/* Toast */}
            {toast && (
                <div style={{
                    position: 'fixed', top: 80, left: '50%', transform: 'translateX(-50%)',
                    background: toast.ok ? '#22c55e' : '#ef4444', color: '#fff',
                    padding: '11px 22px', borderRadius: 10, fontWeight: 700,
                    fontSize: 14, zIndex: 9999,
                }}>
                    {toast.ok ? '✓' : '✗'} {toast.msg}
                </div>
            )}

            {/* Header */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 }}>
                <div>
                    <h1 style={{ margin: 0, fontSize: 24, fontWeight: 800 }}>🛠 Yordam xabarlari</h1>
                    <p style={{ margin: '4px 0 0', color: 'var(--text-tertiary)', fontSize: 14 }}>
                        Foydalanuvchilardan kelgan muammo va takliflar
                    </p>
                </div>
                <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                    {unreadCount > 0 && (
                        <span style={{
                            background: '#ef4444', color: '#fff',
                            padding: '3px 10px', borderRadius: 20, fontSize: 13, fontWeight: 700,
                        }}>
                            {unreadCount} yangi
                        </span>
                    )}
                    <button
                        onClick={() => navigate('/profile')}
                        className="btn btn-outline-secondary"
                        style={{ fontSize: 13 }}
                    >
                        ← Orqaga
                    </button>
                </div>
            </div>

            {/* Filter tabs */}
            <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
                {[['all', 'Barchasi'], ['unread', 'O\'qilmagan'], ['replied', 'Javob berilgan']].map(([key, label]) => (
                    <button
                        key={key}
                        onClick={() => setFilter(key)}
                        style={{
                            padding: '6px 14px', borderRadius: 8, fontSize: 13, fontWeight: 600,
                            border: filter === key ? 'none' : '1px solid var(--border)',
                            background: filter === key ? 'linear-gradient(135deg, #6366f1, #a855f7)' : 'transparent',
                            color: filter === key ? '#fff' : 'var(--text-secondary)', cursor: 'pointer',
                        }}
                    >
                        {label}
                    </button>
                ))}
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '340px 1fr', gap: 20, alignItems: 'start' }}>
                {/* LEFT: message list */}
                <div style={{
                    background: 'var(--surface)', border: '1px solid var(--border)',
                    borderRadius: 14, overflow: 'hidden',
                }}>
                    {loading ? (
                        <div style={{ padding: 32, textAlign: 'center', color: 'var(--text-tertiary)' }}>Yuklanmoqda...</div>
                    ) : filtered.length === 0 ? (
                        <div style={{ padding: 32, textAlign: 'center', color: 'var(--text-tertiary)' }}>
                            <div style={{ fontSize: 32, marginBottom: 8 }}>📭</div>
                            <p style={{ margin: 0, fontSize: 14 }}>Xabarlar yo'q</p>
                        </div>
                    ) : (
                        filtered.map(msg => (
                            <div
                                key={msg.id}
                                onClick={() => { setSelected(msg); setReplyText(msg.reply || ''); }}
                                style={{
                                    padding: '14px 16px',
                                    borderBottom: '1px solid var(--border)',
                                    cursor: 'pointer',
                                    background: selected?.id === msg.id
                                        ? 'rgba(99,102,241,0.1)'
                                        : !msg.is_read ? 'rgba(239,68,68,0.05)' : 'transparent',
                                    transition: 'background 0.15s',
                                }}
                            >
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 5 }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                        <div style={{
                                            width: 30, height: 30, borderRadius: '50%',
                                            background: 'linear-gradient(135deg, #6366f1, #a855f7)',
                                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                                            fontSize: 13, fontWeight: 700, color: '#fff', flexShrink: 0,
                                        }}>
                                            {(msg.username || 'U')[0].toUpperCase()}
                                        </div>
                                        <div>
                                            <div style={{ fontWeight: 700, fontSize: 13, color: 'var(--text-primary)' }}>{msg.username}</div>
                                            <div style={{ fontSize: 11, color: 'var(--text-tertiary)' }}>
                                                {new Date(msg.created_at).toLocaleString()}
                                            </div>
                                        </div>
                                    </div>
                                    <div style={{ display: 'flex', gap: 4 }}>
                                        {!msg.is_read && (
                                            <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#ef4444', display: 'block', marginTop: 4 }} />
                                        )}
                                        {msg.reply && (
                                            <span style={{ fontSize: 10, background: '#22c55e22', color: '#22c55e', padding: '2px 6px', borderRadius: 6, fontWeight: 600 }}>javob</span>
                                        )}
                                    </div>
                                </div>
                                <div style={{
                                    fontSize: 13, color: 'var(--text-secondary)',
                                    overflow: 'hidden', whiteSpace: 'nowrap', textOverflow: 'ellipsis',
                                }}>
                                    {msg.message}
                                </div>
                            </div>
                        ))
                    )}
                </div>

                {/* RIGHT: selected message detail */}
                {selected ? (
                    <div style={{
                        background: 'var(--surface)', border: '1px solid var(--border)',
                        borderRadius: 14, padding: '24px',
                    }}>
                        {/* User info */}
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                                <div style={{
                                    width: 40, height: 40, borderRadius: '50%',
                                    background: 'linear-gradient(135deg, #6366f1, #a855f7)',
                                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                                    fontSize: 17, fontWeight: 700, color: '#fff',
                                }}>
                                    {(selected.username || 'U')[0].toUpperCase()}
                                </div>
                                <div>
                                    <div style={{ fontWeight: 700 }}>{selected.username}</div>
                                    <div style={{ fontSize: 12, color: 'var(--text-tertiary)' }}>
                                        {new Date(selected.created_at).toLocaleString()}
                                    </div>
                                </div>
                            </div>
                            <button
                                onClick={() => handleDelete(selected.id)}
                                style={{
                                    background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)',
                                    color: '#ef4444', borderRadius: 8, padding: '6px 12px',
                                    fontSize: 13, cursor: 'pointer', fontWeight: 600,
                                }}
                            >
                                O'chirish
                            </button>
                        </div>

                        {/* Message */}
                        <div style={{
                            background: 'var(--bg)', border: '1px solid var(--border)',
                            borderRadius: 12, padding: '16px', marginBottom: 20,
                            fontSize: 15, lineHeight: 1.7, color: 'var(--text-primary)',
                            whiteSpace: 'pre-wrap',
                        }}>
                            {selected.message}
                        </div>

                        {/* Reply form */}
                        <div>
                            <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-tertiary)', marginBottom: 8, display: 'block' }}>
                                {selected.reply ? 'JAVOBNI TAHRIRLASH' : 'JAVOB YOZISH'}
                            </label>
                            <textarea
                                value={replyText}
                                onChange={e => setReplyText(e.target.value)}
                                rows={4}
                                placeholder="Javobingizni yozing..."
                                style={{
                                    width: '100%', padding: '12px 14px', borderRadius: 10, fontSize: 14,
                                    background: 'var(--bg)', border: '1px solid var(--border)',
                                    color: 'var(--text-primary)', outline: 'none', resize: 'vertical',
                                    boxSizing: 'border-box', marginBottom: 12,
                                }}
                            />
                            <button
                                onClick={handleReply}
                                disabled={sending || !replyText.trim()}
                                className="btn btn-primary"
                                style={{ padding: '10px 24px', fontWeight: 700 }}
                            >
                                {sending ? 'Yuborilmoqda...' : selected.reply ? 'Javobni yangilash' : 'Javob yuborish'}
                            </button>
                        </div>

                        {/* Existing reply preview */}
                        {selected.reply && (
                            <div style={{
                                marginTop: 16, background: 'rgba(34,197,94,0.08)',
                                border: '1px solid rgba(34,197,94,0.2)',
                                borderRadius: 10, padding: '14px',
                            }}>
                                <div style={{ fontSize: 11, color: '#22c55e', fontWeight: 700, marginBottom: 6 }}>
                                    ✓ YUBORILGAN JAVOB • {selected.replied_at ? new Date(selected.replied_at).toLocaleString() : ''}
                                </div>
                                <div style={{ fontSize: 14, color: 'var(--text-primary)', whiteSpace: 'pre-wrap' }}>
                                    {selected.reply}
                                </div>
                            </div>
                        )}
                    </div>
                ) : (
                    <div style={{
                        background: 'var(--surface)', border: '1px solid var(--border)',
                        borderRadius: 14, padding: '60px 32px', textAlign: 'center',
                        color: 'var(--text-tertiary)',
                    }}>
                        <div style={{ fontSize: 48, marginBottom: 12 }}>✉️</div>
                        <p style={{ fontSize: 15 }}>Xabarni tanlang</p>
                    </div>
                )}
            </div>
        </div>
    );
}
