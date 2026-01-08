import api from './api';
import axios from 'axios';


export const getLessonProgress = (lessonId) =>
    api.get(`/lesson_progress/?lesson=${lessonId}`);

export const getLessonsByCourse = (courseId, token) =>
    api.get(`/lessons/?course=${courseId}`, { headers: { Authorization: `Bearer ${token}` } });

export const getLesson = (id, token) =>
    api.get(`/lessons/${id}/`, { headers: { Authorization: `Bearer ${token}` } });

export const markProgress = (lessonId, payload, token) =>
    api.post(`/lessons/${lessonId}/complete`, payload, { headers: { Authorization: `Bearer ${token}` } });



const API_URL = "http://localhost:8000/api"; // Django server

export const markLessonCompleted = async (lessonId) => {
    const token = localStorage.getItem("access_token");
    if (!token) {
        console.error("No token found!");
        return;
    }

    try {
        const res = await axios.post(
            `${API_URL}/lessons/${lessonId}/complete/`,
            {},
            { headers: { Authorization: `Bearer ${token}` } }
        );
        return res.data;
    } catch (err) {
        console.error("Mark complete error:", err);
        throw err;
    }
};