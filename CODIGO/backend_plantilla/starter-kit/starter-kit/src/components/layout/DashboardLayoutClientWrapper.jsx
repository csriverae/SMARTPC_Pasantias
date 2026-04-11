'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import { useAuthUser } from '@core/hooks/useAuthUser'

export default function DashboardLayout({ children }) {
  const pathname = usePathname()
  const router = useRouter()
  const [isOpen, setIsOpen] = useState(true)
  const [showUserMenu, setShowUserMenu] = useState(false)
  const { user, loading } = useAuthUser()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
    }
  }, [router])

  useEffect(() => {
    if (!loading && !user) {
      localStorage.removeItem('token')
      localStorage.removeItem('tenant_id')
      localStorage.removeItem('user')
      router.push('/login')
    }
  }, [loading, user, router])

  const isActive = (href) => {
    return pathname === href || pathname.endsWith(href)
  }

  const menuGroups = [
    {
      label: 'Principal',
      items: [
        { title: 'Dashboard', href: '/home', icon: '📊' },
        { title: 'Perfil', href: '/profile', icon: '👤' }
      ]
    },
    {
      label: 'Operaciones',
      items: [
        { title: 'Empresas', href: '/companies', icon: '🏢' },
        { title: 'Restaurantes', href: '/restaurants', icon: '🍽️' },
        { title: 'Empleados', href: '/employees', icon: '👨‍💼' },
        { title: 'Acuerdos', href: '/agreements', icon: '📋' }
      ]
    },
    {
      label: 'Gestión',
      items: [
        { title: 'Usuarios', href: '/users', icon: '👥', roles: ['admin'] },
        { title: 'Registros de Consumo', href: '/meal-logs', icon: '🍴' },
        { title: 'Reportes', href: '/reports', icon: '📈' }
      ]
    },
    {
      label: 'Soporte',
      items: [
        { title: 'Centro de Ayuda', href: '/faq', icon: '❓' },
        { title: 'Configuración', href: '/settings', icon: '⚙️' }
      ]
    }
  ]

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('tenant_id')
    localStorage.removeItem('user')
    router.push('/login')
  }

  if (loading) {
    return (
      <div className='flex items-center justify-center min-h-screen bg-gradient-to-br from-indigo-50 to-blue-50'>
        <div className='text-center'>
          <div className='inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4'></div>
          <p className='text-gray-600'>Cargando información del usuario...</p>
        </div>
      </div>
    )
  }

  return (
    <div className='flex bg-gray-50 min-h-screen'>
      {/* Fixed Sidebar */}
      <aside className={`fixed left-0 top-0 h-screen bg-gradient-to-b from-indigo-600 to-indigo-700 transition-all duration-300 flex flex-col shadow-xl z-40 ${
        isOpen ? 'w-64' : 'w-20'
      }`}>
        {/* Logo Header */}
        <div className='flex items-center justify-between p-4 border-b border-indigo-500'>
          {isOpen && (
            <div className='flex items-center gap-2'>
              <div className='text-2xl'>🍽️</div>
              <h1 className='text-xl font-bold text-white'>MesaPass</h1>
            </div>
          )}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className='p-2 hover:bg-indigo-500 rounded-lg transition-colors text-white'
            title={isOpen ? 'Collapse sidebar' : 'Expand sidebar'}
          >
            {isOpen ? '◀' : '▶'}
          </button>
        </div>

        {/* Navigation Menu */}
        <nav className='flex-1 p-3 space-y-2 overflow-y-auto'>
          {menuGroups.map((group) => (
            <div key={group.label}>
              {isOpen && (
                <h3 className='text-xs font-semibold text-indigo-200 uppercase tracking-wider px-4 py-2 mt-4 first:mt-0'>
                  {group.label}
                </h3>
              )}
              <div className='space-y-1'>
                {group.items.map((item) => {
                  if (item.roles && !item.roles.includes(user?.role)) return null
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                        isActive(item.href)
                          ? 'bg-white text-indigo-600 shadow-lg font-semibold'
                          : 'text-indigo-100 hover:bg-indigo-500 hover:text-white'
                      }`}
                      title={!isOpen ? item.title : ''}
                    >
                      <span className='text-lg flex-shrink-0'>{item.icon}</span>
                      {isOpen && <span className='text-sm font-medium'>{item.title}</span>}
                    </Link>
                  )
                })}
              </div>
            </div>
          ))}
        </nav>

        {/* Divider */}
        <div className='border-t border-indigo-500'></div>

        {/* User Section & Exit Button */}
        <div className='p-4 space-y-3'>
          {isOpen && (
            <div className='bg-indigo-500 rounded-lg p-3'>
              <p className='text-xs text-indigo-100 uppercase font-semibold'>Usuario actual</p>
              <p className='text-white font-semibold truncate'>{user?.email}</p>
              <p className='text-xs text-indigo-100 capitalize'>{user?.role || 'Employee'}</p>
            </div>
          )}
          <button
            onClick={handleLogout}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg bg-red-500 text-white hover:bg-red-600 transition-colors font-medium ${
              !isOpen ? 'justify-center' : ''
            }`}
            title={!isOpen ? 'Cerrar sesión' : ''}
          >
            <span className='text-xl flex-shrink-0'>🚪</span>
            {isOpen && <span>Cerrar sesión</span>}
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
