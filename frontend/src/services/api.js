import axios from 'axios';

const API_URL = 'http://localhost:8000';

// Create an Axios instance with a base URL
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Program endpoints
export const programsApi = {
  getAll: () => api.get('/programs/'),
  create: (programData) => api.post('/programs/', programData),
};

// Client endpoints
export const clientsApi = {
  getAll: (search = '') => api.get(`/clients/?search=${search}`),
  getById: (id) => api.get(`/clients/${id}`),
  create: (clientData) => api.post('/clients/', clientData),
};

// Enrollment endpoints
export const enrollmentsApi = {
  createEnrollment: (clientId, enrollmentData) => 
    api.post(`/clients/${clientId}/enrollments/`, enrollmentData),
};

export default {
  programsApi,
  clientsApi,
  enrollmentsApi,
}; 