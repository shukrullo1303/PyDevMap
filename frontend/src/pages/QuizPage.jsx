import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getQuiz, submitQuiz, getUserQuizResult } from "../services/quiz";
import Quiz from "../components/Quiz";
import "../styles/pages/QuizPage.css";

const QuizPage = () => {
    const { id } = useParams();   // id = quiz ID
    const navigate = useNavigate();

    const [quiz, setQuiz] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [showQuiz, setShowQuiz] = useState(true); // Quiz ko‘rinishi

    useEffect(() => {
        loadQuiz();
    }, [id]);

    const loadQuiz = async () => {
        setLoading(true);
        try {
            const res = await getQuiz(id); // quiz ID bo‘yicha
            const quizData = res.data;
            setQuiz(quizData);

            // User natijasini olish
            const resultRes = await getUserQuizResult(quizData.id);
            if (resultRes && resultRes.length > 0) {
                setResult(resultRes[0]);
                setShowQuiz(false); // agar natija bo‘lsa, quizni ko‘rsatmaymiz
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
            setShowQuiz(false); // submit qilgandan keyin quizni yashirish
        } catch (e) {
            console.error("Submit error:", e);
        } finally {
            setSubmitting(false);
        }
    };

    const handleRetake = () => {
        setResult(null);
        setShowQuiz(true);
    };

    if (loading) return <div className="site-container">Loading...</div>;
    if (!quiz) return <div className="site-container">No quiz found</div>;

    const passed = result && result.score >= 80;
    const correctAnswers = result ? result.correct_answers : 0;
    const totalQuestions = quiz.questions.length;

    return (
        <div className="site-container quiz-page">
            <h1>{quiz.title}</h1>

            {showQuiz ? (
                <Quiz quiz={quiz} onSubmit={handleSubmit} submitting={submitting} />
            ) : (
                <div className="quiz-result">
                    {result && (
                        <>
                            <h2>{passed ? "Passed" : "Failed"}</h2>
                            <p>
                                <b>Score:</b> {result.score}%
                            </p>
                            <p>
                                <b>Correct:</b> {correctAnswers} / {totalQuestions}
                            </p>
                        </>
                    )}

                    <div className="quiz-actions d-flex gap-2 mt-3">
                        <button className="btn btn-primary" onClick={handleRetake}>
                            Retake Quiz
                        </button>
                        <button
                            className="btn btn-success"
                            onClick={() => navigate(`/lessons/${quiz.lesson}`)}
                        >
                            Back to Lesson
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default QuizPage;
