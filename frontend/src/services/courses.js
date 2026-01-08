import api from './api';

// Kategoriyalar
export const getCategories = () => api.get('courses/categories/');

// Kategoriya bo'yicha kurslar
export const getCategory = (id) => api.get(`/categories/${id}/`);

// Kurslar ro'yxati
export const getCourses = () => api.get('courses/');

// Kurs detali
export const getCourse = (id) => api.get(`courses/${id}/`);

// Enrollments
// export const enrollCourse = async (courseId) => {
//   return api.post(`courses/${courseId}/enroll/`);
// };

// export const checkEnrolled = (courseId) =>
//   api.get(`courses/${courseId}/is-enrolled/`);