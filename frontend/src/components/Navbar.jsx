import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { useNavigate } from 'react-router-dom';

const Navigation = () => {
    const { user, logout } = useAuth();
    const { theme, toggle: toggleTheme } = useTheme();
    const nav = useNavigate();
    const location = useLocation();

    const handleLogout = () => { logout(); nav('/'); };
    const isActive = (path) => location.pathname === path;

    return (
        <nav style={{
            background: 'var(--surface)',
            backdropFilter: 'blur(12px)',
            borderBottom: '1px solid var(--border)',
            position: 'sticky', top: 0, zIndex: 50,
            transition: 'background 0.2s, border-color 0.2s',
        }}>
            <div style={{
                maxWidth: 1200, margin: '0 auto',
                padding: '0 24px',
                display: 'flex', alignItems: 'center',
                height: 64, gap: 0,
            }}>
                {/* LEFT: Logo + Nav links */}
                <div style={{ display: 'flex', alignItems: 'center', gap: 4, flex: 1 }}>
                    <Link to="/" style={{
                        display: 'flex', alignItems: 'center', gap: 10,
                        textDecoration: 'none', marginRight: 8,
                    }}>
                        <div style={{
                            width: 34, height: 34,
                            background: 'var(--primary-600)',
                            color: '#0d0f17',
                            borderRadius: 8,
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            fontWeight: 700, fontSize: 13, flexShrink: 0,
                        }}>py</div>
                        <span style={{
                            fontWeight: 700, fontSize: 18,
                            color: 'var(--text-primary)',
                        }}>pyDevMap</span>
                    </Link>

                    {/* Nav links */}
                    <div className="nav-desktop-links">
                        <Link to="/" className={`nav-btn ${isActive('/') ? 'active' : ''}`}>
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                                <polyline points="9 22 9 12 15 12 15 22"/>
                            </svg>
                            Yo'l Xaritasi
                        </Link>
                        <Link to="/courses" className={`nav-btn ${isActive('/courses') ? 'active' : ''}`}>
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
                                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
                            </svg>
                            Kurslar
                        </Link>
                        <Link to="/tasks" className={`nav-btn ${location.pathname.startsWith('/tasks') ? 'active' : ''}`}>
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>
                            </svg>
                            Masalalar
                        </Link>
                        <Link to="/leaderboard" className={`nav-btn ${isActive('/leaderboard') ? 'active' : ''}`}>
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <polyline points="18 20 18 10"/><polyline points="12 20 12 4"/><polyline points="6 20 6 14"/>
                            </svg>
                            Reyting
                        </Link>
                        {user && (
                            <Link to="/placement-test" className={`nav-btn ${isActive('/placement-test') ? 'active' : ''}`} style={{
                                background: isActive('/placement-test') ? undefined : 'linear-gradient(135deg, rgba(99,102,241,0.15), rgba(168,85,247,0.15))',
                                borderColor: 'rgba(168,85,247,0.4)',
                            }}>
                                <span style={{ fontSize: 13 }}>🧠</span>
                                Bilimni baholash
                            </Link>
                        )}
                        {user && (
                            <Link to="/ai-advisor" className={`nav-btn ${isActive('/ai-advisor') ? 'active' : ''}`} style={{
                                background: isActive('/ai-advisor') ? undefined : 'linear-gradient(135deg, rgba(99,102,241,0.15), rgba(168,85,247,0.15))',
                                borderColor: 'rgba(168,85,247,0.4)',
                            }}>
                                <span style={{ fontSize: 13 }}>🤖</span>
                                Maslahatchi
                            </Link>
                        )}
                    </div>
                </div>

                {/* Theme toggle */}
                <button onClick={toggleTheme} title={theme === 'dark' ? 'Light mode' : 'Dark mode'} style={{
                    background: 'none', border: '1px solid var(--border)',
                    borderRadius: 8, width: 34, height: 34,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    cursor: 'pointer', fontSize: 16, flexShrink: 0, marginRight: 4,
                    color: 'var(--text-secondary)',
                }}>
                    {theme === 'dark' ? '☀️' : '🌙'}
                </button>

                {/* RIGHT: auth buttons */}
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0 }}>
                    {user ? (
                        <>
                            <Link to="/profile" style={{
                                display: 'flex', alignItems: 'center', gap: 6,
                                textDecoration: 'none',
                                padding: '5px 12px', borderRadius: 8,
                                border: '1px solid var(--border)',
                                background: 'var(--surface)',
                                fontSize: 13, fontWeight: 500,
                                color: 'var(--text-primary)',
                                whiteSpace: 'nowrap',
                            }}>
                                <span style={{
                                    width: 22, height: 22, borderRadius: '50%',
                                    background: 'var(--primary-600)',
                                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                                    color: '#0d0f17', fontWeight: 700, fontSize: 11, flexShrink: 0,
                                }}>
                                    {user.username?.[0]?.toUpperCase() || 'U'}
                                </span>
                                {user.username || user.email}
                            </Link>
                            <button onClick={handleLogout} style={{
                                background: 'rgba(239,68,68,0.1)',
                                border: '1px solid rgba(239,68,68,0.4)',
                                color: '#ef4444',
                                borderRadius: 8, padding: '5px 12px',
                                fontSize: 13, cursor: 'pointer',
                                whiteSpace: 'nowrap', fontWeight: 600,
                            }}
                            onMouseEnter={e => { e.currentTarget.style.background = '#ef4444'; e.currentTarget.style.color = '#fff'; }}
                            onMouseLeave={e => { e.currentTarget.style.background = 'rgba(239,68,68,0.1)'; e.currentTarget.style.color = '#ef4444'; }}
                            >
                                Chiqish
                            </button>
                        </>
                    ) : (
                        <>
                            <Link to="/login" style={{
                                textDecoration: 'none', padding: '5px 14px', borderRadius: 8,
                                border: '1px solid var(--border)', background: 'var(--surface)',
                                fontSize: 13, fontWeight: 500, color: 'var(--text-primary)',
                                whiteSpace: 'nowrap',
                            }}>Kirish</Link>
                            <Link to="/register" style={{
                                textDecoration: 'none', padding: '5px 14px', borderRadius: 8,
                                background: 'var(--primary-600)', border: '1px solid var(--primary-600)',
                                fontSize: 13, fontWeight: 600, color: '#0d0f17',
                                whiteSpace: 'nowrap',
                            }}>Ro'yxatdan o'tish</Link>
                        </>
                    )}
                </div>

            </div>
        </nav>
    );
};

export default Navigation;
