'use client'

import { useState, useEffect } from 'react'

export interface AuthUser {
  id?: string
  full_name: string
  email: string
  role: 'admin' | 'employee'
  avatar?: string
}

export interface UseAuthUserReturn {
  user: AuthUser | null
  loading: boolean
  error: string | null
  refetch: () => Promise<void>
}

export const useAuthUser = (): UseAuthUserReturn => {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchUser = async () => {
    try {
      setLoading(true)
      setError(null)

      // Intenta obtener del localStorage primero
      const storedUser = localStorage.getItem('user')
      if (storedUser) {
        try {
          const parsedUser = JSON.parse(storedUser)
          setUser(parsedUser)
          setLoading(false)
          return
        } catch (e) {
          console.warn('Error parseando usuario del localStorage:', e)
        }
      }

      // Si no está en localStorage, obtén del endpoint
      const token = localStorage.getItem('token')
      if (!token) {
        setError('No authenticated')
        setLoading(false)
        return
      }

      const response = await fetch('http://localhost:8000/auth/me', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        if (response.status === 401 || response.status === 403) {
          localStorage.removeItem('token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user')
          setError('Unauthorized. Please login again.')
          setUser(null)
          setLoading(false)
          return
        }

        const errorText = await response.text()
        throw new Error(`Error: ${response.status} ${response.statusText} ${errorText}`)
      }

      const responseData = await response.json()
      // Extraer el usuario del objeto data
      const userData = responseData.data || responseData
      setUser(userData)
      // Guardar en localStorage para futuras cargas
      localStorage.setItem('user', JSON.stringify(userData))
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error fetching user'
      setError(message)
      setUser(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchUser()
  }, [])

  return {
    user,
    loading,
    error,
    refetch: fetchUser
  }
}
