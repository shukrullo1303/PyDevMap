import api from '../services/api';
import React, { useEffect, useState, useRef } from 'react';
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

// ── Avatar display ─────────────────────────────────────────────
function Avatar({ url, name, size = 72 }) {
    const initials = (name || 'U')[0].toUpperCase();
    return url ? (
        <img
            src={url}
            alt="avatar"
            style={{
                width: size, height: size, borderRadius: '50%',
                objectFit: 'cover', border: '3px solid var(--border)',
            }}
        />
    ) : (
        <div style={{
            width: size, height: size, borderRadius: '50%',
            background: 'linear-gradient(135deg, #6366f1, #a855f7)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: size * 0.38, fontWeight: 800, color: '#fff',
            border: '3px solid var(--border)', flexShrink: 0,
        }}>
            {initials}
        </div>
    );
}

// ── Kichik tab button ──────────────────────────────────────────
function TabBtn({ active, onClick, children }) {
    return (
        <button
            onClick={onClick}
            style={{
                padding: '8px 18px', borderRadius: 8, fontSize: 13, fontWeight: 600,
                border: active ? 'none' : '1px solid var(--border)',
                background: active ? 'linear-gradient(135deg, #6366f1, #a855f7)' : 'transparent',
                color: active ? '#fff' : 'var(--text-secondary)',
                cursor: 'pointer', transition: 'all 0.15s',
            }}
        >
            {children}
        </button>
    );
}

// ── Input style ───────────────────────────────────────────────
const inputStyle = {
    width: '100%', padding: '10px 14px', borderRadius: 8, fontSize: 14,
    background: 'var(--bg)', border: '1px solid var(--border)',
    color: 'var(--text-primary)', outline: 'none', boxSizing: 'border-box',
};

