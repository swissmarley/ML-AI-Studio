import axios from 'axios'

// Get API URL from environment variable
// In development with Vite proxy, we can use relative URLs
// In production or when VITE_API_URL is set, use that
const API_URL = import.meta.env.VITE_API_URL || ''
const BASE_URL = API_URL ? `${API_URL}/api/v1` : '/api/v1'

console.log('API URL configured:', API_URL || 'Using relative URL (Vite proxy)')
console.log('Base URL:', BASE_URL)

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout (increased for debugging)
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle token expiration and network errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Log network errors for debugging
    if (!error.response) {
      console.error('Network Error:', {
        message: error.message,
        code: error.code,
        config: {
          url: error.config?.url,
          baseURL: error.config?.baseURL,
          method: error.config?.method
        }
      })
    }
    
    // Authentication disabled - no redirect on 401
    // if (error.response?.status === 401) {
    //   localStorage.removeItem('token')
    //   window.location.href = '/login'
    // }
    return Promise.reject(error)
  }
)

export default api

