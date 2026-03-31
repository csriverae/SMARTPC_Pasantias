'use client'

import { useState, useCallback } from 'react'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'

export interface ApiResponse<T> {
  message: string
  status: number
  error: boolean
  data: T
}

export interface ApiError {
  message: string
  status: number
  error: boolean
}

/**
 * Hook para hacer llamadas a la API con manejo de errores
 */
export const useApi = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<ApiError | null>(null)

  const request = useCallback(
    async <T = any,>(
      endpoint: string,
      method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' = 'GET',
      body?: any,
      token?: string
    ): Promise<ApiResponse<T> | null> => {
      try {
        setLoading(true)
        setError(null)

        const headers: HeadersInit = {
          'Content-Type': 'application/json',
        }

        // Obtener token del localStorage si no se proporciona
        const authToken = token || (typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null)

        if (authToken) {
          headers['Authorization'] = `Bearer ${authToken}`
        }

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
          method,
          headers,
          body: body ? JSON.stringify(body) : undefined,
        })

        const data = await response.json()

        if (!response.ok) {
          setError({
            message: data.message || 'An error occurred',
            status: response.status,
            error: true,
          })
          return null
        }

        setLoading(false)
        return data as ApiResponse<T>
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Unknown error'
        setError({
          message: errorMessage,
          status: 0,
          error: true,
        })
        setLoading(false)
        return null
      }
    },
    []
  )

  return { request, loading, error }
}

/**
 * Hook para operaciones de Tenant
 */
export const useTenants = () => {
  const { request, loading, error } = useApi()

  const createTenant = useCallback(
    async (name: string) => {
      return request<any>('/tenants', 'POST', { name })
    },
    [request]
  )

  const listTenants = useCallback(
    async (skip: number = 0, limit: number = 100) => {
      return request<any[]>('/tenants', 'GET')
    },
    [request]
  )

  const getTenant = useCallback(
    async (tenantId: number) => {
      return request<any>(`/tenants/${tenantId}`, 'GET')
    },
    [request]
  )

  const updateTenant = useCallback(
    async (tenantId: number, name: string) => {
      return request<any>(`/tenants/${tenantId}`, 'PATCH', { name })
    },
    [request]
  )

  const deleteTenant = useCallback(
    async (tenantId: number) => {
      return request<any>(`/tenants/${tenantId}`, 'DELETE')
    },
    [request]
  )

  return { createTenant, listTenants, getTenant, updateTenant, deleteTenant, loading, error }
}

/**
 * Hook para operaciones de Restaurant
 */
export const useRestaurants = () => {
  const { request, loading, error } = useApi()

  const createRestaurant = useCallback(
    async (data: {
      name: string
      description?: string
      address?: string
      phone?: string
      email?: string
    }) => {
      return request<any>('/restaurants', 'POST', data)
    },
    [request]
  )

  const listRestaurants = useCallback(
    async (skip: number = 0, limit: number = 100) => {
      return request<any[]>(`/restaurants?skip=${skip}&limit=${limit}`, 'GET')
    },
    [request]
  )

  const getRestaurant = useCallback(
    async (restaurantId: number) => {
      return request<any>(`/restaurants/${restaurantId}`, 'GET')
    },
    [request]
  )

  const updateRestaurant = useCallback(
    async (restaurantId: number, data: any) => {
      return request<any>(`/restaurants/${restaurantId}`, 'PATCH', data)
    },
    [request]
  )

  const deleteRestaurant = useCallback(
    async (restaurantId: number) => {
      return request<any>(`/restaurants/${restaurantId}`, 'DELETE')
    },
    [request]
  )

  return { createRestaurant, listRestaurants, getRestaurant, updateRestaurant, deleteRestaurant, loading, error }
}

/**
 * Hook para obtener tenant_id del token JWT
 */
export const useTenantFromToken = () => {
  const [tenantId, setTenantId] = useState<number | null>(null)

  const extractTenantId = useCallback(() => {
    if (typeof window === 'undefined') return

    const token = localStorage.getItem('accessToken')
    if (!token) return

    try {
      // Decodificar JWT sin verificar firma (solo para cliente)
      const parts = token.split('.')
      if (parts.length !== 3) return

      const decoded = JSON.parse(atob(parts[1]))
      setTenantId(decoded.tenant_id)
      return decoded.tenant_id
    } catch (err) {
      console.error('Error decoding token:', err)
    }
  }, [])

  return { tenantId, extractTenantId }
}
