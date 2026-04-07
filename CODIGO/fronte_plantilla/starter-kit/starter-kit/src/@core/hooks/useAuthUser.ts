'use client'

import { useState, useEffect } from 'react'

export interface AuthUser {
  id?: string
  full_name: string
  email: string
  role: 'admin' | 'employee'
  avatar?: string
  tenant_name?: string
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
          const normalizedUser = parsedUser?.data?.data || parsedUser
          const role = normalizedUser.role || normalizedUser.tenant_role
          if (role) {
            normalizedUser.role = role
          }
          setUser(normalizedUser)
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

      const tenant = localStorage.getItem('tenant_id')
      const response = await fetch('http://localhost:8000/auth/me', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
          'X-Tenant-ID': tenant || '',
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`)
      }

      const json = await response.json()
      const userData = json?.data?.data || json
      const role = userData.role || userData.tenant_role
      if (role) {
        userData.role = role
      }
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
