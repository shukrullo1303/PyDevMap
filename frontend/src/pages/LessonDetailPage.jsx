import React, { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { getLesson, markLessonCompleted } from "../services/lessons";
import { getQuizByLesson, getUserQuizResult } from "../services/quiz";
import api from "../services/api";
import "../styles/pages/LessonDetailPage.css";

export default function LessonDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [lesson, setLesson]     = useState(null);
  const [quiz, setQuiz]         = useState(null);
  const [result, setResult]     = useState(null);
  const [taskSolved, setTaskSolved] = useState(false);
  const [loading, setLoading]   = useState(true);

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

      {/* YouTube video */}
      {lesson.video_url && (() => {
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

        {lesson.next_lesson_id && (
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
        )}
      </div>
    </div>
  );
}
