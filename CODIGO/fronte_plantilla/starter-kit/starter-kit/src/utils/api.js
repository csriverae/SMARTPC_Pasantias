import axios from 'axios'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  const tenant = localStorage.getItem('tenant_id')

  config.headers = config.headers || {}

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  if (tenant) {
    config.headers['X-Tenant-ID'] = tenant
  }

  return config
})

export default api