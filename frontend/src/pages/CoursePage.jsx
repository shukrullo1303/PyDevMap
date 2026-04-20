import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getCourse } from '../services/courses';
import { getLessonsByCourse } from '../services/lessons';
import LessonListCard from '../components/LessonListCard';
import { enrollCourse, checkEnrolled } from '../services/enrollments';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

const COURSE_ICONS = ['🐍', '⚙️', '📊', '🏗️', '🌐', '🤖', '🔧', '📦', '🚀', '🔐'];
const ICON_BG_COLORS = [
    'linear-gradient(135deg, #22c55e, #16a34a)',
    'linear-gradient(135deg, #3b82f6, #0891b2)',
    'linear-gradient(135deg, #f97316, #dc2626)',
    'linear-gradient(135deg, #a855f7, #ec4899)',
    'linear-gradient(135deg, #14b8a6, #22c55e)',
];

const CoursePage = () => {
    const { id } = useParams();
    const { user } = useAuth();
    const [course, setCourse] = useState(null);
    const [lessons, setLessons] = useState([]);
    const [enrolled, setEnrolled] = useState(false);
    const [loading, setLoading] = useState(true);
    const [enrolling, setEnrolling] = useState(false);
    const [payModal, setPayModal] = useState(null); // { checkout_url, amount, provider }

    const iconIdx = Number(id) % COURSE_ICONS.length || 0;
    const icon = COURSE_ICONS[iconIdx];
    const bgColor = ICON_BG_COLORS[iconIdx % ICON_BG_COLORS.length];

    useEffect(() => {
        const load = async () => {
            try {
                const res = await getCourse(id);
                setCourse(res.data);
            } catch (err) {
                console.error(err);
            }

            try {
                const res2 = await getLessonsByCourse(id);
                setLessons(Array.isArray(res2.data) ? res2.data : res2.data.results || []);
            } catch {
                setLessons([]);
            }

            if (user) {
                try {
                    const r = await checkEnrolled(id);
                    setEnrolled(r.data.enrolled);
                } catch {
                    setEnrolled(false);
                }
            }

            setLoading(false);
        };
        load();
    }, [id, user]);

    const handleEnroll = async () => {
        setEnrolling(true);
        try {
            const isFreeNow = course.is_free || Number(course.price) === 0;
            if (isFreeNow) {
                const res = await enrollCourse(course.id);
                if (res.data.detail === 'Successfully enrolled') setEnrolled(true);
            } else {
                // To'lovli kurs — Payme order yarat
                const res = await api.post('/payment/payme/order/', { course_id: course.id });
                if (res.data.enrolled) {
                    setEnrolled(true);
                } else {
                    setPayModal({
                        checkout_url: res.data.checkout_url,
                        amount: res.data.amount,
                        provider: 'payme',
                    });
                }
            }
        } catch (err) {
            console.error('Enroll error:', err.response?.data);
        } finally {
            setEnrolling(false);
        }
    };

    if (loading) return (
        <div className="site-container loading-state">
            <div className="loading-spinner"></div>
            <p>Yuklanmoqda...</p>
        </div>
    );

    if (!course) return (
        <div className="site-container empty-state">
            <p>Kurs topilmadi.</p>
        </div>
    );

    const isFree = course.is_free || Number(course.price) === 0;

    return (
      <>
      {/* ── To'lov modal ── */}
      {payModal && (
        <div style={{
          position: 'fixed', inset: 0, zIndex: 2000,
          background: 'rgba(0,0,0,0.75)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          padding: 24,
        }}>
          <div style={{
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 20,
            padding: '36px 32px',
            maxWidth: 420, width: '100%',
            textAlign: 'center',
          }}>
            <div style={{ fontSize: 48, marginBottom: 12 }}>💳</div>
            <h3 style={{ fontSize: 22, fontWeight: 800, marginBottom: 8 }}>To'lov</h3>
            <p style={{ color: 'var(--text-secondary)', marginBottom: 4 }}>{course.title}</p>
            <div style={{
              fontSize: 28, fontWeight: 800,
              color: 'var(--primary-400)',
              marginBottom: 24,
            }}>
              {Number(payModal.amount).toLocaleString('fr-FR')} so'm
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {/* Payme */}
              <a
                href={payModal.checkout_url}
                target="_blank" rel="noreferrer"
                style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10,
                  padding: '13px 0', borderRadius: 10, fontWeight: 700, fontSize: 15,
                  background: '#00CAAB', color: '#fff', textDecoration: 'none',
                }}
                onClick={() => setPayModal(null)}
              >
                <span style={{ fontSize: 20 }}>💚</span> Payme orqali to'lash
              </a>

              {/* Click */}
              <button
                onClick={async () => {
                  try {
                    const r = await api.post('/payment/click/order/', { course_id: course.id });
                    if (r.data.checkout_url) {
                      window.open(r.data.checkout_url, '_blank');
                      setPayModal(null);
                    }
                  } catch (e) { console.error(e); }
                }}
                style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10,
                  padding: '13px 0', borderRadius: 10, fontWeight: 700, fontSize: 15,
                  background: '#FE5722', color: '#fff', border: 'none', cursor: 'pointer',
                }}
              >
                <span style={{ fontSize: 20 }}>🔴</span> Click orqali to'lash
              </button>

              <button
                onClick={() => setPayModal(null)}
                className="btn btn-outline-secondary"
                style={{ marginTop: 4 }}
              >
                Bekor qilish
              </button>
            </div>
          </div>
        </div>
      )}
      <div className="site-container">
        <div className="site-container">
            {/* Breadcrumb */}
            <div className="breadcrumb">
                <Link to="/">Bosh sahifa</Link>
                <span>/</span>
                <Link to="/courses">Kurslar</Link>
                <span>/</span>
                <span style={{ color: 'var(--text-primary)' }}>{course.title}</span>
            </div>

            {/* Course Hero */}
            <div style={{
                background: 'var(--surface)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius-lg)',
                padding: '32px',
                marginBottom: 32,
            }}>
                <div style={{ display: 'flex', gap: 20, alignItems: 'flex-start', flexWrap: 'wrap' }}>
                    {/* Icon */}
                    <div style={{
                        width: 64,
                        height: 64,
                        borderRadius: 'var(--radius-md)',
                        background: bgColor,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: 32,
                        flexShrink: 0,
                    }}>
                        {icon}
                    </div>

                    <div style={{ flex: 1, minWidth: 200 }}>
                        <h1 style={{ fontSize: 'var(--font-size-3xl)', marginBottom: 8 }}>
                            {course.title}
                        </h1>
                        <p style={{ color: 'var(--text-secondary)', marginBottom: 16 }}>
                            {course.subtitle || course.description?.slice(0, 150)}
                        </p>

                        <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
                            {isFree ? (
                                <span className="badge badge-free" style={{ fontSize: 14, padding: '4px 14px' }}>Bepul</span>
                            ) : (
                                <span style={{ fontWeight: 700, fontSize: 'var(--font-size-xl)', color: 'var(--text-primary)' }}>
                                    {Number(course.price).toLocaleString('fr-FR').replace(',', ' ')} so'm
                                </span>
                            )}

                            {user ? (
                                <button
                                    onClick={handleEnroll}
                                    className={`btn ${enrolled ? 'btn-secondary' : 'btn-primary'}`}
                                    disabled={enrolled || enrolling}
                                    style={{ padding: '10px 24px' }}
                                >
                                    {enrolled ? (
                                        <>
                                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                                                <polyline points="20 6 9 17 4 12"/>
                                            </svg>
                                            Ro'yxatda
                                        </>
                                    ) : enrolling ? 'Yuklanmoqda...' : (
                                        <>
                                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                                <line x1="12" y1="5" x2="12" y2="19"/>
                                                <line x1="5" y1="12" x2="19" y2="12"/>
                                            </svg>
                                            Ro'yxatdan o'tish
                                        </>
                                    )}
                                </button>
                            ) : (
                                <Link to="/login" className="btn btn-primary" style={{ padding: '10px 24px' }}>
                                    Kirish kerak
                                </Link>
                            )}
                        </div>
                    </div>
                </div>
            </div>

            {/* Layout */}
            <div className="sidebar course-layout">
                <div className="course-main">
                    {/* About */}
                    <section style={{ marginBottom: 40 }}>
                        <h2 style={{ fontSize: 'var(--font-size-2xl)', marginBottom: 16 }}>Kurs haqida</h2>
                        <p style={{ color: 'var(--text-secondary)', lineHeight: 1.75, whiteSpace: 'pre-wrap' }}>
                            {course.description}
                        </p>
                    </section>

                    {/* Lessons */}
                    <section>
                        <h2 style={{ fontSize: 'var(--font-size-2xl)', marginBottom: 16 }}>
                            Darslar
                            <span style={{
                                marginLeft: 10,
                                fontSize: 'var(--font-size-base)',
                                fontWeight: 400,
                                color: 'var(--text-tertiary)',
                            }}>
                                ({lessons.length} ta)
                            </span>
                        </h2>

                        {lessons.length === 0 ? (
                            <div className="empty-state" style={{ padding: '24px 0' }}>
                                <p>Darslar hali qo'shilmagan</p>
                            </div>
                        ) : (
                            <div className="lesson-grid">
                                {lessons.map((lesson, idx) => {
                                    const prevLesson = lessons.find(l => l.id === lesson.prev_lesson_id);
                                    const prevProgress = prevLesson?.progress_records?.find(pr => pr.user === user?.id);
                                    const isOpen = enrolled && (
                                        lesson.prev_lesson_id === null ||
                                        prevProgress?.completed
                                    );
                                    return (
                                        <LessonListCard
                                            key={lesson.id}
                                            lesson={lesson}
                                            index={idx + 1}
                                            isOpen={isOpen}
                                        />
                                    );
                                })}
                            </div>
                        )}
                    </section>
                </div>

                {/* Sidebar */}
                <aside>
                    <div style={{
                        background: 'var(--surface)',
                        border: '1px solid var(--border)',
                        borderRadius: 'var(--radius-md)',
                        padding: 'var(--space-xl)',
                        position: 'sticky',
                        top: 80,
                    }}>
                        <h4 style={{ marginBottom: 20, paddingBottom: 16, borderBottom: '1px solid var(--border)' }}>
                            Kurs ma'lumotlari
                        </h4>

                        {[
                            { label: "O'qituvchi", value: course.instructor_name || 'TBA' },
                            { label: 'Daraja', value: course.level || 'Noaniq' },
                            { label: 'Darslar', value: `${lessons.length} ta` },
                            { label: 'Kategoriya', value: course.category_name || '—' },
                        ].map(({ label, value }) => (
                            <div key={label} style={{ marginBottom: 16 }}>
                                <div style={{
                                    fontSize: 'var(--font-size-xs)',
                                    fontWeight: 600,
                                    color: 'var(--text-tertiary)',
                                    textTransform: 'uppercase',
                                    letterSpacing: '0.5px',
                                    marginBottom: 4,
                                }}>
                                    {label}
                                </div>
                                <div style={{ fontSize: 'var(--font-size-base)', color: 'var(--text-primary)', fontWeight: 500 }}>
                                    {value}
                                </div>
                            </div>
                        ))}

                        {/* Status */}
                        <div style={{ marginTop: 8 }}>
                            <div style={{
                                fontSize: 'var(--font-size-xs)',
                                fontWeight: 600,
                                color: 'var(--text-tertiary)',
                                textTransform: 'uppercase',
                                letterSpacing: '0.5px',
                                marginBottom: 4,
                            }}>
                                Status
                            </div>
                            <span className={`badge ${enrolled ? 'badge-success' : 'badge-outline'}`}
                                style={{ fontSize: 13, padding: '4px 12px' }}>
                                {enrolled ? '✓ Ro\'yxatda' : 'Hali yozilmagan'}
                            </span>
                        </div>
                    </div>
                </aside>
            </div>
        </div>
      </div>
    </>
    );
};

export default CoursePage;
