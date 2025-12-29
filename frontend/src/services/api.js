import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const api = axios.create({
  baseURL: API,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chatbot APIs
export const chatbotAPI = {
  create: (data) => api.post('/chatbots', data),
  getAll: (params) => api.get('/chatbots', { params }),
  getById: (id) => api.get(`/chatbots/${id}`),
  update: (id, data) => api.put(`/chatbots/${id}`, data),
  delete: (id) => api.delete(`/chatbots/${id}`),
  getStats: (id) => api.get(`/chatbots/${id}/stats`),
};

// Stats APIs
export const statsAPI = {
  getGlobal: () => api.get('/stats'),
};

// Conversation APIs
export const conversationAPI = {
  create: (data) => api.post('/conversations', data),
  update: (id, data) => api.put(`/conversations/${id}`, data),
  getById: (id) => api.get(`/conversations/${id}`),
};

export default api;