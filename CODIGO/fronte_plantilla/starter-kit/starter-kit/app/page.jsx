'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function Page() {
  const router = useRouter()

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token')
    
    if (token) {
      // Redirect to dashboard if logged in
      router.push('/dashboard')
    } else {
      // Redirect to login if not logged in
      router.push('/login')
    }
  }, [router])

  return (
    <div className='flex items-center justify-center min-h-screen'>
      <p className='text-lg'>Redirecting...</p>
    </div>
  )
}
