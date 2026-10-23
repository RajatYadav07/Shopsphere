import axios from 'axios';

export const getApiBaseUrl = (): string => {
  if (typeof window !== 'undefined') {
    const custom = localStorage.getItem('shopsphere_api_url');
    if (custom) return custom.trim();
  }
  return import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';
};

export const apiClient = axios.create({
  baseURL: getApiBaseUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

// Update baseURL dynamically per request if changed in storage
apiClient.interceptors.request.use((config) => {
  config.baseURL = getApiBaseUrl();
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const errorMsg =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'An unexpected network error occurred';
    console.error('API Error:', errorMsg);
    return Promise.reject(new Error(errorMsg));
  }
);
