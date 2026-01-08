import api from './api';

export const login =  (username, password) =>
    api.post('auth/token/', { username, password });


export const register = (payload) => api.post('auth/register/', payload);


export const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
};

export const getProfile = () => api.get('auth/me/');

export const setTokens = ({ access, refresh }) => {
    if (access) localStorage.setItem('access_token', access);
    if (refresh) localStorage.setItem('refresh_token', refresh);
};

