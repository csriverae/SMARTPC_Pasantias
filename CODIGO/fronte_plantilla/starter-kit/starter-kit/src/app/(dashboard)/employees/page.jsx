'use client'

import { useState, useEffect } from 'react'
import api from '@/utils/api'

export default function EmployeesPage() {
  const [employees, setEmployees] = useState([])
  const [companies, setCompanies] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({ name: '', email: '', company_id: '' })
  const [error, setError] = useState('')
  const [copiedToken, setCopiedToken] = useState(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [empRes, compRes] = await Promise.all([
        api.get('/api/employees'),
        api.get('/api/companies')
      ])
      setEmployees(empRes.data.data || [])
      setCompanies(compRes.data.data || [])
    } catch (error) {
      console.error('Error loading data:', error)
      setError('Error cargando datos')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      setError('')
      await api.post('/api/employees', formData)
      setFormData({ name: '', email: '', company_id: '' })
      setShowForm(false)
      loadData()
    } catch (error) {
      console.error('Error creating employee:', error)
      setError(error.response?.data?.message || 'Error creando empleado')
    }
  }

  const copyToClipboard = (token) => {
    navigator.clipboard.writeText(token)
    setCopiedToken(token)
    setTimeout(() => setCopiedToken(null), 2000)
  }

  if (loading) {
    return <div className='p-6'>Cargando empleados...</div>
  }

  return (
    <div className='p-6'>
      <div className='flex justify-between items-center mb-6'>
        <h1 className='text-3xl font-bold'>Empleados</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className='bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700'
        >
          {showForm ? 'Cancelar' : 'Nuevo Empleado'}
        </button>
      </div>

      {error && (
        <div className='bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4'>
          {error}
        </div>
      )}

      {showForm && (
        <div className='bg-white p-6 rounded-lg shadow-md mb-6'>
          <h2 className='text-xl font-semibold mb-4'>Crear Nuevo Empleado</h2>
          <form onSubmit={handleSubmit} className='space-y-4'>
            <div>
              <label className='block text-sm font-medium mb-1'>Nombre</label>
              <input
                type='text'
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                className='w-full p-2 border rounded-lg'
                required
              />
            </div>
            <div>
              <label className='block text-sm font-medium mb-1'>Email</label>
              <input
                type='email'
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                className='w-full p-2 border rounded-lg'
                required
              />
            </div>
            <div>
              <label className='block text-sm font-medium mb-1'>Empresa</label>
              <select
                value={formData.company_id}
                onChange={(e) => setFormData({...formData, company_id: e.target.value})}
                className='w-full p-2 border rounded-lg'
                required
              >
                <option value=''>Seleccionar empresa</option>
                {companies.map(c => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>
            <button
              type='submit'
              className='bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 w-full'
            >
              Crear Empleado
            </button>
          </form>
        </div>
      )}

      <div className='bg-white rounded-lg shadow-md'>
        <div className='p-6'>
          <h2 className='text-xl font-semibold mb-4'>Lista de Empleados</h2>
          {employees.length === 0 ? (
            <p className='text-gray-500'>No hay empleados registrados</p>
          ) : (
            <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
              {employees.map(employee => (
                <div key={employee.id} className='border-2 rounded-lg p-4 hover:shadow-lg transition-shadow'>
                  <h3 className='font-semibold text-lg'>{employee.name}</h3>
                  <p className='text-sm text-gray-600 mb-2'>Email: {employee.email}</p>
                  <p className='text-sm text-gray-600 mb-3'>Empresa: {companies.find(c => c.id === employee.company_id)?.name || 'N/A'}</p>
                  
                  <div className='bg-gray-50 rounded p-3 mb-3'>
                    <p className='text-xs font-medium text-gray-600 mb-1'>Token QR:</p>
                    <div className='flex items-center gap-2'>
                      <code className='text-xs font-mono font-bold text-blue-600 flex-1'>
                        {employee.qr_token}
                      </code>
                      <button
                        onClick={() => copyToClipboard(employee.qr_token)}
                        className='text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded hover:bg-indigo-200 transition-colors'
                      >
                        {copiedToken === employee.qr_token ? '✓ Copiado' : 'Copiar'}
                      </button>
                    </div>
                  </div>

                  <div className='text-xs text-gray-500 space-y-1'>
                    <p>ID: {employee.id}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}