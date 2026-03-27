'use client'

import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'

export type User = {
  id?: string
  full_name: string
  email: string
  role: 'admin' | 'employee'
  avatar?: string
}

export type AuthContextValue = {
  user: User | null
  token: string | null
  ready: boolean
  login: (token: string, user: User) => void
  logout: () => void
}

const AUTH_TOKEN_KEY = 'token'
const AUTH_USER_KEY = 'user'

const AuthContext = createContext<AuthContextValue>({
  user: null,
  token: null,
  ready: false,
  login: () => {},
  logout: () => {}
})

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const router = useRouter()
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [ready, setReady] = useState<boolean>(false)

  useEffect(() => {
    const storedToken = localStorage.getItem(AUTH_TOKEN_KEY)
    const storedUser = localStorage.getItem(AUTH_USER_KEY)

    if (storedToken && storedUser) {
      try {
        const parsedUser: User = JSON.parse(storedUser)
        setToken(storedToken)
        setUser(parsedUser)
      } catch (error) {
        localStorage.removeItem(AUTH_USER_KEY)
        setUser(null)
      }
    }

    setReady(true)
  }, [])

  const login = (newToken: string, newUser: User) => {
    localStorage.setItem(AUTH_TOKEN_KEY, newToken)
    localStorage.setItem(AUTH_USER_KEY, JSON.stringify(newUser))
    setToken(newToken)
    setUser(newUser)
    router.push('/home')
  }

  const logout = () => {
    localStorage.removeItem(AUTH_TOKEN_KEY)
    localStorage.removeItem(AUTH_USER_KEY)
    setToken(null)
    setUser(null)
    router.push('/login')
  }

  const value = useMemo(
    () => ({ user, token, ready, login, logout }),
    [user, token, ready]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
