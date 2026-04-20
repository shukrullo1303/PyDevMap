import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const TOPIC_LABELS = {
  basics: 'Asoslar', strings: 'Satrlar', lists: "Ro'yxatlar",
  dicts: "Lug'atlar", functions: 'Funksiyalar', oop: 'OOP',
  exceptions: 'Xatolar', files: 'Fayllar', modules: 'Modullar',
  algorithms: 'Algoritmlar',
};

const DIFFICULTY_STARS = (d) => '★'.repeat(d) + '☆'.repeat(5 - d);

const LEVEL_INFO = {
  beginner:     { label: "Boshlang'ich",  color: '#22c55e', emoji: '🌱' },
  intermediate: { label: "O'rta daraja",  color: '#e8b84b', emoji: '📈' },
  advanced:     { label: 'Ilg\'or',       color: '#3b82f6', emoji: '🚀' },
  expert:       { label: 'Expert',        color: '#a855f7', emoji: '🏆' },
};

export default function PlacementTestPage() {
  const navigate = useNavigate();
  const [phase, setPhase]       = useState('intro');   // intro | test | result
  const [session, setSession]   = useState(null);
  const [question, setQuestion] = useState(null);
  const [selected, setSelected] = useState('');
  const [codeAnswer, setCodeAnswer] = useState('');
  const [feedback, setFeedback]  = useState(null);   // {is_correct, explanation}
  const [progress, setProgress]  = useState(0);
  const [total, setTotal]        = useState(25);
  const [result, setResult]      = useState(null);
  const [loading, setLoading]    = useState(false);
  const [startTime, setStartTime] = useState(null);

  const startTest = async () => {
    setLoading(true);
    try {
      const res = await api.post('/placement/start/');
      setSession(res.data.session_id);
      setQuestion(res.data.question);
      setProgress(res.data.question_num - 1);
      setTotal(res.data.total);
      setPhase('test');
      setStartTime(Date.now());
    } catch (e) {
      alert('Test boshlashda xatolik.');
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!selected && !codeAnswer) return;
    const answer = question.type === 'code' ? codeAnswer : selected;
    const timeSec = Math.round((Date.now() - startTime) / 1000);
    setLoading(true);

    try {
      const res = await api.post('/placement/answer/', {
        session_id: session,
        question_id: question.id,
        answer,
        time_spent: timeSec,
      });

      if (res.data.finished) {
        setResult(res.data.result);
        setPhase('result');
        return;
      }

      setFeedback({ is_correct: res.data.is_correct, explanation: res.data.explanation });
      setProgress(res.data.progress);

      setTimeout(() => {
        setFeedback(null);
        setSelected('');
        setCodeAnswer('');
        setQuestion(res.data.next_question);
        setStartTime(Date.now());
      }, 1800);

    } catch (e) {
      alert('Xatolik yuz berdi.');
    } finally {
      setLoading(false);
    }
  };

  // ── INTRO ──────────────────────────────────────────────
  if (phase === 'intro') return (
    <div className="site-container" style={{ maxWidth: 600, margin: '60px auto', textAlign: 'center' }}>
      <div style={{ fontSize: 72, marginBottom: 16 }}>🧠</div>
      <h1 style={{ fontSize: 32, fontWeight: 800, marginBottom: 12 }}>Daraja aniqlash testi</h1>
      <p style={{ color: 'var(--text-secondary)', fontSize: 16, marginBottom: 8 }}>
        25 ta savol — adaptiv algoritm sizning darajangizni aniq belgilaydi
      </p>
      <div style={{
        background: 'rgba(232,184,75,0.1)', border: '1px solid rgba(232,184,75,0.3)',
        borderRadius: 12, padding: '16px 24px', marginBottom: 32, display: 'inline-block',
      }}>
        <p style={{ margin: 0, color: '#e8b84b', fontWeight: 600 }}>
          80%+ natija → 50% chegirma kuponi!
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 12, alignItems: 'center', marginBottom: 32 }}>
        {[
          ['⚡', 'Adaptiv — noto\'g\'ri javob bersangiz, osonroq savol keladi'],
          ['📊', '10 ta mavzu bo\'yicha: asoslardan algoritmgacha'],
          ['🎯', 'Natijaga qarab kurslar tavsiya qilinadi'],
          ['🏷️', 'Iqtidorli o\'quvchilarga chegirma kuponi'],
        ].map(([icon, text]) => (
          <div key={text} style={{ display: 'flex', gap: 12, alignItems: 'center', color: 'var(--text-secondary)' }}>
            <span style={{ fontSize: 20 }}>{icon}</span>
            <span style={{ fontSize: 14 }}>{text}</span>
          </div>
        ))}
      </div>

      <button
        className="btn btn-primary"
        style={{ padding: '14px 48px', fontSize: 16, fontWeight: 700 }}
        onClick={startTest}
        disabled={loading}
      >
        {loading ? 'Yuklanmoqda...' : 'Testni boshlash'}
      </button>
    </div>
  );

  // ── TEST ───────────────────────────────────────────────
  if (phase === 'test' && question) {
    const pct = Math.round((progress / total) * 100);
    return (
      <div className="site-container" style={{ maxWidth: 700, margin: '0 auto' }}>
        {/* Progress */}
        <div style={{ marginBottom: 24 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
            <span style={{ color: 'var(--text-secondary)', fontSize: 14 }}>
              Savol {progress + 1} / {total}
            </span>
            <span style={{ color: 'var(--text-secondary)', fontSize: 14 }}>
              {TOPIC_LABELS[question.topic] || question.topic} • {DIFFICULTY_STARS(question.difficulty)}
            </span>
          </div>
          <div style={{ background: 'var(--border)', borderRadius: 8, height: 8 }}>
            <div style={{
              background: 'linear-gradient(90deg, var(--primary-400), #a855f7)',
              width: pct + '%', height: '100%', borderRadius: 8,
              transition: 'width 0.4s ease',
            }} />
          </div>
        </div>

        {/* Question card */}
        <div style={{
          background: 'var(--surface)', border: '1px solid var(--border)',
          borderRadius: 16, padding: '28px 32px', marginBottom: 20,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 20 }}>
            <span style={{
              background: 'rgba(139,92,246,0.15)', color: '#a855f7',
              padding: '4px 12px', borderRadius: 20, fontSize: 12, fontWeight: 600,
            }}>
              {question.points} ball
            </span>
            <span style={{ fontSize: 12, color: 'var(--text-tertiary)' }}>
              {question.type === 'code' ? 'Kod yozish' : "Ko'p tanlovli"}
            </span>
          </div>

          <pre style={{
            fontFamily: "'Fira Code', monospace",
            fontSize: 15, lineHeight: 1.7,
            color: 'var(--text-primary)',
            whiteSpace: 'pre-wrap', margin: 0,
          }}>
            {question.text}
          </pre>
        </div>

        {/* Feedback overlay */}
        {feedback && (
          <div style={{
            padding: '14px 20px', borderRadius: 12, marginBottom: 16,
            background: feedback.is_correct ? 'rgba(34,197,94,0.1)' : 'rgba(239,68,68,0.1)',
            border: `1px solid ${feedback.is_correct ? '#22c55e40' : '#ef444440'}`,
          }}>
            <p style={{ margin: 0, fontWeight: 700, color: feedback.is_correct ? '#22c55e' : '#ef4444' }}>
              {feedback.is_correct ? '✓ To\'g\'ri!' : '✗ Noto\'g\'ri'}
            </p>
            {feedback.explanation && (
              <p style={{ margin: '6px 0 0', fontSize: 13, color: 'var(--text-secondary)' }}>
                {feedback.explanation}
              </p>
            )}
          </div>
        )}

        {/* MCQ options */}
        {question.type === 'mcq' && !feedback && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 24 }}>
            {question.options.map((opt, i) => (
              <button
                key={i}
                onClick={() => setSelected(opt)}
                style={{
                  padding: '14px 20px', borderRadius: 10, textAlign: 'left',
                  border: `2px solid ${selected === opt ? 'var(--primary-400)' : 'var(--border)'}`,
                  background: selected === opt ? 'rgba(99,102,241,0.1)' : 'var(--surface)',
                  color: 'var(--text-primary)', cursor: 'pointer', fontSize: 14,
                  fontFamily: "'Fira Code', monospace",
                  transition: 'all 0.15s',
                }}
              >
                <span style={{ color: 'var(--text-tertiary)', marginRight: 10 }}>
                  {String.fromCharCode(65 + i)}.
                </span>
                {opt}
              </button>
            ))}
          </div>
        )}

        {/* Code answer */}
        {question.type === 'code' && !feedback && (
          <div style={{ marginBottom: 24 }}>
            {question.code_template && (
              <div style={{
                background: 'rgba(0,0,0,0.3)', borderRadius: '8px 8px 0 0',
                padding: '8px 16px', fontSize: 12, color: 'var(--text-tertiary)',
              }}>
                Boshlang'ich kod:
                <pre style={{ margin: '4px 0 0', fontFamily: "'Fira Code', monospace", fontSize: 13, color: 'var(--text-secondary)' }}>
                  {question.code_template}
                </pre>
              </div>
            )}
            <textarea
              value={codeAnswer}
              onChange={e => setCodeAnswer(e.target.value)}
              placeholder="Kodingizni shu yerga yozing..."
              style={{
                width: '100%', minHeight: 140,
                background: 'var(--surface)', border: '2px solid var(--border)',
                borderRadius: question.code_template ? '0 0 8px 8px' : 8,
                padding: '12px 16px', color: 'var(--text-primary)',
                fontFamily: "'Fira Code', monospace", fontSize: 14,
                resize: 'vertical', outline: 'none',
                boxSizing: 'border-box',
              }}
            />
          </div>
        )}

        {!feedback && (
          <button
            className="btn btn-primary"
            style={{ width: '100%', padding: '14px', fontSize: 15, fontWeight: 700 }}
            onClick={submitAnswer}
            disabled={loading || (!selected && !codeAnswer)}
          >
            {loading ? 'Tekshirilmoqda...' : 'Javobni yuborish'}
          </button>
        )}
      </div>
    );
  }

  // ── RESULT ─────────────────────────────────────────────
  if (phase === 'result' && result) {
    const lvl = LEVEL_INFO[result.level] || LEVEL_INFO.beginner;
    return (
      <div className="site-container" style={{ maxWidth: 700, margin: '40px auto' }}>
        {/* Score card */}
        <div style={{
          background: 'var(--surface)', border: '1px solid var(--border)',
          borderRadius: 20, padding: '36px 32px', textAlign: 'center', marginBottom: 24,
        }}>
          <div style={{ fontSize: 56, marginBottom: 8 }}>{lvl.emoji}</div>
          <h2 style={{ fontSize: 28, fontWeight: 800, marginBottom: 4 }}>{lvl.label}</h2>
          <p style={{ fontSize: 48, fontWeight: 900, color: lvl.color, margin: '8px 0' }}>
            {result.percentage}%
          </p>
          <p style={{ color: 'var(--text-secondary)' }}>
            {result.total_score} / {result.max_score} ball
          </p>
        </div>

        {/* AI tahlil */}
        {result.ai_analysis && (
          <div style={{
            background: 'rgba(139,92,246,0.08)', border: '1px solid rgba(139,92,246,0.2)',
            borderRadius: 16, padding: '20px 24px', marginBottom: 24,
          }}>
            <h4 style={{ margin: '0 0 12px', color: '#a855f7', fontSize: 15 }}>
              🤖 AI Tahlil
            </h4>
            <p style={{ margin: 0, color: 'var(--text-secondary)', lineHeight: 1.7 }}>
              {result.ai_analysis}
            </p>
          </div>
        )}

        {/* Kupon */}
        {result.coupon_code && (
          <div style={{
            background: 'rgba(232,184,75,0.1)', border: '2px dashed #e8b84b',
            borderRadius: 16, padding: '20px 24px', marginBottom: 24, textAlign: 'center',
          }}>
            <p style={{ margin: '0 0 8px', color: 'var(--text-secondary)', fontSize: 14 }}>
              Sizga chegirma kuponi berildi!
            </p>
            <div style={{
              fontSize: 28, fontWeight: 900, color: '#e8b84b',
              letterSpacing: 4, marginBottom: 8,
            }}>
              {result.coupon_code}
            </div>
            <p style={{ margin: 0, color: '#e8b84b', fontWeight: 700 }}>
              {result.discount}% chegirma • {result.coupon_until} gacha
            </p>
          </div>
        )}

        {/* Kuchli/zaif mavzular */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 24 }}>
          {result.strong_topics?.length > 0 && (
            <div style={{ background: 'rgba(34,197,94,0.08)', border: '1px solid rgba(34,197,94,0.2)', borderRadius: 12, padding: '16px 20px' }}>
              <h5 style={{ margin: '0 0 10px', color: '#22c55e' }}>Kuchli mavzular</h5>
              {result.strong_topics.map(t => (
                <div key={t} style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 4 }}>
                  ✓ {TOPIC_LABELS[t] || t}
                </div>
              ))}
            </div>
          )}
          {result.weak_topics?.length > 0 && (
            <div style={{ background: 'rgba(239,68,68,0.08)', border: '1px solid rgba(239,68,68,0.2)', borderRadius: 12, padding: '16px 20px' }}>
              <h5 style={{ margin: '0 0 10px', color: '#ef4444' }}>O'rganish kerak</h5>
              {result.weak_topics.map(t => (
                <div key={t} style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 4 }}>
                  ✗ {TOPIC_LABELS[t] || t}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Tavsiya qilingan kurslar */}
        {result.recommended_courses?.length > 0 && (
          <div style={{ marginBottom: 28 }}>
            <h3 style={{ marginBottom: 16 }}>Tavsiya qilingan kurslar</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {result.recommended_courses.map(c => (
                <div key={c.id} style={{
                  background: 'var(--surface)', border: '1px solid var(--border)',
                  borderRadius: 12, padding: '14px 20px',
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                }}>
                  <span style={{ fontWeight: 600 }}>{c.title}</span>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                    <span style={{ color: 'var(--primary-400)', fontWeight: 700 }}>
                      {c.is_free || Number(c.price) === 0
                        ? 'Bepul'
                        : Number(c.price).toLocaleString('fr-FR') + " so'm"}
                    </span>
                    <button
                      className="btn btn-primary btn-sm"
                      onClick={() => navigate('/courses/' + c.id)}
                    >
                      Ko'rish
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div style={{ display: 'flex', gap: 12 }}>
          <button
            className="btn btn-outline-secondary"
            style={{ flex: 1 }}
            onClick={() => navigate('/courses')}
          >
            Kurslarga o'tish
          </button>
          <button
            className="btn btn-primary"
            style={{ flex: 1 }}
            onClick={() => navigate('/profile')}
          >
            Profilga qaytish
          </button>
        </div>
      </div>
    );
  }

  return null;
}
