import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const QUICK_PROMPTS = [
    { label: 'Web dasturchi', msg: "Web dasturlashni o'rganmoqchiman, qayerdan boshlayman?" },
    { label: 'Data analitik', msg: "Data analitik bo'lmoqchiman, nima o'rganishim kerak?" },
    { label: 'ML / AI', msg: "Machine Learning va AI yo'nalishida ishlamoqchiman" },
    { label: 'Backend', msg: "Backend dasturchi bo'lmoqchiman, Django o'rganmoqchiman" },
    { label: 'Avtomatlashtirish', msg: "Python bilan ish jarayonlarini avtomatlashtirmoqchiman" },
    { label: 'Kiberhavfsizlik', msg: "Kiberhavfsizlik yo'nalishini o'rganmoqchiman" },
    { label: 'O\'yin dasturlash', msg: "Python bilan o'yin yaratmoqchiman" },
    { label: 'Moliya/Fintech', msg: "Moliya va algoritmik savdo uchun Python o'rganmoqchiman" },
];

const LEVEL_COLORS = {
    beginner:     '#22c55e',
    intermediate: '#e8b84b',
    advanced:     '#ef4444',
    Beginner:     '#22c55e',
    Intermediate: '#e8b84b',
    Advanced:     '#ef4444',
};

