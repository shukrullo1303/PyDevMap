import api from './api';

export const getTasks = (params = {}) =>
    api.get('/compiler/tasks/', { params });

export const getTask = (id) =>
    api.get(`/compiler/tasks/${id}/`);

export const submitCode = (taskId, code) =>
    api.post(`/compiler/submit/${taskId}/`, { code });

export const runCode = (userCode, testCode) =>
    api.post('/compiler/run_code/', { user_code: userCode, test_code: testCode });

export const analyzeCode = (taskId, userCode, actualOutput) =>
    api.post('/compiler/analyze/', {
        task_id: taskId,
        user_code: userCode,
        actual_output: actualOutput,
    });
