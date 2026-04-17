import React, { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getTask, submitCode, analyzeCode } from '../services/compiler';

// ─── Difficulty badge ─────────────────────────────────────
const DIFF = {
    Beginner:     { color: '#22c55e', label: "Beginner"     },
    Intermediate: { color: '#e8b84b', label: "Intermediate" },
    Professional: { color: '#ef4444', label: "Professional" },
};

const DiffBadge = ({ d }) => {
    const cfg = DIFF[d] || { color: '#9a9cb0', label: d };
    return (
        <span style={{
            display: 'inline-flex', alignItems: 'center', gap: 5,
            padding: '3px 12px', borderRadius: 999, fontSize: 12, fontWeight: 600,
            color: cfg.color, background: `${cfg.color}18`,
            border: `1px solid ${cfg.color}40`,
        }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: cfg.color }} />
            {cfg.label}
        </span>
    );
};

// ─── Markdown-like renderer (juda oddiy) ──────────────────
function renderDesc(text) {
    if (!text) return null;
    return text.split('\n').map((line, i) => {
        if (line.startsWith('**') && line.endsWith('**')) {
            return <p key={i} style={{ fontWeight: 700, color: 'var(--text-primary)', margin: '12px 0 4px' }}>{line.slice(2, -2)}</p>;
        }
        if (line.startsWith('```') || line === '```') return null;
        if (line.startsWith('- ')) {
            return <li key={i} style={{ color: 'var(--text-secondary)', marginLeft: 16, marginBottom: 2 }}>{line.slice(2)}</li>;
        }
        return <p key={i} style={{ color: 'var(--text-secondary)', margin: '2px 0', lineHeight: 1.7 }}>{line}</p>;
    });
}

