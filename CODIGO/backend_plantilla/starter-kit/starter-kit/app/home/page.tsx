'use client'

import { useEffect, useState } from 'react'
import axios from 'axios'
import StatsCard from '@/components/dashboard/StatsCard'
import UsersList from '@/components/dashboard/UsersList'
import CompaniesList from '@/components/dashboard/CompaniesList'
import EmployeesList from '@/components/dashboard/EmployeesList'
import RestaurantsList from '@/components/dashboard/RestaurantsList'

interface Stats {
  users: number
  companies: number
  employees: number
  restaurants: number
}

interface User {
  user_id: string
  email: string
  full_name: string
  role: string
}

interface Company {
  id: string
  name: string
  ruc: string
}

interface Employee {
  id: string
  full_name: string
  email: string
  phone: string
  qr_token: string
}

interface Restaurant {
  id: string
  name: string
}

const API_BASE_URL = 'http://localhost:8000'

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats>({
    users: 0,
    companies: 0,
    employees: 0,
    restaurants: 0
  })
  const [users, setUsers] = useState<User[]>([])
  const [companies, setCompanies] = useState<Company[]>([])
  const [employees, setEmployees] = useState<Employee[]>([])
  const [restaurants, setRestaurants] = useState<Restaurant[]>([])
  const [currentUser, setCurrentUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')
  const [error, setError] = useState<string | null>(null)
  const [showModal, setShowModal] = useState(false)
  const [modalType, setModalType] = useState('')

  const getHeaders = () => {
    const token = localStorage.getItem('token')
    const tenantId = localStorage.getItem('tenant_id')
    return {
      Authorization: `Bearer ${token}`,
      'X-Tenant-ID': tenantId,
      'Content-Type': 'application/json'
    }
  }

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      setError(null)

      const config = { headers: getHeaders() }

      // Cargar usuario actual
      const meRes = await axios.get(`${API_BASE_URL}/auth/me`, config)
      const userData = meRes.data?.data?.data || meRes.data?.data || meRes.data
      setCurrentUser(userData)

      // Cargar usuarios
      const usersRes = await axios.get(`${API_BASE_URL}/api/users`, config)
      const usersData = usersRes.data?.data?.data || usersRes.data?.data || []
      setUsers(Array.isArray(usersData) ? usersData : [])

      // Cargar empresas
      const companiesRes = await axios.get(`${API_BASE_URL}/api/companies`, config)
      const companiesData = companiesRes.data?.data?.data || companiesRes.data?.data || []
      setCompanies(Array.isArray(companiesData) ? companiesData : [])

      // Cargar empleados
      const employeesRes = await axios.get(`${API_BASE_URL}/api/employees`, config)
      const employeesData = employeesRes.data?.data?.data || employeesRes.data?.data || []
      setEmployees(Array.isArray(employeesData) ? employeesData : [])

      // Cargar restaurantes
      const restaurantsRes = await axios.get(`${API_BASE_URL}/api/restaurants`, config)
      const restaurantsData = restaurantsRes.data?.data?.data || restaurantsRes.data?.data || []
      setRestaurants(Array.isArray(restaurantsData) ? restaurantsData : [])

      // Actualizar estadísticas
      setStats({
        users: usersData.length || 0,
        companies: companiesData.length || 0,
        employees: employeesData.length || 0,
        restaurants: restaurantsData.length || 0
      })
    } catch (err: any) {
      console.error('Error cargando datos:', err)
      setError(err?.response?.data?.data?.detail || 'Error al cargar datos')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadDashboardData()
  }, [])

  const handleCreateUser = async (email: string, role: string) => {
    try {
      const res = await axios.post(
        `${API_BASE_URL}/api/users/invite`,
        { email, role },
        { headers: getHeaders() }
      )
      const invitation = res.data?.data?.data || res.data?.data
      alert(`Usuario invitado. Contraseña temporal: ${invitation.generated_password}`)
      loadDashboardData()
      setShowModal(false)
    } catch (err: any) {
      setError(err?.response?.data?.data?.detail || 'Error al invitar usuario')
    }
  }

  const handleCreateCompany = async (name: string, ruc: string) => {
    try {
      await axios.post(
        `${API_BASE_URL}/api/companies`,
        { name, ruc },
        { headers: getHeaders() }
      )
      loadDashboardData()
      setShowModal(false)
      alert('Empresa creada exitosamente')
    } catch (err: any) {
      setError(err?.response?.data?.data?.detail || 'Error al crear empresa')
    }
  }

  const handleCreateRestaurant = async (name: string) => {
    try {
      await axios.post(
        `${API_BASE_URL}/api/restaurants`,
        { name },
        { headers: getHeaders() }
      )
      loadDashboardData()
      setShowModal(false)
      alert('Restaurante creado exitosamente')
    } catch (err: any) {
      setError(err?.response?.data?.data?.detail || 'Error al crear restaurante')
    }
  }

  const handleCreateEmployee = async (name: string, email: string, company_id: string) => {
    try {
      await axios.post(
        `${API_BASE_URL}/api/employees`,
        { name, email, company_id: parseInt(company_id) },
        { headers: getHeaders() }
      )
      loadDashboardData()
      setShowModal(false)
      alert('Empleado creado exitosamente')
    } catch (err: any) {
      setError(err?.response?.data?.data?.detail || 'Error al crear empleado')
    }
  }

  if (loading) {
    return (
      <div className='flex items-center justify-center min-h-screen'>
        <div className='text-center'>
          <div className='animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4'></div>
          <p className='text-slate-600'>Cargando dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className='py-6 px-6 sm:px-8'>
      <div className='flex items-center justify-between mb-8'>
        <div>
          <h1 className='text-3xl font-bold tracking-tight text-slate-900'>Dashboard MesaPass</h1>
          <p className='text-sm text-slate-500 mt-1'>Hola, {currentUser?.full_name || 'Usuario'}</p>
        </div>
      </div>

      {error && (
        <div className='mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800'>
          {error}
        </div>
      )}

      {/* Stats Cards */}
      <div className='grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-8'>
        <StatsCard
          label='Usuarios'
          value={stats.users}
          icon='tabler-users'
          bgColor='bg-indigo-100'
          textColor='text-indigo-600'
          tab='users'
          onTabChange={setActiveTab}
        />
        <StatsCard
          label='Empresas'
          value={stats.companies}
          icon='tabler-building'
          bgColor='bg-blue-100'
          textColor='text-blue-600'
          tab='companies'
          onTabChange={setActiveTab}
        />
        <StatsCard
          label='Empleados'
          value={stats.employees}
          icon='tabler-users-group'
          bgColor='bg-green-100'
          textColor='text-green-600'
          tab='employees'
          onTabChange={setActiveTab}
        />
        <StatsCard
          label='Restaurantes'
          value={stats.restaurants}
          icon='tabler-utensils'
          bgColor='bg-orange-100'
          textColor='text-orange-600'
          tab='restaurants'
          onTabChange={setActiveTab}
        />
      </div>

      {/* Tabs Navigation */}
      <div className='flex gap-2 mb-6 border-b border-slate-200'>
        {[
          { id: 'overview', label: 'Resumen' },
          { id: 'users', label: 'Usuarios' },
          { id: 'companies', label: 'Empresas' },
          { id: 'employees', label: 'Empleados' },
          { id: 'restaurants', label: 'Restaurantes' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 font-medium text-sm transition-colors ${
              activeTab === tab.id
                ? 'text-indigo-600 border-b-2 border-indigo-600'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Contents */}
      <div className='space-y-4'>
        {activeTab === 'users' && (
          <UsersList
            users={users}
            onInviteClick={() => {
              setModalType('user')
              setShowModal(true)
            }}
          />
        )}

        {activeTab === 'companies' && (
          <CompaniesList
            companies={companies}
            onCreateClick={() => {
              setModalType('company')
              setShowModal(true)
            }}
          />
        )}

        {activeTab === 'employees' && (
          <EmployeesList
            employees={employees}
            onCreateClick={() => {
              setModalType('employee')
              setShowModal(true)
            }}
          />
        )}

        {activeTab === 'restaurants' && (
          <RestaurantsList
            restaurants={restaurants}
            onCreateClick={() => {
              setModalType('restaurant')
              setShowModal(true)
            }}
          />
        )}

        {activeTab === 'overview' && (
          <div className='grid gap-4 lg:grid-cols-2'>
            <div className='bg-white border border-slate-200 rounded-xl p-6'>
              <h2 className='text-lg font-semibold text-slate-900 mb-4'>Información General</h2>
              <div className='space-y-3'>
                <p className='text-slate-600'>
                  <span className='font-medium'>Tenant:</span> {currentUser?.tenant_name || 'N/A'}
                </p>
                <p className='text-slate-600'>
                  <span className='font-medium'>Rol:</span> <span className='capitalize'>{currentUser?.role || 'N/A'}</span>
                </p>
                <p className='text-slate-600'>
                  <span className='font-medium'>Email:</span> {currentUser?.email || 'N/A'}
                </p>
              </div>
            </div>
            <div className='bg-white border border-slate-200 rounded-xl p-6'>
              <h2 className='text-lg font-semibold text-slate-900 mb-4'>Acciones Rápidas</h2>
              <div className='space-y-2'>
                <button
                  onClick={() => {
                    setModalType('user')
                    setShowModal(true)
                  }}
                  className='w-full p-3 border border-slate-200 rounded-lg hover:bg-slate-50 text-left text-slate-900 font-medium transition-colors'
                >
                  + Invitar Usuario
                </button>
                <button
                  onClick={() => {
                    setModalType('company')
                    setShowModal(true)
                  }}
                  className='w-full p-3 border border-slate-200 rounded-lg hover:bg-slate-50 text-left text-slate-900 font-medium transition-colors'
                >
                  + Crear Empresa
                </button>
                <button
                  onClick={() => {
                    setModalType('restaurant')
                    setShowModal(true)
                  }}
                  className='w-full p-3 border border-slate-200 rounded-lg hover:bg-slate-50 text-left text-slate-900 font-medium transition-colors'
                >
                  + Crear Restaurante
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Modal for creating users/companies/restaurants */}
      {showModal && (
        <div className='fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50'>
          <div className='bg-white rounded-lg shadow-lg p-6 max-w-md w-full mx-4'>
            <div className='flex justify-between items-center mb-4'>
              <h3 className='text-lg font-semibold'>
                {modalType === 'user' && 'Invitar Usuario'}
                {modalType === 'company' && 'Crear Empresa'}
                {modalType === 'restaurant' && 'Crear Restaurante'}
                {modalType === 'employee' && 'Crear Empleado'}
              </h3>
              <button
                onClick={() => setShowModal(false)}
                className='text-gray-500 hover:text-gray-700 text-2xl leading-none'
              >
                ×
              </button>
            </div>

            {modalType === 'user' && (
              <UserForm onSubmit={handleCreateUser} onClose={() => setShowModal(false)} />
            )}
            {modalType === 'company' && (
              <CompanyForm onSubmit={handleCreateCompany} onClose={() => setShowModal(false)} />
            )}
            {modalType === 'restaurant' && (
              <RestaurantForm onSubmit={handleCreateRestaurant} onClose={() => setShowModal(false)} />
            )}
            {modalType === 'employee' && (
              <EmployeeForm companies={companies} onSubmit={handleCreateEmployee} onClose={() => setShowModal(false)} />
            )}
          </div>
        </div>
      )}
    </div>
  )
}

// Form Components
function UserForm({ onSubmit, onClose }: any) {
  const [email, setEmail] = useState('')
  const [role, setRole] = useState('employee')
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (email) {
      setSubmitting(true)
      await onSubmit(email, role)
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className='space-y-4'>
      <div>
        <label className='block text-sm font-medium text-slate-700 mb-1'>Email</label>
        <input
          type='email'
          placeholder='usuario@empresa.com'
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className='w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:border-indigo-500'
          required
        />
      </div>
      <div>
        <label className='block text-sm font-medium text-slate-700 mb-1'>Rol</label>
        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className='w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:border-indigo-500'
        >
          <option value='employee'>Employee</option>
          <option value='company_admin'>Company Admin</option>
          <option value='admin'>Admin</option>
        </select>
      </div>
      <div className='flex gap-2 pt-4'>
        <button
          type='submit'
          disabled={submitting}
          className='flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 font-medium transition-colors'
        >
          {submitting ? 'Invitando...' : 'Invitar'}
        </button>
        <button
          type='button'
          onClick={onClose}
          className='flex-1 px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 font-medium transition-colors'
        >
          Cancelar
        </button>
      </div>
    </form>
  )
}

function CompanyForm({ onSubmit, onClose }: any) {
  const [name, setName] = useState('')
  const [ruc, setRuc] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (name && ruc) {
      setSubmitting(true)
      await onSubmit(name, ruc)
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className='space-y-4'>
      <div>
        <label className='block text-sm font-medium text-slate-700 mb-1'>Nombre Empresa</label>
        <input
          type='text'
          placeholder='Ej: Mi Empresa S.A.'
          value={name}
          onChange={(e) => setName(e.target.value)}
          className='w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:border-indigo-500'
          required
        />
      </div>
      <div>
        <label className='block text-sm font-medium text-slate-700 mb-1'>RUC (13 dígitos)</label>
        <input
          type='text'
          placeholder='1234567890123'
          value={ruc}
          onChange={(e) => setRuc(e.target.value.replace(/\D/g, ''))}
          className='w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:border-indigo-500'
          required
          maxLength={13}
        />
      </div>
      <div className='flex gap-2 pt-4'>
        <button
          type='submit'
          disabled={submitting}
          className='flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 font-medium transition-colors'
        >
          {submitting ? 'Creando...' : 'Crear'}
        </button>
        <button
          type='button'
          onClick={onClose}
          className='flex-1 px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 font-medium transition-colors'
        >
          Cancelar
        </button>
      </div>
    </form>
  )
}

function RestaurantForm({ onSubmit, onClose }: any) {
  const [name, setName] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (name) {
      setSubmitting(true)
      await onSubmit(name)
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className='space-y-4'>
      <div>
        <label className='block text-sm font-medium text-slate-700 mb-1'>Nombre Restaurante</label>
        <input
          type='text'
          placeholder='Ej: Restaurante La Abuela'
          value={name}
          onChange={(e) => setName(e.target.value)}
          className='w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:border-indigo-500'
          required
        />
      </div>
      <div className='flex gap-2 pt-4'>
        <button
          type='submit'
          disabled={submitting}
          className='flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 font-medium transition-colors'
        >
          {submitting ? 'Creando...' : 'Crear'}
        </button>
        <button
          type='button'
          onClick={onClose}
          className='flex-1 px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 font-medium transition-colors'
        >
          Cancelar
        </button>
      </div>
    </form>
  )
}

function EmployeeForm({ companies, onSubmit, onClose }: any) {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [companyId, setCompanyId] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (name && email && companyId) {
      setSubmitting(true)
      await onSubmit(name, email, companyId)
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className='space-y-4'>
      <div>
        <label className='block text-sm font-medium text-slate-700 mb-1'>Nombre Completo</label>
        <input
          type='text'
          placeholder='Ej: Juan Pérez'
          value={name}
          onChange={(e) => setName(e.target.value)}
          className='w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:border-indigo-500'
          required
        />
      </div>
      <div>
        <label className='block text-sm font-medium text-slate-700 mb-1'>Email</label>
        <input
          type='email'
          placeholder='juan@empresa.com'
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className='w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:border-indigo-500'
          required
        />
      </div>
      <div>
        <label className='block text-sm font-medium text-slate-700 mb-1'>Empresa</label>
        <select
          value={companyId}
          onChange={(e) => setCompanyId(e.target.value)}
          className='w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:border-indigo-500'
          required
        >
          <option value=''>Selecciona una empresa</option>
          {companies.map((company: any) => (
            <option key={company.id} value={company.id}>
              {company.name}
            </option>
          ))}
        </select>
      </div>
      <div className='flex gap-2 pt-4'>
        <button
          type='submit'
          disabled={submitting}
          className='flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 font-medium transition-colors'
        >
          {submitting ? 'Creando...' : 'Crear'}
        </button>
        <button
          type='button'
          onClick={onClose}
          className='flex-1 px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 font-medium transition-colors'
        >
          Cancelar
        </button>
      </div>
    </form>
  )
}
