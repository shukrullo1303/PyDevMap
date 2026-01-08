// services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE || 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach Authorization header if token present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});



// Token refresh logic
let isRefreshing = false;
let refreshQueue = [];

const processQueue = (error, token = null) => {
  refreshQueue.forEach((prom) => {
    if (error) prom.reject(error);
    else prom.resolve(token);
  });
  refreshQueue = [];
};

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (!error.response) {
      return Promise.reject(new Error('Network Error: Unable to reach API.'));
    }

    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      const refresh = localStorage.getItem('refresh_token');
      if (!refresh) return Promise.reject(error);

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          refreshQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return api(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const res = await axios.post(
          (process.env.REACT_APP_API_BASE || 'http://localhost:8000/api/') + 'auth/token/refresh/',
          { refresh }
        );
        const newAccess = res.data.access;
        localStorage.setItem('access_token', newAccess);
        api.defaults.headers.common.Authorization = `Bearer ${newAccess}`;
        processQueue(null, newAccess);
        return api(originalRequest);
      } catch (err) {
        processQueue(err, null);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default api;
