'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useState } from 'react'

export default function DashboardSidebar() {
  const pathname = usePathname()
  const router = useRouter()
  const [isOpen, setIsOpen] = useState(true)

  const isActive = (href) => {
    return pathname === href || pathname.endsWith(href)
  }

  const menuItems = [
    { title: 'Inicio', href: '/home', icon: '📊' },
    { title: 'Perfil', href: '/profile', icon: '👤' },
    { title: 'Configuración', href: '/settings', icon: '⚙️' },
    { title: 'Planes', href: '/pricing', icon: '💰' },
    { title: 'Ayuda', href: '/faq', icon: '❓' }
  ]

  return (
    <aside className={`fixed left-0 top-0 h-screen bg-white border-r border-slate-200 transition-all duration-300 flex flex-col shadow-lg ${
      isOpen ? 'w-64' : 'w-20'
    }`}>
      {/* Logo Header */}
      <div className='flex items-center justify-between p-4 border-b border-slate-200'>
        {isOpen && (
          <h1 className='text-xl font-bold text-indigo-600'>MesaPass</h1>
        )}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className='p-2 hover:bg-slate-100 rounded-lg transition-colors'
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
            <span className='text-xl'>{item.icon}</span>
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
          <span className='text-xl'>🚪</span>
          {isOpen && <span>Exit Dashboard</span>}
        </button>
      </div>
    </aside>
  )
}
