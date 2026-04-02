'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'

export default function DashboardLayout({ children }) {
  const pathname = usePathname()
  const router = useRouter()
  const [isOpen, setIsOpen] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
    }
  }, [router])

  const isActive = (href) => {
    return pathname === href || pathname.endsWith(href)
  }

  const menuItems = [
    { title: 'Dashboard', href: '/home', icon: '📊' },
    { title: 'Empresas', href: '/companies', icon: '🏢' },
    { title: 'Empleados', href: '/employees', icon: '👥' },
    { title: 'Consumos', href: '/meal-logs', icon: '🍽️' },
    { title: 'Profile', href: '/profile', icon: '👤' },
    { title: 'Settings', href: '/settings', icon: '⚙️' },
    { title: 'Pricing', href: '/pricing', icon: '💰' },
    { title: 'FAQ', href: '/faq', icon: '❓' }
  ]

  return (
    <div className='flex bg-slate-50 min-h-screen'>
      {/* Fixed Sidebar */}
      <aside className={`fixed left-0 top-0 h-screen bg-white border-r border-slate-200 transition-all duration-300 flex flex-col shadow-lg z-40 ${
        isOpen ? 'w-64' : 'w-20'
      }`}>
        {/* Logo Header */}
        <div className='flex items-center justify-between p-4 border-b border-slate-200'>
          {isOpen && (
            <h1 className='text-xl font-bold text-indigo-600'>MesaPass</h1>
          )}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className='p-2 hover:bg-slate-100 rounded-lg transition-colors ml-auto'
            title={isOpen ? 'Collapse sidebar' : 'Expand sidebar'}
          >
            {isOpen ? '◀' : '▶'}
          </button>
        </div>

        {/* Navigation Menu */}
        <nav className='flex-1 p-4 space-y-2'>
          {menuItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                isActive(item.href)
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'text-slate-700 hover:bg-slate-100'
              }`}
              title={!isOpen ? item.title : ''}
            >
              <span className='text-xl flex-shrink-0'>{item.icon}</span>
              {isOpen && <span className='font-medium'>{item.title}</span>}
            </Link>
          ))}
        </nav>

        {/* Divider */}
        <div className='border-t border-slate-200'></div>

        {/* Exit Button */}
        <div className='p-4'>
          <button
            onClick={() => router.push('/')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg bg-red-50 text-red-700 hover:bg-red-100 transition-colors font-medium ${
              !isOpen ? 'justify-center' : ''
            }`}
            title={!isOpen ? 'Exit dashboard' : ''}
          >
            <span className='text-xl flex-shrink-0'>🚪</span>
            {isOpen && <span>Exit Dashboard</span>}
          </button>
        </div>
      </aside>

      {/* Main Content Area - Dynamic margin based on sidebar state */}
      <main className={`flex-1 overflow-auto transition-all duration-300 ${
        isOpen ? 'ml-64' : 'ml-20'
      }`}>
        <div className='min-h-screen'>
          {children}
        </div>
      </main>
    </div>
  )
}
