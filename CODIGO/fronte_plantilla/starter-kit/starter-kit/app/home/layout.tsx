'use client'

// React Imports
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

// Layout Imports
import LayoutWrapper from '@layouts/LayoutWrapper'
import VerticalLayout from '@layouts/VerticalLayout'

// Hook Imports
import { useSettings } from '@core/hooks/useSettings'

export default function HomeLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const { settings } = useSettings()

  useEffect(() => {
    // Check token
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