export default function ProfilePage() {
    const navigate = useNavigate();
    const [user, setUser]               = useState(null);
    const [enrollments, setEnrollments] = useState([]);
    const [loading, setLoading]         = useState(true);
    const [progress, setProgress]       = useState([]);
    const [testResult, setTestResult]   = useState(null);
    const [tab, setTab]                 = useState('profile'); // profile | password | support
    const [toast, setToast]             = useState(null);      // { msg, ok }

    // ── Edit Profile state ──────────────────────────────────────
    const [editForm, setEditForm]       = useState({ username: '', first_name: '', last_name: '' });
    const [editSaving, setEditSaving]   = useState(false);
    const avatarInputRef                = useRef();
    const [avatarLoading, setAvatarLoading] = useState(false);

    // ── Password state ──────────────────────────────────────────
    const [pwForm, setPwForm]           = useState({ old_password: '', new_password: '', confirm: '' });
    const [pwSaving, setPwSaving]       = useState(false);

    // ── Support state ───────────────────────────────────────────
    const [messages, setMessages]       = useState([]);
    const [msgInput, setMsgInput]       = useState('');
    const [msgSending, setMsgSending]   = useState(false);
    const supportBottomRef              = useRef();

    const showToast = (msg, ok = true) => {
        setToast({ msg, ok });
        setTimeout(() => setToast(null), 3500);
    };

    useEffect(() => {
        const load = async () => {
            try {
                const profileRes = await getProfile();
                const u = profileRes.data;
                setUser(u);
                setEditForm({ username: u.username || '', first_name: u.first_name || '', last_name: u.last_name || '' });

                const enrollRes = await getMyEnrollments(u.id);
                setEnrollments(Array.isArray(enrollRes.data) ? enrollRes.data : enrollRes.data.results || []);

                const progressRes = await api.get('/course-progress/');
                setProgress(progressRes.data);

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
        load();
    }, []);

    // Load support messages when tab opens
    useEffect(() => {
        if (tab !== 'support') return;
        api.get('/support/').then(r => setMessages(r.data)).catch(() => {});
    }, [tab]);

    // Scroll to bottom of support chat
    useEffect(() => {
        supportBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // ── Handlers ───────────────────────────────────────────────

    const handleAvatarChange = async (e) => {
        const file = e.target.files?.[0];
        if (!file) return;
        setAvatarLoading(true);
        const form = new FormData();
        form.append('avatar', file);
        try {
            const res = await api.post('/auth/avatar/', form, { headers: { 'Content-Type': 'multipart/form-data' } });
            setUser(u => ({ ...u, avatar_url: res.data.avatar_url }));
            showToast('Profil rasm yangilandi!');
        } catch (e) {
            showToast(e.response?.data?.error || 'Xatolik yuz berdi', false);
        } finally {
            setAvatarLoading(false);
        }
    };

    const handleProfileSave = async () => {
        setEditSaving(true);
        try {
            const res = await api.patch('/auth/profile/', editForm);
            setUser(u => ({ ...u, ...res.data }));
            showToast('Profil yangilandi!');
        } catch (e) {
            showToast(e.response?.data?.error || 'Xatolik yuz berdi', false);
        } finally {
            setEditSaving(false);
        }
    };

    const handlePasswordSave = async () => {
        if (pwForm.new_password !== pwForm.confirm) {
            showToast('Yangi parollar mos kelmayapti', false);
            return;
        }
        setPwSaving(true);
        try {
            await api.post('/auth/password/', {
                old_password: pwForm.old_password,
                new_password: pwForm.new_password,
            });
            setPwForm({ old_password: '', new_password: '', confirm: '' });
            showToast('Parol muvaffaqiyatli o\'zgartirildi!');
        } catch (e) {
            showToast(e.response?.data?.error || 'Xatolik yuz berdi', false);
        } finally {
            setPwSaving(false);
        }
    };

    const handleSendMessage = async () => {
        const text = msgInput.trim();
        if (!text || msgSending) return;
        setMsgSending(true);
        try {
            const res = await api.post('/support/', { message: text });
            setMessages(m => [res.data, ...m]);
            setMsgInput('');
        } catch (e) {
            showToast('Xabar yuborishda xatolik', false);
        } finally {
            setMsgSending(false);
        }
    };

    if (loading) {
        return <div className="site-container"><div className="loading-state">Profil yuklanmoqda...</div></div>;
    }

    const lvl = testResult ? (LEVEL_INFO[testResult.level] || LEVEL_INFO.beginner) : null;
    const nameLocked = user?.name_locked;

    return (
        <div className="site-container">
            {/* Toast */}
            {toast && (
                <div style={{
                    position: 'fixed', top: 80, left: '50%', transform: 'translateX(-50%)',
                    background: toast.ok ? '#22c55e' : '#ef4444',
                    color: '#fff', padding: '11px 22px', borderRadius: 10,
                    fontWeight: 700, fontSize: 14, zIndex: 9999,
                    boxShadow: '0 4px 20px rgba(0,0,0,0.3)',
                }}>
                    {toast.ok ? '✓' : '✗'} {toast.msg}
                </div>
            )}

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
                                        <div style={{ fontSize: 22, fontWeight: 800, color: lvl.color }}>{lvl.label}</div>
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
                                            <div style={{ fontSize: 18, fontWeight: 900, color: '#e8b84b', letterSpacing: 2 }}>{testResult.coupon.code}</div>
                                            <div style={{ fontSize: 11, color: '#e8b84b' }}>{testResult.coupon.percentage}% • {testResult.coupon.valid_until} gacha</div>
                                        </div>
                                    )}
                                    <button className="btn btn-outline-secondary" style={{ fontSize: 13 }} onClick={() => navigate('/placement-test')}>
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
                                    <h3 style={{ margin: '0 0 6px', fontSize: 18, fontWeight: 800 }}>Bilimni baholash</h3>
                                    <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: 14 }}>25 ta adaptiv savol • Darajangizni aniqlaymiz</p>
                                    <p style={{ margin: '4px 0 0', color: '#e8b84b', fontSize: 13, fontWeight: 600 }}>80%+ natija — 50% chegirma kuponi!</p>
                                </div>
                                <button
                                    className="btn btn-primary"
                                    style={{ padding: '12px 28px', fontWeight: 700, fontSize: 15, background: 'linear-gradient(135deg, #6366f1, #a855f7)', border: 'none' }}
                                    onClick={() => navigate('/placement-test')}
                                >
                                    Testni boshlash
                                </button>
                            </div>
                        </section>
                    )}

                    {/* ── Tabs ── */}
                    <section className="profile-section">
                        <div style={{ display: 'flex', gap: 8, marginBottom: 24, flexWrap: 'wrap' }}>
                            <TabBtn active={tab === 'profile'}  onClick={() => setTab('profile')}>👤 Profilim</TabBtn>
                            <TabBtn active={tab === 'password'} onClick={() => setTab('password')}>🔒 Parol</TabBtn>
                            <TabBtn active={tab === 'support'}  onClick={() => setTab('support')}>💬 Yordam</TabBtn>
                            {user?.is_staff && (
                                <TabBtn active={false} onClick={() => navigate('/admin-support')}>🛠 Admin Panel</TabBtn>
                            )}
                        </div>

                        {/* ── TAB: Profil ── */}
                        {tab === 'profile' && (
                            <div>
                                {/* Avatar */}
                                <div style={{ display: 'flex', alignItems: 'center', gap: 18, marginBottom: 24 }}>
                                    <div style={{ position: 'relative' }}>
                                        <Avatar url={user?.avatar_url} name={user?.username} size={80} />
                                        <button
                                            onClick={() => avatarInputRef.current?.click()}
                                            disabled={avatarLoading}
                                            style={{
                                                position: 'absolute', bottom: 0, right: 0,
                                                width: 26, height: 26, borderRadius: '50%',
                                                background: '#6366f1', border: '2px solid var(--bg)',
                                                color: '#fff', fontSize: 13, cursor: 'pointer',
                                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                            }}
                                            title="Rasmni o'zgartirish"
                                        >
                                            {avatarLoading ? '⟳' : '✎'}
                                        </button>
                                        <input
                                            ref={avatarInputRef}
                                            type="file"
                                            accept="image/*"
                                            style={{ display: 'none' }}
                                            onChange={handleAvatarChange}
                                        />
                                    </div>
                                    <div>
                                        <div style={{ fontWeight: 700, fontSize: 17 }}>{user?.username}</div>
                                        <div style={{ color: 'var(--text-secondary)', fontSize: 13 }}>{user?.email}</div>
                                        <div style={{ fontSize: 12, color: 'var(--text-tertiary)', marginTop: 2 }}>
                                            {new Date(user?.date_joined || Date.now()).toLocaleDateString()} dan beri a'zo
                                        </div>
                                    </div>
                                </div>

                                {/* Edit form */}
                                <div style={{ display: 'flex', flexDirection: 'column', gap: 14, maxWidth: 440 }}>
                                    <div>
                                        <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-tertiary)', marginBottom: 5, display: 'block' }}>USERNAME</label>
                                        <input
                                            style={inputStyle}
                                            value={editForm.username}
                                            onChange={e => setEditForm(f => ({ ...f, username: e.target.value }))}
                                            placeholder="username"
                                        />
                                    </div>

                                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                                        <div>
                                            <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-tertiary)', marginBottom: 5, display: 'block' }}>ISM</label>
                                            <div style={{ position: 'relative' }}>
                                                <input
                                                    style={{ ...inputStyle, ...(nameLocked ? { opacity: 0.5, cursor: 'not-allowed' } : {}) }}
                                                    value={editForm.first_name}
                                                    onChange={e => setEditForm(f => ({ ...f, first_name: e.target.value }))}
                                                    placeholder="Ism"
                                                    disabled={nameLocked}
                                                />
                                            </div>
                                        </div>
                                        <div>
                                            <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-tertiary)', marginBottom: 5, display: 'block' }}>FAMILIYA</label>
                                            <input
                                                style={{ ...inputStyle, ...(nameLocked ? { opacity: 0.5, cursor: 'not-allowed' } : {}) }}
                                                value={editForm.last_name}
                                                onChange={e => setEditForm(f => ({ ...f, last_name: e.target.value }))}
                                                placeholder="Familiya"
                                                disabled={nameLocked}
                                            />
                                        </div>
                                    </div>

                                    {nameLocked && (
                                        <div style={{
                                            background: 'rgba(232,184,75,0.1)', border: '1px solid rgba(232,184,75,0.3)',
                                            borderRadius: 8, padding: '10px 14px', fontSize: 13, color: '#e8b84b',
                                        }}>
                                            🔒 Sertifikat olgandan keyin ism-familiya o'zgartirib bo'lmaydi
                                        </div>
                                    )}

                                    <button
                                        className="btn btn-primary"
                                        style={{ alignSelf: 'flex-start', padding: '10px 24px', fontWeight: 700 }}
                                        onClick={handleProfileSave}
                                        disabled={editSaving}
                                    >
                                        {editSaving ? 'Saqlanmoqda...' : 'Saqlash'}
                                    </button>
                                </div>
                            </div>
                        )}

                        {/* ── TAB: Parol ── */}
                        {tab === 'password' && (
                            <div style={{ maxWidth: 380 }}>
                                <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                                    <div>
                                        <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-tertiary)', marginBottom: 5, display: 'block' }}>JORIY PAROL</label>
                                        <input
                                            type="password"
                                            style={inputStyle}
                                            value={pwForm.old_password}
                                            onChange={e => setPwForm(f => ({ ...f, old_password: e.target.value }))}
                                            placeholder="Hozirgi parolni kiriting"
                                        />
                                    </div>
                                    <div>
                                        <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-tertiary)', marginBottom: 5, display: 'block' }}>YANGI PAROL</label>
                                        <input
                                            type="password"
                                            style={inputStyle}
                                            value={pwForm.new_password}
                                            onChange={e => setPwForm(f => ({ ...f, new_password: e.target.value }))}
                                            placeholder="Kamida 8 ta belgi"
                                        />
                                    </div>
                                    <div>
                                        <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-tertiary)', marginBottom: 5, display: 'block' }}>YANGI PAROLNI TASDIQLANG</label>
                                        <input
                                            type="password"
                                            style={{
                                                ...inputStyle,
                                                borderColor: pwForm.confirm && pwForm.new_password !== pwForm.confirm ? '#ef4444' : undefined,
                                            }}
                                            value={pwForm.confirm}
                                            onChange={e => setPwForm(f => ({ ...f, confirm: e.target.value }))}
                                            placeholder="Takrorlang"
                                        />
                                        {pwForm.confirm && pwForm.new_password !== pwForm.confirm && (
                                            <div style={{ fontSize: 12, color: '#ef4444', marginTop: 4 }}>Parollar mos kelmayapti</div>
                                        )}
                                    </div>
                                    <button
                                        className="btn btn-primary"
                                        style={{ alignSelf: 'flex-start', padding: '10px 24px', fontWeight: 700 }}
                                        onClick={handlePasswordSave}
                                        disabled={pwSaving || !pwForm.old_password || !pwForm.new_password || pwForm.new_password !== pwForm.confirm}
                                    >
                                        {pwSaving ? 'Saqlanmoqda...' : 'Parolni o\'zgartirish'}
                                    </button>
                                </div>
                            </div>
                        )}

                        {/* ── TAB: Support ── */}
                        {tab === 'support' && (
                            <div>
                                <p style={{ color: 'var(--text-secondary)', fontSize: 14, marginBottom: 16 }}>
                                    Muammo yoki taklifingizni yozing — tez orada javob beramiz.
                                </p>

                                {/* Message history */}
                                <div style={{
                                    background: 'var(--bg)', border: '1px solid var(--border)',
                                    borderRadius: 12, padding: '16px', minHeight: 200, maxHeight: 380,
                                    overflowY: 'auto', marginBottom: 14,
                                    display: 'flex', flexDirection: 'column', gap: 16,
                                }}>
                                    {messages.length === 0 ? (
                                        <div style={{ textAlign: 'center', color: 'var(--text-tertiary)', paddingTop: 40 }}>
                                            <div style={{ fontSize: 36, marginBottom: 8 }}>💬</div>
                                            <p style={{ fontSize: 14 }}>Hozircha xabarlar yo'q</p>
                                        </div>
                                    ) : (
                                        [...messages].reverse().map(msg => (
                                            <div key={msg.id}>
                                                {/* User message */}
                                                <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: msg.reply ? 8 : 0 }}>
                                                    <div style={{
                                                        maxWidth: '78%', padding: '10px 14px',
                                                        borderRadius: '14px 14px 4px 14px',
                                                        background: 'linear-gradient(135deg, #6366f1, #a855f7)',
                                                        color: '#fff', fontSize: 14, lineHeight: 1.6,
                                                    }}>
                                                        <div>{msg.message}</div>
                                                        <div style={{ fontSize: 11, opacity: 0.75, marginTop: 4, textAlign: 'right' }}>
                                                            {new Date(msg.created_at).toLocaleString()}
                                                        </div>
                                                    </div>
                                                </div>
                                                {/* Admin reply */}
                                                {msg.reply && (
                                                    <div style={{ display: 'flex', gap: 10, alignItems: 'flex-start' }}>
                                                        <div style={{
                                                            width: 30, height: 30, borderRadius: 8, flexShrink: 0,
                                                            background: 'linear-gradient(135deg, #e8b84b, #c99a20)',
                                                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                                                            fontSize: 14,
                                                        }}>🛠</div>
                                                        <div style={{
                                                            maxWidth: '78%', padding: '10px 14px',
                                                            borderRadius: '4px 14px 14px 14px',
                                                            background: 'rgba(232,184,75,0.1)',
                                                            border: '1px solid rgba(232,184,75,0.25)',
                                                            color: 'var(--text-primary)', fontSize: 14, lineHeight: 1.6,
                                                        }}>
                                                            <div>{msg.reply}</div>
                                                            <div style={{ fontSize: 11, color: 'var(--text-tertiary)', marginTop: 4 }}>
                                                                {msg.replied_at ? new Date(msg.replied_at).toLocaleString() : ''}
                                                            </div>
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                        ))
                                    )}
                                    <div ref={supportBottomRef} />
                                </div>

                                {/* Send input */}
                                <div style={{ display: 'flex', gap: 10 }}>
                                    <textarea
                                        value={msgInput}
                                        onChange={e => setMsgInput(e.target.value)}
                                        onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSendMessage(); } }}
                                        placeholder="Muammo yoki taklifingizni yozing... (Enter — yuborish)"
                                        rows={2}
                                        style={{
                                            flex: 1, padding: '10px 14px', borderRadius: 10, fontSize: 14,
                                            background: 'var(--bg)', border: '1px solid var(--border)',
                                            color: 'var(--text-primary)', outline: 'none', resize: 'none',
                                        }}
                                    />
                                    <button
                                        onClick={handleSendMessage}
                                        disabled={msgSending || !msgInput.trim()}
                                        className="btn btn-primary"
                                        style={{ padding: '10px 18px', borderRadius: 10, fontWeight: 700, alignSelf: 'flex-end' }}
                                    >
                                        {msgSending ? '...' : 'Yuborish'}
                                    </button>
                                </div>
                            </div>
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
                                    const cp = progress.find(p => p.course_id === e.course) || { progress: 0 };
                                    const displayTitle = e.course_title || cp.course_title || ('Kurs #' + e.course);
                                    return (
                                        <div key={e.id} className="enrollment-item">
                                            <div className="enrollment-header">
                                                <h4>{displayTitle}</h4>
                                                {cp.progress === 100
                                                    ? <DownloadCertificateButton courseId={e.course} />
                                                    : <span className="enrollment-status">Jarayonda</span>
                                                }
                                            </div>
                                            <p className="enrollment-date">
                                                Ro'yxatdan o'tilgan: {new Date(e.created_at).toLocaleDateString()}
                                            </p>
                                            <div className="enrollment-progress">
                                                <div className="progress-bar">
                                                    <div className="progress-fill" style={{ width: cp.progress + '%' }}></div>
                                                </div>
                                                <small>{cp.progress}% bajarildi</small>
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
                        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
                            <Avatar url={user?.avatar_url} name={user?.username} size={48} />
                            <div>
                                <div style={{ fontWeight: 700 }}>{user?.username}</div>
                                <div style={{ fontSize: 12, color: 'var(--text-tertiary)' }}>{user?.email}</div>
                            </div>
                        </div>
                        <h4>Statistika</h4>
                        <div className="stat-item">
                            <span className="stat-value">{enrollments.length}</span>
                            <span className="stat-label">Ro'yxatdan o'tilgan kurslar</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-value">{progress.filter(p => p.progress === 100).length}</span>
                            <span className="stat-label">Tugatilgan kurslar</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-value">{testResult ? testResult.percentage + '%' : '—'}</span>
                            <span className="stat-label">Bilim darajasi</span>
                        </div>
                    </div>

                    {testResult?.recommended_courses?.length > 0 && (
                        <div className="sidebar-card" style={{ marginTop: 16 }}>
                            <h4 style={{ marginBottom: 14 }}>Tavsiya qilingan kurslar</h4>
                            {testResult.recommended_courses.slice(0, 4).map(c => (
                                <div
                                    key={c.id}
                                    onClick={() => navigate('/courses/' + c.id)}
                                    style={{
                                        padding: '10px 0', borderBottom: '1px solid var(--border)',
                                        cursor: 'pointer', fontSize: 13, color: 'var(--text-secondary)',
                                        transition: 'color 0.15s',
                                    }}
                                    onMouseEnter={e => e.currentTarget.style.color = 'var(--text-primary)'}
                                    onMouseLeave={e => e.currentTarget.style.color = 'var(--text-secondary)'}
                                >
                                    <div style={{ fontWeight: 600, color: 'var(--text-primary)', marginBottom: 2 }}>{c.title}</div>
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
}
