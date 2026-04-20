import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import '../styles/pages/AuthPages.css';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError]       = useState(null);
    const [loading, setLoading]   = useState(false);
    const [showTestModal, setShowTestModal] = useState(false);
    const nav = useNavigate();
    const { login } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setLoading(true);
        try {
            await login(username, password);
            // Test o'tilganmi tekshirish
            try {
                const res = await api.get('/placement/result/');
                if (!res.data.has_result) {
                    setShowTestModal(true);
                    return;
                }
            } catch { /* ignore */ }
            nav('/profile');
        } catch (err) {
            setError(err.response?.data?.detail || err.message || 'Login failed');
        } finally {
            setLoading(false);
        }
    };

    if (showTestModal) return (
        <div style={{
            position: 'fixed', inset: 0, zIndex: 1000,
            background: 'rgba(0,0,0,0.75)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            padding: 24,
        }}>
            <div style={{
                background: 'var(--surface)', border: '1px solid var(--border)',
                borderRadius: 20, padding: '40px 36px',
                maxWidth: 460, width: '100%', textAlign: 'center',
                boxShadow: '0 24px 80px rgba(0,0,0,0.4)',
            }}>
                <div style={{ fontSize: 56, marginBottom: 12 }}>🧠</div>
                <h2 style={{ fontSize: 22, fontWeight: 800, marginBottom: 8 }}>
                    Bilimni baholash testi
                </h2>
                <p style={{ color: 'var(--text-secondary)', fontSize: 15, marginBottom: 8 }}>
                    Siz hali darajangizni aniqlamagansiz!
                </p>
                <p style={{ color: 'var(--text-secondary)', fontSize: 14, marginBottom: 8 }}>
                    25 ta savol · 5-7 daqiqa · Adaptiv algoritm
                </p>
                <div style={{
                    background: 'rgba(232,184,75,0.1)', border: '1px solid rgba(232,184,75,0.3)',
                    borderRadius: 10, padding: '10px 18px', marginBottom: 28, display: 'inline-block',
                }}>
                    <span style={{ color: '#e8b84b', fontWeight: 700, fontSize: 14 }}>
                        80%+ natija = 50% chegirma kuponi!
                    </span>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                    <button
                        className="btn btn-primary"
                        style={{
                            fontWeight: 700, fontSize: 15, padding: '13px 0',
                            background: 'linear-gradient(135deg, #6366f1, #a855f7)',
                            border: 'none',
                        }}
                        onClick={() => nav('/placement-test')}
                    >
                        Testni boshlash
                    </button>
                    <button
                        className="btn btn-outline-secondary"
                        style={{ fontSize: 13 }}
                        onClick={() => nav('/profile')}
                    >
                        Keyinroq o'taman
                    </button>
                </div>
            </div>
        </div>
    );

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <h1>Xush kelibsiz</h1>
                    <p>Kirish uchun ma'lumotlaringizni kiriting</p>
                </div>

                {error && (
                    <div className="auth-error">
                        <strong>Xatolik:</strong> {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="form-group">
                        <label className="form-label">Foydalanuvchi nomi</label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="username"
                            className="form-control"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Parol</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="••••••••"
                            className="form-control"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary auth-submit"
                        disabled={loading}
                    >
                        {loading ? 'Kirilmoqda...' : 'Kirish'}
                    </button>
                </form>

                <div className="auth-footer">
                    <p>Akkauntingiz yo'qmi? <Link to="/register">Ro'yxatdan o'ting</Link></p>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
