import api from "./api";
import axios from "axios";

export const getQuiz = (quizId) => api.get(`/quiz/${quizId}`);
export const submitQuiz = (id, answers) =>
  api.post(`/quiz/${id}/submit/`, { answers });


export const getUserQuizResult = async (quizId) => {
  const token = localStorage.getItem("access_token");

  if (!token) {
    console.error("No access token found");
    return null;
  }

  try {
    const res = await api.get(`/quiz_result/?quiz=${quizId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return res.data;
  } catch (err) {
    console.error("Error fetching user quiz result:", err.response || err);
    return null;
  }
};

export const getQuizByLesson = (lessonId) => api.get(`/quiz/?lesson=${lessonId}`);
