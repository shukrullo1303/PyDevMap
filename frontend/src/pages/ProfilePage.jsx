import api from '../services/api';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProfile } from '../services/auth';
import { getMyEnrollments } from '../services/enrollments';
import '../styles/pages/ProfilePage.css';
import DownloadCertificateButton from '../components/DownloadCertificateButton';

const LEVEL_INFO = {
    beginner:     { label: "Boshlang'ich", color: '#22c55e', emoji: '🌱' },
    intermediate: { label: "O'rta daraja",  color: '#e8b84b', emoji: '📈' },
    advanced:     { label: "Ilg'or",        color: '#3b82f6', emoji: '🚀' },
    expert:       { label: 'Expert',        color: '#a855f7', emoji: '🏆' },
};

const ProfilePage = () => {
    const navigate = useNavigate();
    const [user, setUser]             = useState(null);
    const [enrollments, setEnrollments] = useState([]);
    const [loading, setLoading]       = useState(true);
    const [progress, setProgress]     = useState([]);
    const [testResult, setTestResult] = useState(null); // placement test natijasi

    useEffect(() => {
        const loadProfile = async () => {
            try {
                const profileRes = await getProfile();
                const userData = profileRes.data;
                setUser(userData);

                const enrollRes = await getMyEnrollments(userData.id);
                const enrollList = Array.isArray(enrollRes.data)
                    ? enrollRes.data
                    : enrollRes.data.results || [];
                setEnrollments(enrollList);

                const progressRes = await api.get('/course-progress/');
                setProgress(progressRes.data);

                // Placement test natijasini olish
                try {
                    const testRes = await api.get('/placement/result/');
                    if (testRes.data.has_result) setTestResult(testRes.data);
                } catch { /* test hali o'tilmagan */ }

            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        loadProfile();
    }, []);

    if (loading) {
        return <div className="site-container">
            <div className="loading-state">Profil yuklanmoqda...</div>
        </div>;
    }

    const lvl = testResult ? (LEVEL_INFO[testResult.level] || LEVEL_INFO.beginner) : null;

    return (
        <div className="site-container">
            <div className="profile-layout sidebar">
                <div className="profile-main">

                    {/* ── Bilimni baholash kartasi ── */}
                    {testResult ? (
                        <section className="profile-section" style={{ padding: 0 }}>
                            <div style={{
                                background: 'linear-gradient(135deg, rgba(99,102,241,0.12), rgba(168,85,247,0.12))',
                                border: '1px solid rgba(168,85,247,0.3)',
                                borderRadius: 16, padding: '24px 28px',
                                display: 'flex', alignItems: 'center',
                                justifyContent: 'space-between', flexWrap: 'wrap', gap: 16,
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                                    <div style={{ fontSize: 44 }}>{lvl.emoji}</div>
                                    <div>
                                        <div style={{ fontSize: 12, color: 'var(--text-tertiary)', fontWeight: 600, letterSpacing: 1, textTransform: 'uppercase', marginBottom: 4 }}>
                                            Bilimni baholash natijasi
                                        </div>
                                        <div style={{ fontSize: 22, fontWeight: 800, color: lvl.color }}>
                                            {lvl.label}
                                        </div>
                                        <div style={{ fontSize: 14, color: 'var(--text-secondary)', marginTop: 2 }}>
                                            Ball: <b style={{ color: 'var(--text-primary)' }}>{testResult.percentage}%</b>
                                        </div>
                                    </div>
                                </div>
                                <div style={{ display: 'flex', flexDirection: 'column', gap: 8, alignItems: 'flex-end' }}>
                                    {testResult.coupon && !testResult.coupon.is_used && (
                                        <div style={{
                                            background: 'rgba(232,184,75,0.12)', border: '1.5px dashed #e8b84b',
                                            borderRadius: 10, padding: '8px 16px', textAlign: 'center',
                                        }}>
                                            <div style={{ fontSize: 11, color: 'var(--text-tertiary)', marginBottom: 2 }}>Chegirma kuponingiz</div>
                                            <div style={{ fontSize: 18, fontWeight: 900, color: '#e8b84b', letterSpacing: 2 }}>
                                                {testResult.coupon.code}
                                            </div>
                                            <div style={{ fontSize: 11, color: '#e8b84b' }}>
                                                {testResult.coupon.percentage}% • {testResult.coupon.valid_until} gacha
                                            </div>
                                        </div>
                                    )}
                                    <button
                                        className="btn btn-outline-secondary"
                                        style={{ fontSize: 13 }}
                                        onClick={() => navigate('/placement-test')}
                                    >
                                        Qayta topshirish
                                    </button>
                                </div>
                            </div>
                        </section>
                    ) : (
                        <section className="profile-section" style={{ padding: 0 }}>
                            <div style={{
                                background: 'linear-gradient(135deg, rgba(99,102,241,0.08), rgba(168,85,247,0.08))',
                                border: '2px dashed rgba(168,85,247,0.4)',
                                borderRadius: 16, padding: '28px 32px',
                                display: 'flex', alignItems: 'center',
                                justifyContent: 'space-between', flexWrap: 'wrap', gap: 20,
                            }}>
                                <div>
                                    <div style={{ fontSize: 28, marginBottom: 8 }}>🧠</div>
                                    <h3 style={{ margin: '0 0 6px', fontSize: 18, fontWeight: 800 }}>
                                        Bilimni baholash
                                    </h3>
                                    <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: 14 }}>
                                        25 ta adaptiv savol • Darajangizni aniqlaymiz
                                    </p>
                                    <p style={{ margin: '4px 0 0', color: '#e8b84b', fontSize: 13, fontWeight: 600 }}>
                                        80%+ natija — 50% chegirma kuponi!
                                    </p>
                                </div>
                                <button
                                    className="btn btn-primary"
                                    style={{
                                        padding: '12px 28px', fontWeight: 700, fontSize: 15,
                                        background: 'linear-gradient(135deg, #6366f1, #a855f7)',
                                        border: 'none',
                                    }}
                                    onClick={() => navigate('/placement-test')}
                                >
                                    Testni boshlash
                                </button>
                            </div>
                        </section>
                    )}

                    {/* ── Profil ── */}
                    <section className="profile-section">
                        <h2>Profilim</h2>
                        {user ? (
                            <div className="profile-card">
                                <div className="profile-avatar">
                                    {user.username?.[0]?.toUpperCase() || user.email?.[0]?.toUpperCase() || 'U'}
                                </div>
                                <div className="profile-info">
                                    <h3>{user.username || 'User'}</h3>
                                    <p>{user.first_name} {user.last_name}</p>
                                    <p className="profile-email">{user.email}</p>
                                    <p className="profile-joined">
                                        {new Date(user.date_joined || Date.now()).toLocaleDateString()} sanasida ro'yxatdan o'tgan
                                    </p>
                                </div>
                            </div>
                        ) : (
                            <div className="empty-state">Profil topilmadi!</div>
                        )}
                    </section>

                    {/* ── Kurslar ── */}
                    <section className="profile-section">
                        <h2>Mening kurslarim</h2>
                        {enrollments.length === 0 ? (
                            <div className="empty-state">
                                <p>Ro'yxatdan o'tilgan kurslar topilmadi.</p>
                                <p className="empty-desc">O'zingiz yoqtirgan kurslarni toping va ro'yxatdan o'ting</p>
                            </div>
                        ) : (
                            <div className="enrollments-list">
                                {enrollments.map((e) => {
                                    const courseProgress = progress.find(p => p.course_id === e.course) || { progress: 0 };
                                    const displayTitle = e.course_title || courseProgress.course_title || `Kurs #${e.course}`;
                                    return (
                                        <div key={e.id} className="enrollment-item">
                                            <div className="enrollment-header">
                                                <h4>{displayTitle}</h4>
                                                {courseProgress.progress === 100 ?
                                                    <DownloadCertificateButton courseId={e.course} /> :
                                                    <span className="enrollment-status">Jarayonda</span>
                                                }
                                            </div>
                                            <p className="enrollment-date">
                                                Ro'yxatdan o'tilgan: {new Date(e.created_at).toLocaleDateString()}
                                            </p>
                                            <div className="enrollment-progress">
                                                <div className="progress-bar">
                                                    <div className="progress-fill" style={{ width: `${courseProgress.progress}%` }}></div>
                                                </div>
                                                <small>{courseProgress.progress}% complete</small>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        )}
                    </section>
                </div>

                {/* ── Sidebar ── */}
                <aside className="profile-sidebar">
                    <div className="sidebar-card">
                        <h4>Statistika</h4>
                        <div className="stat-item">
                            <span className="stat-value">{enrollments.length}</span>
                            <span className="stat-label">Ro'yxatdan o'tilgan kurslar</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-value">
                                {progress.filter(p => p.progress === 100).length}
                            </span>
                            <span className="stat-label">Tugatilgan kurslar</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-value">
                                {testResult ? testResult.percentage + '%' : '—'}
                            </span>
                            <span className="stat-label">Bilim darajasi</span>
                        </div>
                    </div>

                    {/* Test natijasi sidebar */}
                    {testResult && testResult.recommended_courses?.length > 0 && (
                        <div className="sidebar-card" style={{ marginTop: 16 }}>
                            <h4 style={{ marginBottom: 14 }}>Tavsiya qilingan kurslar</h4>
                            {testResult.recommended_courses.slice(0, 4).map(c => (
                                <div
                                    key={c.id}
                                    onClick={() => navigate('/courses/' + c.id)}
                                    style={{
                                        padding: '10px 0', borderBottom: '1px solid var(--border)',
                                        cursor: 'pointer', fontSize: 13,
                                        color: 'var(--text-secondary)',
                                        transition: 'color 0.15s',
                                    }}
                                    onMouseEnter={e => e.currentTarget.style.color = 'var(--text-primary)'}
                                    onMouseLeave={e => e.currentTarget.style.color = 'var(--text-secondary)'}
                                >
                                    <div style={{ fontWeight: 600, color: 'var(--text-primary)', marginBottom: 2 }}>
                                        {c.title}
                                    </div>
                                    <div style={{ fontSize: 11, color: 'var(--primary-400)' }}>
                                        {c.is_free || Number(c.price) === 0 ? 'Bepul' : Number(c.price).toLocaleString('fr-FR') + " so'm"}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </aside>
            </div>
        </div>
    );
};

export default ProfilePage;
