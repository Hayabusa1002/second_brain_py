import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL

const client = axios.create({
  baseURL: `${BASE_URL}/api`,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
})

// Auto refresh in 401
client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config

    const isAuthEndpoint =
      original.url?.includes('/auth/login') ||
      original.url?.includes('/auth/refresh') ||
      original.url?.includes('/auth/register') ||
      original.url?.includes('/auth/me')

    if (error.response?.status === 401 && !original._retry && !isAuthEndpoint) {
      original._retry = true
      try {
        await axios.post(`${BASE_URL}/api/auth/refresh`, {}, { withCredentials: true })
        return client(original)
      } catch {
        // Only redirect when location isn't the login
        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }
      }
    }

    return Promise.reject(error)
  }
)

export default client