// ─── AI tahlil paneli ─────────────────────────────────────
function AIPanel({ analysis, loading }) {
    if (loading) return (
        <div style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', gap: 10, color: 'var(--text-secondary)', fontSize: 13 }}>
            <div className="loading-spinner" style={{ width: 18, height: 18, borderWidth: 2 }} />
            AI tahlil qilinmoqda...
        </div>
    );
    if (!analysis) return null;

    const { is_correct, ai_detection, suggestion } = analysis;

    return (
        <div style={{ borderTop: '1px solid var(--border)' }}>
            {/* Natija baneri */}
            <div style={{
                padding: '14px 20px',
                background: is_correct === true
                    ? 'rgba(34,197,94,0.08)'
                    : is_correct === false
                        ? 'rgba(239,68,68,0.08)'
                        : 'var(--surface-2)',
                borderBottom: '1px solid var(--border)',
                display: 'flex', alignItems: 'center', gap: 12,
            }}>
                <span style={{ fontSize: 22 }}>
                    {is_correct === true ? '✅' : is_correct === false ? '❌' : '🔍'}
                </span>
                <div>
                    <div style={{ fontWeight: 700, fontSize: 15, color: 'var(--text-primary)' }}>
                        {is_correct === true ? 'To\'g\'ri! Natija qabul qilindi'
                            : is_correct === false ? 'Natija noto\'g\'ri'
                                : 'Natija tekshirildi'}
                    </div>
                    <div style={{ fontSize: 12, color: 'var(--text-tertiary)', marginTop: 2 }}>
                        Kutilgan: <code style={{ color: 'var(--primary-600)' }}>{analysis.expected_output}</code>
                        &nbsp;·&nbsp;
                        Sizniki: <code style={{ color: 'var(--text-primary)' }}>{analysis.actual_output || '(bo\'sh)'}</code>
                    </div>
                </div>
            </div>

            {/* AI detection */}
            <div style={{ padding: '14px 20px', borderBottom: '1px solid var(--border)' }}>
                <div style={{ fontSize: 12, fontWeight: 700, color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: 8 }}>
                    Kod tahlili
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
                    <span style={{
                        display: 'inline-flex', alignItems: 'center', gap: 6,
                        padding: '4px 12px', borderRadius: 999, fontSize: 12, fontWeight: 600,
                        color: ai_detection.is_ai_generated ? '#e8b84b' : '#22c55e',
                        background: ai_detection.is_ai_generated ? 'rgba(232,184,75,0.12)' : 'rgba(34,197,94,0.12)',
                        border: `1px solid ${ai_detection.is_ai_generated ? '#e8b84b40' : '#22c55e40'}`,
                    }}>
                        {ai_detection.is_ai_generated ? '🤖 AI yozgan ehtimol' : '✍️ O\'z kodingiz'}
                        &nbsp;({ai_detection.confidence_score}% ishonch)
                    </span>
                </div>
                {ai_detection.reasons.length > 0 && (
                    <div style={{ marginTop: 8 }}>
                        {ai_detection.reasons.map((r, i) => (
                            <div key={i} style={{ fontSize: 12, color: 'var(--text-tertiary)', marginBottom: 2 }}>
                                • {r}
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Tavsiya */}
            {suggestion && (
                <div style={{ padding: '14px 20px' }}>
                    <div style={{ fontSize: 12, fontWeight: 700, color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: 8 }}>
                        Tavsiya
                    </div>
                    <div style={{
                        background: 'var(--surface-2)', border: '1px solid var(--border)',
                        borderLeft: '3px solid var(--primary-600)',
                        borderRadius: 8, padding: '12px 16px',
                        fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.7,
                        whiteSpace: 'pre-wrap',
                    }}>
                        {suggestion}
                    </div>
                </div>
            )}
        </div>
    );
}

// ─── ASOSIY KOMPONENT ─────────────────────────────────────
export default function TaskPage() {
    const { id } = useParams();
    const navigate = useNavigate();
    const editorRef = useRef(null);

    const [task, setTask]           = useState(null);
    const [loading, setLoading]     = useState(true);
    const [code, setCode]           = useState('');
    const [runResult, setRunResult] = useState(null);   // { status, output }
    const [submitting, setSubmitting] = useState(false);
    const [analysis, setAnalysis]   = useState(null);
    const [analysisLoading, setAnalysisLoading] = useState(false);
    const [activeTab, setActiveTab] = useState('description'); // 'description' | 'output'

    useEffect(() => {
        getTask(id)
            .then(r => {
                setTask(r.data);
                setCode(r.data.starter_code || '# Kodingizni shu yerga yozing\n');
                setLoading(false);
            })
            .catch(() => setLoading(false));
    }, [id]);

    const handleSubmit = async () => {
        if (!code.trim()) return;
        setSubmitting(true);
        setAnalysis(null);
        setRunResult(null);
        setActiveTab('output');

        try {
            const res = await submitCode(id, code);
            const { status: s, output, points_earned, is_correct: submitCorrect } = res.data;
            setRunResult({ status: s, output, points_earned, is_correct: submitCorrect });

            // AI tahlil
            setAnalysisLoading(true);
            try {
                const aRes = await analyzeCode(id, code, output || '');
                // Submit is_correct ni ustuvor qo'yamiz (unittest uchun to'g'ri)
                if (submitCorrect !== undefined) {
                    aRes.data.is_correct = submitCorrect;
                }
                setAnalysis(aRes.data);
            } catch { /* AI xato bo'lsa skip */ }
            setAnalysisLoading(false);
        } catch (err) {
            const errMsg = err.response?.data?.error || err.message || 'Server xatosi';
            setRunResult({ status: 'Error', output: errMsg });
        } finally {
            setSubmitting(false);
        }
    };

    // Tab tugmasi stili
    const tabStyle = (active) => ({
        padding: '8px 16px', fontSize: 13, fontWeight: active ? 600 : 500,
        color: active ? 'var(--primary-600)' : 'var(--text-secondary)',
        background: 'transparent', border: 'none',
        borderBottom: active ? '2px solid var(--primary-600)' : '2px solid transparent',
        cursor: 'pointer', transition: 'color 0.15s',
        marginBottom: -1,
    });

    if (loading) return (
        <div className="loading-state" style={{ height: 'calc(100vh - 64px)' }}>
            <div className="loading-spinner" />
            <p>Yuklanmoqda...</p>
        </div>
    );
    if (!task) return (
        <div className="empty-state"><p>Task topilmadi.</p>
            <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={() => navigate('/tasks')}>
                Orqaga
            </button>
        </div>
    );

    return (
        <div style={{ height: 'calc(100vh - 64px)', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
            {/* Top bar */}
            <div style={{
                background: 'var(--surface)', borderBottom: '1px solid var(--border)',
                padding: '0 20px',
                display: 'flex', alignItems: 'center', gap: 12, height: 48, flexShrink: 0,
            }}>
                <button
                    onClick={() => navigate('/tasks')}
                    style={{
                        background: 'none', border: 'none', cursor: 'pointer',
                        color: 'var(--text-secondary)', padding: '4px 8px',
                        borderRadius: 6, fontSize: 20, display: 'flex', alignItems: 'center',
                    }}
                    title="Orqaga"
                >←</button>
                <span style={{ fontWeight: 600, fontSize: 14, color: 'var(--text-primary)', flex: 1 }}>
                    {task.title}
                </span>
                <DiffBadge d={task.difficulty} />
            </div>

            {/* Main layout: Left + Right */}
            <div style={{ flex: 1, display: 'flex', overflow: 'hidden', minHeight: 0 }}>

                {/* ── LEFT PANEL: task description ── */}
                <div style={{
                    width: '42%', minWidth: 320, borderRight: '1px solid var(--border)',
                    display: 'flex', flexDirection: 'column', overflow: 'hidden',
                    background: 'var(--surface)',
                }}>
                    {/* tabs */}
                    <div style={{
                        display: 'flex', borderBottom: '1px solid var(--border)',
                        padding: '0 16px', flexShrink: 0,
                    }}>
                        <button style={tabStyle(activeTab === 'description')} onClick={() => setActiveTab('description')}>
                            Masala
                        </button>
                        <button style={tabStyle(activeTab === 'output')} onClick={() => setActiveTab('output')}>
                            Natija {runResult && <span style={{ marginLeft: 4, width: 6, height: 6, borderRadius: '50%', background: runResult.status === 'Success' ? '#22c55e' : '#ef4444', display: 'inline-block', verticalAlign: 'middle' }} />}
                        </button>
                    </div>

                    {/* content */}
                    <div style={{ flex: 1, overflow: 'auto', padding: 20 }}>
                        {activeTab === 'description' ? (
                            <>
                                <h2 style={{ fontSize: 18, marginBottom: 12 }}>{task.title}</h2>
                                <div style={{ marginBottom: 20 }}>{renderDesc(task.description)}</div>

                                {/* Expected output */}
                                {task.expected_output && (
                                    <div style={{ marginTop: 16 }}>
                                        <div style={{ fontSize: 12, fontWeight: 700, color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: 6 }}>
                                            Kutilgan natija
                                        </div>
                                        <div style={{
                                            background: 'var(--surface-2)', border: '1px solid var(--border)',
                                            borderRadius: 8, padding: '10px 14px',
                                            fontFamily: 'monospace', fontSize: 14,
                                            color: 'var(--primary-600)',
                                        }}>
                                            {task.expected_output}
                                        </div>
                                    </div>
                                )}

                                {/* Hint */}
                                <div style={{
                                    marginTop: 20, padding: '10px 14px',
                                    background: 'rgba(232,184,75,0.06)',
                                    border: '1px solid rgba(232,184,75,0.25)',
                                    borderRadius: 8, fontSize: 12, color: 'var(--text-tertiary)',
                                }}>
                                    💡 <strong>Eslatma:</strong> Funksiya nomi <code style={{ color: 'var(--primary-600)' }}>solve</code> bo'lishi kerak.
                                    Natija <code>print</code> emas, <code>return</code> bilan qaytarilsin.
                                </div>
                            </>
                        ) : (
                            <>
                                {!runResult ? (
                                    <div style={{ textAlign: 'center', paddingTop: 40, color: 'var(--text-tertiary)', fontSize: 14 }}>
                                        <p style={{ fontSize: 36, margin: '0 0 12px' }}>🚀</p>
                                        <p>Kodni topshiring va natijani shu yerda ko'ring</p>
                                    </div>
                                ) : (
                                    <>
                                        <div style={{
                                            display: 'flex', alignItems: 'center', gap: 8,
                                            marginBottom: 12, flexWrap: 'wrap',
                                        }}>
                                            <span style={{ fontSize: 20 }}>
                                                {runResult.status === 'Success' ? '✅' : runResult.status === 'Timeout' ? '⏱️' : '❌'}
                                            </span>
                                            <span style={{
                                                fontWeight: 700, fontSize: 15,
                                                color: runResult.status === 'Success' ? '#22c55e' : '#ef4444',
                                            }}>
                                                {runResult.status === 'Success' ? 'Kod ishladi' : `Xato: ${runResult.status}`}
                                            </span>
                                            {runResult.points_earned > 0 && (
                                                <span style={{
                                                    padding: '2px 10px', borderRadius: 999,
                                                    background: 'rgba(232,184,75,0.15)',
                                                    color: '#e8b84b', fontSize: 12, fontWeight: 700,
                                                    border: '1px solid rgba(232,184,75,0.3)',
                                                }}>
                                                    +{runResult.points_earned} ball
                                                </span>
                                            )}
                                        </div>

                                        {runResult.output && (
                                            <div>
                                                <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: 6 }}>
                                                    Chiqish
                                                </div>
                                                <pre style={{
                                                    background: 'var(--surface-2)', border: '1px solid var(--border)',
                                                    borderRadius: 8, padding: '12px 14px',
                                                    fontFamily: 'monospace', fontSize: 13,
                                                    color: 'var(--text-primary)', margin: 0,
                                                    whiteSpace: 'pre-wrap', wordBreak: 'break-word',
                                                    maxHeight: 200, overflow: 'auto',
                                                }}>
                                                    {runResult.output}
                                                </pre>
                                            </div>
                                        )}

                                        {/* AI panel */}
                                        <div style={{ marginTop: 16, background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10, overflow: 'hidden' }}>
                                            <AIPanel analysis={analysis} loading={analysisLoading} />
                                        </div>
                                    </>
                                )}
                            </>
                        )}
                    </div>
                </div>

                {/* ── RIGHT PANEL: code editor ── */}
                <div style={{
                    flex: 1, display: 'flex', flexDirection: 'column',
                    background: '#0d1117', overflow: 'hidden',
                }}>
                    {/* Editor header */}
                    <div style={{
                        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                        padding: '0 16px', height: 42, flexShrink: 0,
                        borderBottom: '1px solid rgba(255,255,255,0.06)',
                        background: '#161b22',
                    }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                            <span style={{
                                display: 'inline-flex', alignItems: 'center', gap: 6,
                                padding: '2px 10px', borderRadius: 6,
                                background: 'rgba(232,184,75,0.12)',
                                color: '#e8b84b', fontSize: 12, fontWeight: 600,
                            }}>
                                🐍 Python
                            </span>
                        </div>
                        <div style={{ display: 'flex', gap: 8 }}>
                            <button
                                onClick={() => setCode(task.starter_code || '')}
                                style={{
                                    background: 'rgba(255,255,255,0.06)',
                                    border: '1px solid rgba(255,255,255,0.1)',
                                    color: '#9a9cb0', borderRadius: 6,
                                    padding: '4px 12px', fontSize: 12, cursor: 'pointer',
                                }}
                            >
                                Asl ko'rinish
                            </button>
                            <button
                                onClick={handleSubmit}
                                disabled={submitting}
                                style={{
                                    background: submitting ? '#555' : '#22c55e',
                                    border: 'none', color: '#fff',
                                    borderRadius: 6, padding: '4px 16px',
                                    fontSize: 12, fontWeight: 700, cursor: 'pointer',
                                    opacity: submitting ? 0.7 : 1,
                                    display: 'flex', alignItems: 'center', gap: 6,
                                }}
                            >
                                {submitting ? (
                                    <>
                                        <div style={{ width: 12, height: 12, border: '2px solid #fff', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />
                                        Ishlanmoqda...
                                    </>
                                ) : (
                                    <>▶ Topshirish</>
                                )}
                            </button>
                        </div>
                    </div>

                    {/* Code textarea */}
                    <textarea
                        ref={editorRef}
                        value={code}
                        onChange={e => setCode(e.target.value)}
                        onKeyDown={e => {
                            // Tab = 4 bo'sh joy
                            if (e.key === 'Tab') {
                                e.preventDefault();
                                const start = e.target.selectionStart;
                                const end = e.target.selectionEnd;
                                const newCode = code.substring(0, start) + '    ' + code.substring(end);
                                setCode(newCode);
                                setTimeout(() => {
                                    editorRef.current.selectionStart = start + 4;
                                    editorRef.current.selectionEnd = start + 4;
                                }, 0);
                            }
                        }}
                        spellCheck={false}
                        style={{
                            flex: 1, padding: '16px 20px',
                            background: '#0d1117', color: '#e6edf3',
                            border: 'none', outline: 'none',
                            fontFamily: "'Fira Code', 'Cascadia Code', 'Consolas', monospace",
                            fontSize: 14, lineHeight: 1.65,
                            resize: 'none', whiteSpace: 'pre',
                            overflowWrap: 'normal', overflowX: 'auto',
                            tabSize: 4,
                        }}
                    />

                    {/* Bottom status */}
                    <div style={{
                        padding: '6px 16px',
                        background: '#161b22',
                        borderTop: '1px solid rgba(255,255,255,0.06)',
                        display: 'flex', alignItems: 'center', gap: 12,
                        fontSize: 11, color: '#6b7280',
                        flexShrink: 0,
                    }}>
                        <span>Qatorlar: {code.split('\n').length}</span>
                        <span>·</span>
                        <span>Belgilar: {code.length}</span>
                        <span>·</span>
                        <span>Tab — 4 bo'sh joy</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
