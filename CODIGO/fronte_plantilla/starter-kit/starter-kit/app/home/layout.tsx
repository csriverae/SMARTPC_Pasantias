'use client'

// Util Imports
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import LayoutWrapper from '@layouts/LayoutWrapper'
import { useSettings } from '@core/hooks/useSettings'
import VerticalLayout from '@layouts/VerticalLayout'

export default function HomeLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const { settings } = useSettings()

  useEffect(() => {
    // Verificar token
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
    if (!token) {
      router.push('/login')
    }
  }, [router])

  return (
    <LayoutWrapper>
      <VerticalLayout>
        {children}
      </VerticalLayout>
    </LayoutWrapper>
  )
}
