import React, { useEffect, useState } from 'react';
import api from '../services/api';

const MEDAL = { 1: '🥇', 2: '🥈', 3: '🥉' };

const DIFF_POINTS = [
    { label: 'Beginner', points: 10, color: '#22c55e', bg: 'rgba(34,197,94,0.1)' },
    { label: 'Intermediate', points: 20, color: '#e8b84b', bg: 'rgba(232,184,75,0.1)' },
    { label: 'Professional', points: 30, color: '#ef4444', bg: 'rgba(239,68,68,0.1)' },
];

export default function LeaderboardPage() {
    const [rows, setRows] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get('/compiler/leaderboard/')
            .then(r => { setRows(r.data); setLoading(false); })
            .catch(() => setLoading(false));
    }, []);

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
                    }}>🏆</span>
                    Reyting
                </h1>
                <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
                    Eng ko'p masala yechgan foydalanuvchilar
                </p>

                {/* Ball tizimi */}
                <div style={{ display: 'flex', gap: 10, marginTop: 16, flexWrap: 'wrap' }}>
                    {DIFF_POINTS.map(d => (
                        <div key={d.label} style={{
                            padding: '6px 14px', borderRadius: 8,
                            background: d.bg, border: `1px solid ${d.color}30`,
                            fontSize: 12, color: d.color, fontWeight: 600,
                            display: 'flex', alignItems: 'center', gap: 6,
                        }}>
                            <span style={{ width: 6, height: 6, borderRadius: '50%', background: d.color }} />
                            {d.label} = {d.points} ball
                        </div>
                    ))}
                </div>
            </div>

            {/* Table */}
            {loading ? (
                <div className="loading-state"><div className="loading-spinner" /><p>Yuklanmoqda...</p></div>
            ) : rows.length === 0 ? (
                <div className="empty-state">
                    <p style={{ fontSize: 36, marginBottom: 8 }}>🏁</p>
                    <p>Hali hech kim masala yechmagan.</p>
                    <p style={{ fontSize: 13, color: 'var(--text-tertiary)' }}>Birinchi bo'lib reyting egasi bo'ling!</p>
                </div>
            ) : (
                <div style={{
                    background: 'var(--surface)',
                    border: '1px solid var(--border)',
                    borderRadius: 12, overflow: 'hidden',
                }}>
                    {/* Table header */}
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: '60px 1fr 120px 120px',
                        padding: '10px 20px',
                        borderBottom: '1px solid var(--border)',
                        fontSize: 11, fontWeight: 700,
                        color: 'var(--text-tertiary)',
                        textTransform: 'uppercase', letterSpacing: '0.6px',
                    }}>
                        <span>O'rin</span>
                        <span>Foydalanuvchi</span>
                        <span style={{ textAlign: 'center' }}>Yechilgan</span>
                        <span style={{ textAlign: 'right' }}>Ballar</span>
                    </div>

                    {rows.map((row, idx) => {
                        const isTop3 = row.rank <= 3;
                        return (
                            <div key={row.username} style={{
                                display: 'grid',
                                gridTemplateColumns: '60px 1fr 120px 120px',
                                padding: '14px 20px',
                                borderBottom: idx < rows.length - 1 ? '1px solid var(--border)' : 'none',
                                alignItems: 'center',
                                background: isTop3 ? `rgba(232,184,75,0.0${4 - row.rank})` : 'transparent',
                                transition: 'background 0.15s',
                            }}
                            onMouseEnter={e => e.currentTarget.style.background = 'var(--surface-2)'}
                            onMouseLeave={e => e.currentTarget.style.background = isTop3 ? `rgba(232,184,75,0.0${4 - row.rank})` : 'transparent'}
                            >
                                {/* Rank */}
                                <span style={{ fontSize: isTop3 ? 22 : 14, fontWeight: 700, color: isTop3 ? '#e8b84b' : 'var(--text-tertiary)' }}>
                                    {MEDAL[row.rank] || `#${row.rank}`}
                                </span>

                                {/* User */}
                                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                                    <div style={{
                                        width: 34, height: 34, borderRadius: '50%',
                                        background: isTop3
                                            ? 'linear-gradient(135deg,#e8b84b,#f0c85a)'
                                            : 'var(--surface-2)',
                                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                                        fontWeight: 700, fontSize: 14,
                                        color: isTop3 ? '#0d0f17' : 'var(--text-secondary)',
                                        border: '1px solid var(--border)',
                                        flexShrink: 0,
                                    }}>
                                        {row.username[0].toUpperCase()}
                                    </div>
                                    <span style={{ fontWeight: 600, color: 'var(--text-primary)', fontSize: 14 }}>
                                        {row.username}
                                    </span>
                                </div>

                                {/* Solved */}
                                <span style={{ textAlign: 'center', fontSize: 14, color: 'var(--text-secondary)', fontWeight: 500 }}>
                                    {row.solved_count} ta
                                </span>

                                {/* Points */}
                                <span style={{
                                    textAlign: 'right', fontWeight: 700, fontSize: 16,
                                    color: isTop3 ? '#e8b84b' : 'var(--text-primary)',
                                }}>
                                    {row.total_points}
                                    <span style={{ fontSize: 11, fontWeight: 400, color: 'var(--text-tertiary)', marginLeft: 3 }}>ball</span>
                                </span>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}