export default function AiAdvisorPage() {
    const navigate = useNavigate();
    const [input, setInput]     = useState('');
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);
    const [courses, setCourses] = useState([]);
    const [roadmap, setRoadmap] = useState([]);
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [history]);

    const send = async (msg) => {
        const text = (msg || input).trim();
        if (!text || loading) return;
        setInput('');
        const newHist = [...history, { role: 'user', content: text }];
        setHistory(newHist);
        setLoading(true);
        try {
            const res = await api.post('/ai/advisor/', {
                message: text,
                history: newHist.slice(-6),
            });
            setHistory(h => [...h, { role: 'assistant', content: res.data.reply }]);
            if (res.data.recommended_courses?.length) setCourses(res.data.recommended_courses);
            if (res.data.roadmap?.length) setRoadmap(res.data.roadmap);
        } catch {
            setHistory(h => [...h, { role: 'assistant', content: "Xatolik yuz berdi. Qaytadan urinib ko'ring." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="site-container" style={{ maxWidth: 1100, margin: '0 auto', paddingTop: 32 }}>
            {/* Header */}
            <div style={{ marginBottom: 28 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 8 }}>
                    <div style={{
                        width: 48, height: 48, borderRadius: 14,
                        background: 'linear-gradient(135deg, #6366f1, #a855f7)',
                        display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 24,
                    }}>🤖</div>
                    <div>
                        <h1 style={{ margin: 0, fontSize: 26, fontWeight: 800 }}>AI Karyera Maslahatchisi</h1>
                        <p style={{ margin: 0, color: 'var(--text-tertiary)', fontSize: 14 }}>
                            Maqsadingizni ayting — yo'nalish va kurslar tavsiya qilamiz
                        </p>
                    </div>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: 24, alignItems: 'start' }}>
                {/* LEFT: Chat */}
                <div>
                    {/* Quick prompts */}
                    {history.length === 0 && (
                        <div style={{ marginBottom: 20 }}>
                            <p style={{ color: 'var(--text-tertiary)', fontSize: 13, marginBottom: 12 }}>
                                Tez boshlash uchun tanlang:
                            </p>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                                {QUICK_PROMPTS.map(q => (
                                    <button
                                        key={q.label}
                                        onClick={() => send(q.msg)}
                                        style={{
                                            padding: '8px 16px', borderRadius: 20, fontSize: 13,
                                            background: 'var(--surface)',
                                            border: '1px solid var(--border)',
                                            color: 'var(--text-secondary)', cursor: 'pointer',
                                            transition: 'all 0.15s',
                                        }}
                                        onMouseEnter={e => {
                                            e.currentTarget.style.borderColor = '#a855f7';
                                            e.currentTarget.style.color = '#a855f7';
                                        }}
                                        onMouseLeave={e => {
                                            e.currentTarget.style.borderColor = 'var(--border)';
                                            e.currentTarget.style.color = 'var(--text-secondary)';
                                        }}
                                    >
                                        {q.label}
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Messages */}
                    <div style={{
                        background: 'var(--surface)', border: '1px solid var(--border)',
                        borderRadius: 16, minHeight: 360, maxHeight: 500,
                        overflowY: 'auto', padding: '20px 16px',
                        marginBottom: 16,
                    }}>
                        {history.length === 0 ? (
                            <div style={{ textAlign: 'center', color: 'var(--text-tertiary)', marginTop: 60 }}>
                                <div style={{ fontSize: 48, marginBottom: 12 }}>💬</div>
                                <p style={{ fontSize: 15 }}>Maqsadingizni yozing yoki yuqoridan tanlang</p>
                                <p style={{ fontSize: 13 }}>Masalan: "Backend dasturchi bo'lmoqchiman"</p>
                            </div>
                        ) : (
                            history.map((h, i) => (
                                <div key={i} style={{
                                    display: 'flex',
                                    justifyContent: h.role === 'user' ? 'flex-end' : 'flex-start',
                                    marginBottom: 14,
                                }}>
                                    {h.role === 'assistant' && (
                                        <div style={{
                                            width: 32, height: 32, borderRadius: 8, flexShrink: 0,
                                            background: 'linear-gradient(135deg, #6366f1, #a855f7)',
                                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                                            fontSize: 16, marginRight: 10, marginTop: 2,
                                        }}>🤖</div>
                                    )}
                                    <div style={{
                                        maxWidth: '78%',
                                        padding: '12px 16px',
                                        borderRadius: h.role === 'user' ? '16px 16px 4px 16px' : '4px 16px 16px 16px',
                                        background: h.role === 'user'
                                            ? 'linear-gradient(135deg, #6366f1, #a855f7)'
                                            : 'rgba(255,255,255,0.04)',
                                        border: h.role === 'user' ? 'none' : '1px solid var(--border)',
                                        color: 'var(--text-primary)',
                                        fontSize: 14, lineHeight: 1.7,
                                        whiteSpace: 'pre-wrap',
                                    }}>
                                        {h.content}
                                    </div>
                                </div>
                            ))
                        )}
                        {loading && (
                            <div style={{ display: 'flex', gap: 10, alignItems: 'center', padding: '8px 0' }}>
                                <div style={{
                                    width: 32, height: 32, borderRadius: 8,
                                    background: 'linear-gradient(135deg, #6366f1, #a855f7)',
                                    display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 16,
                                }}>🤖</div>
                                <div style={{
                                    padding: '10px 16px', borderRadius: '4px 16px 16px 16px',
                                    background: 'rgba(255,255,255,0.04)', border: '1px solid var(--border)',
                                    fontSize: 18, letterSpacing: 4, color: 'var(--text-tertiary)',
                                }}>···</div>
                            </div>
                        )}
                        <div ref={bottomRef} />
                    </div>

                    {/* Input */}
                    <div style={{ display: 'flex', gap: 10 }}>
                        <input
                            value={input}
                            onChange={e => setInput(e.target.value)}
                            onKeyDown={e => e.key === 'Enter' && !e.shiftKey && send()}
                            placeholder="Maqsadingizni yozing..."
                            style={{
                                flex: 1, padding: '12px 18px', borderRadius: 12,
                                background: 'var(--surface)', border: '1px solid var(--border)',
                                color: 'var(--text-primary)', fontSize: 14, outline: 'none',
                            }}
                        />
                        <button
                            onClick={() => send()}
                            disabled={loading || !input.trim()}
                            className="btn btn-primary"
                            style={{
                                padding: '12px 20px', borderRadius: 12,
                                background: 'linear-gradient(135deg, #6366f1, #a855f7)',
                                border: 'none', fontWeight: 700, opacity: loading || !input.trim() ? 0.5 : 1,
                            }}
                        >
                            Yuborish
                        </button>
                    </div>
                </div>

                {/* RIGHT: Roadmap + Kurslar */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
                    {/* Roadmap */}
                    {roadmap.length > 0 && (
                        <div style={{
                            background: 'var(--surface)', border: '1px solid var(--border)',
                            borderRadius: 16, padding: '20px 20px',
                        }}>
                            <h4 style={{ margin: '0 0 16px', fontSize: 15, fontWeight: 700 }}>
                                📍 O'rganish yo'l xaritasi
                            </h4>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
                                {roadmap.map((step, i) => (
                                    <div key={i} style={{ display: 'flex', gap: 12, paddingBottom: 14 }}>
                                        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                                            <div style={{
                                                width: 28, height: 28, borderRadius: '50%', flexShrink: 0,
                                                background: 'linear-gradient(135deg, #6366f1, #a855f7)',
                                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                                fontSize: 12, fontWeight: 700, color: '#fff',
                                            }}>
                                                {i + 1}
                                            </div>
                                            {i < roadmap.length - 1 && (
                                                <div style={{ width: 2, flex: 1, background: 'var(--border)', marginTop: 4 }} />
                                            )}
                                        </div>
                                        <div style={{ paddingTop: 4, fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                                            {step}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Tavsiya kurslar */}
                    {courses.length > 0 && (
                        <div style={{
                            background: 'var(--surface)', border: '1px solid var(--border)',
                            borderRadius: 16, padding: '20px',
                        }}>
                            <h4 style={{ margin: '0 0 14px', fontSize: 15, fontWeight: 700 }}>
                                🎓 Tavsiya qilingan kurslar
                            </h4>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                                {courses.map(c => (
                                    <div
                                        key={c.id}
                                        onClick={() => navigate('/courses/' + c.id)}
                                        style={{
                                            padding: '12px 14px', borderRadius: 10, cursor: 'pointer',
                                            border: '1px solid var(--border)',
                                            background: 'rgba(255,255,255,0.02)',
                                            transition: 'border-color 0.15s, background 0.15s',
                                        }}
                                        onMouseEnter={e => {
                                            e.currentTarget.style.borderColor = '#6366f1';
                                            e.currentTarget.style.background = 'rgba(99,102,241,0.07)';
                                        }}
                                        onMouseLeave={e => {
                                            e.currentTarget.style.borderColor = 'var(--border)';
                                            e.currentTarget.style.background = 'rgba(255,255,255,0.02)';
                                        }}
                                    >
                                        <div style={{ fontWeight: 600, fontSize: 13, marginBottom: 5, color: 'var(--text-primary)' }}>
                                            {c.title}
                                        </div>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                            <span style={{
                                                fontSize: 11, padding: '2px 8px', borderRadius: 10,
                                                background: (LEVEL_COLORS[c.level] || '#22c55e') + '22',
                                                color: LEVEL_COLORS[c.level] || '#22c55e', fontWeight: 600,
                                            }}>
                                                {c.level}
                                            </span>
                                            <span style={{ fontSize: 12, color: 'var(--primary-400)', fontWeight: 700 }}>
                                                {c.is_free || !Number(c.price) ? 'Bepul' : Number(c.price).toLocaleString('fr-FR') + " so'm"}
                                            </span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Placeholder */}
                    {courses.length === 0 && roadmap.length === 0 && (
                        <div style={{
                            background: 'var(--surface)', border: '1px solid var(--border)',
                            borderRadius: 16, padding: '32px 20px', textAlign: 'center',
                            color: 'var(--text-tertiary)',
                        }}>
                            <div style={{ fontSize: 36, marginBottom: 12 }}>🗺️</div>
                            <p style={{ fontSize: 13, margin: 0 }}>
                                Savol bering — yo'l xaritasi va tavsiya qilingan kurslar shu yerda chiqadi
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
