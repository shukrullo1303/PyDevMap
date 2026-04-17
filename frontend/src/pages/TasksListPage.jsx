import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getTasks } from '../services/compiler';

const DIFF_CONFIG = {
    Beginner:     { color: '#22c55e', bg: 'rgba(34,197,94,0.12)',  label: "Beginner"     },
    Intermediate: { color: '#e8b84b', bg: 'rgba(232,184,75,0.12)', label: "Intermediate" },
    Professional: { color: '#ef4444', bg: 'rgba(239,68,68,0.12)',  label: "Professional" },
};

const DIFFS = ['Hammasi', 'Beginner', 'Intermediate', 'Professional'];

const DiffBadge = ({ difficulty }) => {
    const cfg = DIFF_CONFIG[difficulty] || { color: '#9a9cb0', bg: 'rgba(154,156,176,0.12)', label: difficulty };
    return (
        <span style={{
            display: 'inline-flex', alignItems: 'center', gap: 5,
            padding: '2px 10px', borderRadius: 999,
            fontSize: 12, fontWeight: 600,
            color: cfg.color, background: cfg.bg,
            border: `1px solid ${cfg.color}40`,
        }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: cfg.color, display: 'inline-block' }} />
            {cfg.label}
        </span>
    );
};

export default function TasksListPage() {
    const [tasks, setTasks]   = useState([]);
    const [loading, setLoading] = useState(true);
    const [diff, setDiff]     = useState('Hammasi');
    const [search, setSearch] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        getTasks()
            .then(r => { setTasks(r.data); setLoading(false); })
            .catch(() => { setTasks([]); setLoading(false); });
    }, []);

    const filtered = tasks.filter(t => {
        const matchD = diff === 'Hammasi' || t.difficulty === diff;
        const matchS = !search.trim() || t.title.toLowerCase().includes(search.toLowerCase());
        return matchD && matchS;
    });

    const counts = {
        Beginner:     tasks.filter(t => t.difficulty === 'Beginner').length,
        Intermediate: tasks.filter(t => t.difficulty === 'Intermediate').length,
        Professional: tasks.filter(t => t.difficulty === 'Professional').length,
    };

    return (
        <div className="site-container">
            {/* Header */}
            <div style={{ marginBottom: 32 }}>
                <h1 style={{ marginBottom: 8, display: 'flex', alignItems: 'center', gap: 12 }}>
                    <span style={{
                        width: 42, height: 42, borderRadius: 10,
                        background: 'linear-gradient(135deg,#e8b84b,#f0c85a)',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: 20,
                    }}>⚡</span>
                    Masalalar
                </h1>
                <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
                    Python masalalarini yeching va AI tahlilini oling
                </p>

                {/* Stats */}
                <div style={{ display: 'flex', gap: 16, marginTop: 20, flexWrap: 'wrap' }}>
                    {Object.entries(counts).map(([d, n]) => {
                        const cfg = DIFF_CONFIG[d];
                        return (
                            <div key={d} style={{
                                background: 'var(--surface)',
                                border: '1px solid var(--border)',
                                borderRadius: 10, padding: '10px 18px',
                                display: 'flex', alignItems: 'center', gap: 10,
                            }}>
                                <span style={{ width: 8, height: 8, borderRadius: '50%', background: cfg.color }} />
                                <span style={{ fontSize: 13, color: 'var(--text-secondary)' }}>{cfg.label}</span>
                                <span style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{n}</span>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* Filters */}
            <div style={{ display: 'flex', gap: 12, marginBottom: 24, flexWrap: 'wrap', alignItems: 'center' }}>
                <div style={{ position: 'relative', flex: 1, minWidth: 200, maxWidth: 360 }}>
                    <span style={{
                        position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)',
                        color: 'var(--text-tertiary)', fontSize: 15, pointerEvents: 'none',
                    }}>🔍</span>
                    <input
                        className="form-control"
                        placeholder="Masala qidirish..."
                        value={search}
                        onChange={e => setSearch(e.target.value)}
                        style={{ paddingLeft: 38 }}
                    />
                </div>
                <div style={{ display: 'flex', gap: 6 }}>
                    {DIFFS.map(d => (
                        <button key={d}
                            className={`filter-btn ${diff === d ? 'active' : ''}`}
                            onClick={() => setDiff(d)}
                        >{d}</button>
                    ))}
                </div>
            </div>

            {/* Table */}
            {loading ? (
                <div className="loading-state"><div className="loading-spinner" /><p>Yuklanmoqda...</p></div>
            ) : filtered.length === 0 ? (
                <div className="empty-state"><p>Masala topilmadi</p></div>
            ) : (
                <div style={{
                    background: 'var(--surface)',
                    border: '1px solid var(--border)',
                    borderRadius: 12, overflow: 'hidden',
                }}>
                    {/* Table header */}
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: '50px 1fr 140px 100px',
                        padding: '10px 20px',
                        borderBottom: '1px solid var(--border)',
                        fontSize: 12, fontWeight: 600,
                        color: 'var(--text-tertiary)',
                        textTransform: 'uppercase', letterSpacing: '0.5px',
                    }}>
                        <span>#</span>
                        <span>Masala</span>
                        <span>Qiyinlik</span>
                        <span></span>
                    </div>

                    {filtered.map((task, idx) => (
                        <div key={task.id}
                            onClick={() => navigate(`/tasks/${task.id}`)}
                            style={{
                                display: 'grid',
                                gridTemplateColumns: '50px 1fr 140px 100px',
                                padding: '14px 20px',
                                borderBottom: idx < filtered.length - 1 ? '1px solid var(--border)' : 'none',
                                cursor: 'pointer',
                                transition: 'background 0.15s',
                                alignItems: 'center',
                            }}
                            onMouseEnter={e => e.currentTarget.style.background = 'var(--surface-2)'}
                            onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
                        >
                            <span style={{ color: 'var(--text-tertiary)', fontSize: 13 }}>
                                {idx + 1}
                            </span>
                            <span style={{ fontWeight: 500, color: 'var(--text-primary)', fontSize: 14 }}>
                                {task.title}
                            </span>
                            <DiffBadge difficulty={task.difficulty} />
                            <button
                                className="btn btn-primary btn-sm"
                                onClick={e => { e.stopPropagation(); navigate(`/tasks/${task.id}`); }}
                            >
                                Yechish
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
