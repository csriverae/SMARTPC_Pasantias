'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useState } from 'react'

export default function DashboardLayoutWrapper({ children }) {
  const pathname = usePathname()
  const router = useRouter()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const menuItems = [
    {
      label: 'Dashboard',
      icon: '📊',
      href: '/home'
    },
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

  const isActive = (href) => pathname === href || pathname.endsWith(href)

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
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 w-full ${
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
            </Link>
          ))}
        </nav>

        {/* Divider */}
        <div className='border-t border-slate-200'></div>

        {/* Back to Home Button */}
        <div className='p-4'>
          <button
            onClick={handleBackHome}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg bg-red-50 text-red-700 hover:bg-red-100 transition-colors font-medium ${
              !sidebarOpen ? 'justify-center' : ''
            }`}
            title={!sidebarOpen ? 'Exit Dashboard' : ''}
          >
            <span className='text-xl flex-shrink-0'>🚪</span>
            {sidebarOpen && <span>Exit Dashboard</span>}
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
