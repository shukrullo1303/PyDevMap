import React, { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { getLesson, markLessonCompleted } from "../services/lessons";
import { getQuizByLesson, getUserQuizResult } from "../services/quiz";
import api from "../services/api";
import "../styles/pages/LessonDetailPage.css";
import AiChat from "../components/AiChat";

export default function LessonDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [lesson, setLesson]         = useState(null);
  const [quiz, setQuiz]             = useState(null);
  const [result, setResult]         = useState(null);
  const [taskSolved, setTaskSolved] = useState(false);
  const [loading, setLoading]       = useState(true);
  const [completing, setCompleting] = useState(false);
  const [showComplete, setShowComplete] = useState(false); // yakunlash modal

  useEffect(() => { loadLesson(); }, [id]);

  const loadLesson = async () => {
    setLoading(true);
    try {
      const res = await getLesson(id);
      const lessonData = res.data;
      setLesson(lessonData);

      // Majburiy masala yechilganmi?
      if (lessonData.required_task_id) {
        try {
          const solvedRes = await api.get(`/compiler/tasks/${lessonData.required_task_id}/solved/`);
          setTaskSolved(solvedRes.data.solved || false);
        } catch { /* login qilinmagan bo'lishi mumkin */ }
      }

      // Quiz
      try {
        const quizRes = await getQuizByLesson(lessonData.id);
        if (quizRes.data.length > 0) {
          const quizData = quizRes.data[0];
          setQuiz(quizData);
          const resultRes = await getUserQuizResult(quizData.id);
          if (resultRes && resultRes.length > 0) {
            setResult(resultRes[0].score);
          }
        }
      } catch { /* quiz yo'q */ }

    } catch (err) {
      console.error("Lesson load error:", err);
    } finally {
      setLoading(false);
    }
  };

  const goNext = async () => {
    try {
      await markLessonCompleted(lesson.id);
      navigate(`/lessons/${lesson.next_lesson_id}`);
    } catch (err) {
      console.error("Mark complete error:", err);
    }
  };

  const completeCourse = async () => {
    setCompleting(true);
    try {
      await markLessonCompleted(lesson.id);
      setShowComplete(true);
    } catch (err) {
      console.error("Complete error:", err);
    } finally {
      setCompleting(false);
    }
  };

  // Keyingi darsga o'tish uchun shartlar
  const canGoNext = () => {
    if (lesson.required_task_id && !taskSolved) return false;
    if (quiz && !(result >= 80)) return false;
    return true;
  };

  if (loading) return (
    <div className="loading-state">
      <div className="loading-spinner" />
      <p>Dars yuklanmoqda...</p>
    </div>
  );

  if (!lesson) return <div className="empty-state"><p>Dars topilmadi.</p></div>;

  return (
    <div className="site-container lesson-detail-page">

      {/* Breadcrumb */}
      <div style={{ marginBottom: 16, fontSize: 13, color: 'var(--text-tertiary)' }}>
        <Link to="/courses" style={{ color: 'var(--text-tertiary)', textDecoration: 'none' }}>Kurslar</Link>
        {' / '}
        <span>{lesson.title}</span>
      </div>

      <h1 style={{ marginBottom: 20 }}>{lesson.title}</h1>

      {/* Video darslik */}
      {lesson.video_file ? (
        <div className="video-container" style={{ marginBottom: 24 }}>
          <video
            controls
            style={{ width: '100%', borderRadius: 12, maxHeight: 480, background: '#000' }}
            src={lesson.video_file}
          >
            Brauzeringiz video formatini qo'llab-quvvatlamaydi.
          </video>
        </div>
      ) : lesson.video_url && (() => {
        const watchMatch = lesson.video_url.match(/youtube\.com\/watch\?v=([^&]+)/);
        const shortMatch = lesson.video_url.match(/youtu\.be\/([^?]+)/);
        const videoId = watchMatch?.[1] || shortMatch?.[1];
        return videoId ? (
          <div className="video-container" style={{ marginBottom: 24 }}>
            <iframe
              src={`https://www.youtube.com/embed/${videoId}`}
              title="YouTube video player"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
        ) : null;
      })()}

      {/* Dars matni */}
      {lesson.content && (
        <div style={{
          background: 'var(--surface)',
          border: '1px solid var(--border)',
          borderRadius: 12,
          padding: '24px 28px',
          marginBottom: 28,
          fontFamily: "'Fira Code', Consolas, monospace",
          fontSize: 13.5,
          lineHeight: 1.85,
          color: 'var(--text-primary)',
          whiteSpace: 'pre-wrap',
          overflowX: 'auto',
        }}>
          {lesson.content}
        </div>
      )}

      {/* ── MAJBURIY MASALA ── */}
      {lesson.required_task_id && (
        <div style={{
          marginBottom: 28,
          borderRadius: 12,
          border: `2px solid ${taskSolved ? '#22c55e40' : '#e8b84b40'}`,
          background: taskSolved ? 'rgba(34,197,94,0.05)' : 'rgba(232,184,75,0.05)',
          overflow: 'hidden',
        }}>
          {/* Header */}
          <div style={{
            display: 'flex', alignItems: 'center', gap: 12,
            padding: '14px 20px',
            borderBottom: `1px solid ${taskSolved ? '#22c55e30' : '#e8b84b30'}`,
            background: taskSolved ? 'rgba(34,197,94,0.08)' : 'rgba(232,184,75,0.08)',
          }}>
            <span style={{ fontSize: 22 }}>{taskSolved ? '✅' : '🔒'}</span>
            <div>
              <div style={{ fontWeight: 700, fontSize: 14, color: 'var(--text-primary)' }}>
                {taskSolved ? 'Majburiy masala yechildi!' : 'Majburiy masala'}
              </div>
              <div style={{ fontSize: 12, color: 'var(--text-tertiary)', marginTop: 2 }}>
                {taskSolved
                  ? 'Keyingi darsga o\'tishingiz mumkin'
                  : 'Keyingi darsga o\'tish uchun bu masalani yeching'}
              </div>
            </div>
          </div>

          {/* Body */}
          <div style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 12 }}>
            <div>
              <div style={{ fontWeight: 600, fontSize: 14, color: 'var(--text-primary)', marginBottom: 4 }}>
                {lesson.required_task_title}
              </div>
              <div style={{ fontSize: 12, color: 'var(--text-tertiary)' }}>
                Masalani yechib, darsni davom ettiring
              </div>
            </div>
            <Link
              to={`/tasks/${lesson.required_task_id}`}
              style={{
                display: 'inline-flex', alignItems: 'center', gap: 6,
                padding: '8px 18px', borderRadius: 8,
                background: taskSolved ? '#22c55e' : 'var(--primary-600)',
                color: taskSolved ? '#fff' : '#0d0f17',
                fontWeight: 700, fontSize: 13,
                textDecoration: 'none',
              }}
            >
              {taskSolved ? '✓ Yechilgan' : '▶ Masalani yechish'}
            </Link>
          </div>
        </div>
      )}

      {/* ── QUIZ ── */}
      {quiz && (
        <div className="quiz-box" style={{ marginBottom: 28 }}>
          {!result ? (
            <button className="btn btn-primary" onClick={() => navigate(`/quiz/${quiz.id}`)}>
              Testni ishlash
            </button>
          ) : (
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 8 }}>
              <button className="btn btn-primary" onClick={() => navigate(`/quiz/${quiz.id}`)}>
                Testni qayta ishlash
              </button>
              <span style={{ fontSize: 14, color: result >= 80 ? '#22c55e' : '#ef4444', fontWeight: 600 }}>
                Natija: {result}% {result >= 80 ? '✓' : '(80% kerak)'}
              </span>
            </div>
          )}
        </div>
      )}

      {/* ── NAVIGATSIYA ── */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 10 }}>
        {lesson.prev_lesson_id ? (
          <button className="btn btn-outline-secondary" onClick={() => navigate(`/lessons/${lesson.prev_lesson_id}`)}>
            ← Avvalgi dars
          </button>
        ) : <div />}

        {lesson.next_lesson_id ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 4 }}>
            <button
              className="btn btn-success"
              disabled={!canGoNext()}
              onClick={goNext}
              title={
                lesson.required_task_id && !taskSolved
                  ? 'Majburiy masalani yeching'
                  : quiz && !(result >= 80)
                    ? '80% dan yuqori test natijasi kerak'
                    : ''
              }
            >
              Keyingi dars →
            </button>
            {!canGoNext() && (
              <span style={{ fontSize: 11, color: 'var(--text-tertiary)' }}>
                {lesson.required_task_id && !taskSolved
                  ? '🔒 Avval masalani yeching'
                  : '🔒 Test natijasi 80%+ bo\'lsin'}
              </span>
            )}
          </div>
        ) : (
          /* ── OXIRGI DARS: Kursni yakunlash ── */
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 4 }}>
            <button
              className="btn btn-primary"
              disabled={!canGoNext() || completing}
              onClick={completeCourse}
              style={{
                background: canGoNext() ? 'linear-gradient(135deg, #22c55e, #16a34a)' : undefined,
                border: 'none',
                fontWeight: 700,
                fontSize: 14,
                padding: '10px 24px',
              }}
            >
              {completing ? 'Saqlanmoqda...' : '🎓 Kursni yakunlash'}
            </button>
            {!canGoNext() && (
              <span style={{ fontSize: 11, color: 'var(--text-tertiary)' }}>
                {lesson.required_task_id && !taskSolved
                  ? '🔒 Avval masalani yeching'
                  : '🔒 Test natijasi 80%+ bo\'lsin'}
              </span>
            )}
          </div>
        )}
      </div>

      {/* AI Tutor chat */}
      <AiChat lessonId={lesson.id} />

      {/* ── KURS YAKUNLASH MODAL ── */}
      {showComplete && (
        <div style={{
          position: 'fixed', inset: 0, zIndex: 1000,
          background: 'rgba(0,0,0,0.7)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          padding: 24,
        }}>
          <div style={{
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 20,
            padding: '40px 36px',
            maxWidth: 440,
            width: '100%',
            textAlign: 'center',
            boxShadow: '0 24px 80px rgba(0,0,0,0.4)',
          }}>
            <div style={{ fontSize: 64, marginBottom: 16 }}>🎓</div>
            <h2 style={{ fontSize: 24, fontWeight: 800, color: 'var(--text-primary)', marginBottom: 8 }}>
              Tabriklaymiz!
            </h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: 15, marginBottom: 8 }}>
              Siz kursni muvaffaqiyatli yakunladingiz!
            </p>
            <div style={{
              background: 'rgba(34,197,94,0.1)',
              border: '1px solid rgba(34,197,94,0.3)',
              borderRadius: 12,
              padding: '12px 20px',
              marginBottom: 28,
              display: 'inline-block',
            }}>
              <span style={{ fontWeight: 700, color: '#22c55e', fontSize: 14 }}>
                ✓ Kurs 100% yakunlandi
              </span>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              <button
                className="btn btn-primary"
                style={{ fontWeight: 700, fontSize: 14, padding: '12px 0' }}
                onClick={() => {
                  setShowComplete(false);
                  navigate('/profile');
                }}
              >
                Profilga o'tish va sertifikat olish
              </button>
              <button
                className="btn btn-outline-secondary"
                style={{ fontSize: 13 }}
                onClick={() => {
                  setShowComplete(false);
                  navigate('/courses');
                }}
              >
                Boshqa kurslarga qaytish
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
