import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getLesson, markLessonCompleted } from "../services/lessons";
import { getQuizByLesson, getUserQuizResult } from "../services/quiz";
import "../styles/pages/LessonDetailPage.css";

export default function LessonDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [lesson, setLesson] = useState(null);
  const [quiz, setQuiz] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLesson();
  }, [id]);

  const loadLesson = async () => {
    setLoading(true);
    try {
      // 1️⃣ Lessonni olish
      const res = await getLesson(id);
      const lessonData = res.data;
      setLesson(lessonData);

      // 2️⃣ Quizni olish
      try {
        const quizRes = await getQuizByLesson(lessonData.id); // lesson_id asosida
        if (quizRes.data.length > 0) {
          const quizData = quizRes.data[0]; // birinchi quizni olamiz
          setQuiz(quizData);

          // 3️⃣ User natijasini olish
          const resultRes = await getUserQuizResult(quizData.id); // quiz_id bilan
          if (resultRes && resultRes.length > 0) {
            setResult(resultRes[0].score); // array dan score olish
          }
        }
      } catch (err) {
        console.log("Quiz yoki natija yo‘q", err);
      }

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

  if (loading) return <div className="site-container">Loading...</div>;

  return (
    <div className="site-container lesson-detail-page">
      <h1>{lesson.title}</h1>

      {lesson.video_url && (
        <div className="video-container">
          <iframe
            src={`https://www.youtube.com/embed/${lesson.video_url.split("youtu.be/")[1]}`}
            title="YouTube video player"
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          ></iframe>
        </div>
      )}

      {/* ================= QUIZ BLOCK ================= */}
      {quiz && (
        <div className="quiz-box">
          {!result ? (
            <button
              className="btn btn-primary"
              onClick={() => navigate(`/quiz/${quiz.id}`)}
            >
              Testni ishlash
            </button>
          ) : (
            <div className="d-flex justify-content-between align-items-center">
              <button
                className="btn btn-primary my-3"
                onClick={() => navigate(`/quiz/${quiz.id}`)}
              >
                Testni qayta ishlash
              </button>
              <p>Test natijangiz: {result} %</p>
            </div>
          )}
        </div>
      )}

      {/* ================= NAV ================= */}
      <div className="lesson-nav d-flex justify-content-between">
        {lesson.prev_lesson_id ? (
          <button
            className="btn btn-outline-secondary my-3"
            onClick={() => navigate(`/lessons/${lesson.prev_lesson_id}`)}
          >
            ← Avvalgi dars
          </button>
        ) : (
          <div></div>
        )}

        {lesson.next_lesson_id && (
          <button
            className="btn btn-success mb-3"
            disabled={!(result >= 80)}
            onClick={goNext}
          >
            Keyingi dars →
          </button>
        )}
      </div>
    </div>
  );
}
