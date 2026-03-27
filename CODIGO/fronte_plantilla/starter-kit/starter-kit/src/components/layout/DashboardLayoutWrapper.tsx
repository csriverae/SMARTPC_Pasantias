'use client'

import { useRouter, usePathname } from 'next/navigation'
import { useState } from 'react'

interface MenuItem {
  label: string
  icon: string
  href: string
  badge?: number | null
}

interface DashboardLayoutProps {
  children: React.ReactNode
}

export default function DashboardLayoutWrapper({ children }: DashboardLayoutProps) {
  const router = useRouter()
  const pathname = usePathname()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const menuItems: MenuItem[] = [
    {
      label: 'My Profile',
      icon: '👤',
      href: '/profile'
    },
    {
      label: 'Settings',
      icon: '⚙️',
      href: '/settings'
    },
    {
      label: 'Pricing',
      icon: '💰',
      href: '/pricing'
    },
    {
      label: 'FAQ',
      icon: '❓',
      href: '/faq'
    }
  ]

  const isActive = (href: string) => pathname.includes(href)

  const handleNavigation = (href: string) => {
    router.push(href)
  }

  const handleBackHome = () => {
    router.push('/')
  }

  return (
    <div className='flex min-h-screen bg-slate-50'>
      {/* Sidebar */}
      <aside
        className={`${
          sidebarOpen ? 'w-64' : 'w-20'
        } bg-white border-r border-slate-200 transition-all duration-300 flex flex-col shadow-sm sticky top-0 h-screen`}
      >
        {/* Header */}
        <div className='p-4 border-b border-slate-200 flex items-center justify-between'>
          {sidebarOpen && <h2 className='text-lg font-bold text-slate-900'>MesaPass</h2>}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className='p-2 hover:bg-slate-100 rounded-lg transition-colors ml-auto'
            title={sidebarOpen ? 'Collapse' : 'Expand'}
          >
            {sidebarOpen ? '◀' : '▶'}
          </button>
        </div>

        {/* Navigation Items */}
        <nav className='flex-1 p-4 space-y-2'>
          {menuItems.map((item) => (
            <button
              key={item.href}
              onClick={() => handleNavigation(item.href)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                isActive(item.href)
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'text-slate-700 hover:bg-slate-100'
              }`}
              title={!sidebarOpen ? item.label : ''}
            >
              <span className='text-xl flex-shrink-0'>{item.icon}</span>
              {sidebarOpen && (
                <span className='font-medium flex-1 text-left'>{item.label}</span>
              )}
              {sidebarOpen && item.badge && (
                <span className='bg-red-500 text-white text-xs rounded-full px-2 py-1'>
                  {item.badge}
                </span>
              )}
            </button>
          ))}
        </nav>

        {/* Divider */}
        <div className='border-t border-slate-200'></div>

        {/* Back to Home Button */}
        <div className='p-4'>
          <button
            onClick={handleBackHome}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors font-medium ${
              !sidebarOpen ? 'justify-center' : ''
            }`}
            title={!sidebarOpen ? 'Back to Home' : ''}
          >
            <span className='text-xl flex-shrink-0'>🏠</span>
            {sidebarOpen && <span>Back to Home</span>}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className='flex-1 overflow-auto'>
        <div className='min-h-screen'>{children}</div>
      </main>
    </div>
  )
}
