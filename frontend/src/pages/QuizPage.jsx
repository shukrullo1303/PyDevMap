import React, { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { getQuiz, submitQuiz, getUserQuizResult } from "../services/quiz";
import Quiz from "../components/Quiz";
import "../styles/pages/QuizPage.css";

const DIFF_COLOR = {
    Beginner:     '#22c55e',
    Intermediate: '#e8b84b',
    Professional: '#ef4444',
};

const QuizPage = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    const [quiz, setQuiz]           = useState(null);
    const [result, setResult]       = useState(null);
    const [loading, setLoading]     = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [showQuiz, setShowQuiz]   = useState(true);

    useEffect(() => { loadQuiz(); }, [id]);

    const loadQuiz = async () => {
        setLoading(true);
        try {
            const res = await getQuiz(id);
            const quizData = res.data;
            setQuiz(quizData);

            const resultRes = await getUserQuizResult(quizData.id);
            if (resultRes && resultRes.length > 0) {
                setResult(resultRes[0]);
                setShowQuiz(false);
            } else {
                setShowQuiz(true);
            }
        } catch (e) {
            console.error("Quiz load error", e);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (answers) => {
        if (!quiz) return;
        setSubmitting(true);
        try {
            const res = await submitQuiz(quiz.id, answers);
            setResult(res.data);
            setShowQuiz(false);
        } catch (e) {
            console.error("Submit error:", e);
        } finally {
            setSubmitting(false);
        }
    };

    const handleRetake = () => { setResult(null); setShowQuiz(true); };

    if (loading) return (
        <div className="loading-state">
            <div className="loading-spinner" />
            <p>Yuklanmoqda...</p>
        </div>
    );
    if (!quiz) return <div className="empty-state"><p>Test topilmadi</p></div>;

    const passed         = result && result.score >= 80;
    const totalQuestions = quiz.questions?.length || 0;
    const hasRelatedTask = quiz.related_task_id;

    return (
        <div className="site-container quiz-page">
            {/* Header */}
            <div style={{ marginBottom: 24 }}>
                <div style={{ fontSize: 13, color: 'var(--text-tertiary)', marginBottom: 8 }}>
                    <button
                        onClick={() => navigate(-1)}
                        style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-tertiary)', fontSize: 13, padding: 0 }}
                    >
                        ← Darsga qaytish
                    </button>
                </div>
                <h1 style={{ fontSize: 22, marginBottom: 4 }}>
                    {quiz.title || 'Test'}
                </h1>
                <p style={{ color: 'var(--text-tertiary)', fontSize: 13, margin: 0 }}>
                    {totalQuestions} ta savol
                </p>
            </div>

            {showQuiz ? (
                <Quiz quiz={quiz} onSubmit={handleSubmit} submitting={submitting} />
            ) : (
                <div className="quiz-result">
                    {result && (
                        <>
                            {/* Natija banner */}
                            <div style={{
                                width: 72, height: 72, borderRadius: '50%',
                                background: passed ? 'rgba(34,197,94,0.12)' : 'rgba(239,68,68,0.12)',
                                border: `2px solid ${passed ? '#22c55e' : '#ef4444'}`,
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                fontSize: 32, margin: '0 auto 16px',
                            }}>
                                {passed ? '🎉' : '😔'}
                            </div>

                            <h2 style={{
                                color: passed ? '#22c55e' : '#ef4444',
                                fontSize: 22, marginBottom: 8,
                            }}>
                                {passed ? 'Tabriklaymiz!' : 'Muvaffaqiyatsiz'}
                            </h2>

                            <div style={{
                                fontSize: 42, fontWeight: 800,
                                color: 'var(--text-primary)', marginBottom: 4,
                            }}>
                                {result.score}%
                            </div>
                            <p style={{ color: 'var(--text-tertiary)', fontSize: 13, marginBottom: 24 }}>
                                To'g'ri: {result.correct_answers ?? '?'} / {totalQuestions}
                                &nbsp;·&nbsp;
                                O'tish chegarasi: 80%
                            </p>

                            {/* Related task bloki */}
                            {hasRelatedTask && (
                                <div style={{
                                    margin: '0 auto 20px',
                                    maxWidth: 400,
                                    background: 'var(--surface-2)',
                                    border: '1.5px solid var(--primary-600)',
                                    borderRadius: 12,
                                    padding: '16px 20px',
                                    textAlign: 'left',
                                }}>
                                    <div style={{
                                        fontSize: 11, fontWeight: 700,
                                        color: 'var(--primary-600)',
                                        textTransform: 'uppercase', letterSpacing: '0.6px',
                                        marginBottom: 8,
                                    }}>
                                        ⚡ Keyingi qadam — masala
                                    </div>
                                    <div style={{
                                        fontWeight: 600, fontSize: 15,
                                        color: 'var(--text-primary)', marginBottom: 4,
                                    }}>
                                        {quiz.related_task_title}
                                    </div>
                                    {quiz.related_task_difficulty && (
                                        <div style={{
                                            display: 'inline-flex', alignItems: 'center', gap: 5,
                                            padding: '2px 10px', borderRadius: 999, fontSize: 11,
                                            fontWeight: 600, marginBottom: 12,
                                            color: DIFF_COLOR[quiz.related_task_difficulty] || '#9a9cb0',
                                            background: `${DIFF_COLOR[quiz.related_task_difficulty] || '#9a9cb0'}18`,
                                            border: `1px solid ${DIFF_COLOR[quiz.related_task_difficulty] || '#9a9cb0'}40`,
                                        }}>
                                            <span style={{
                                                width: 5, height: 5, borderRadius: '50%',
                                                background: DIFF_COLOR[quiz.related_task_difficulty] || '#9a9cb0',
                                            }} />
                                            {quiz.related_task_difficulty}
                                        </div>
                                    )}
                                    <br />
                                    <Link
                                        to={`/tasks/${quiz.related_task_id}`}
                                        style={{
                                            display: 'inline-flex', alignItems: 'center', gap: 6,
                                            padding: '8px 18px', borderRadius: 8,
                                            background: 'var(--primary-600)',
                                            color: '#0d0f17', fontWeight: 700, fontSize: 13,
                                            textDecoration: 'none',
                                        }}
                                    >
                                        ▶ Masalani yechish
                                    </Link>
                                </div>
                            )}

                            {/* Tugmalar */}
                            <div className="quiz-actions">
                                <button className="btn btn-outline-secondary" onClick={handleRetake}>
                                    Qayta ishlash
                                </button>
                                <button
                                    className="btn btn-secondary"
                                    onClick={() => navigate(`/lessons/${quiz.lesson}`)}
                                >
                                    Darsga qaytish
                                </button>
                            </div>
                        </>
                    )}
                </div>
            )}
        </div>
    );
};

export default QuizPage;
