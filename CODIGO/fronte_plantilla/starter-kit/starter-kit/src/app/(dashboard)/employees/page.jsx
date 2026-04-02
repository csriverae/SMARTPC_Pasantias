'use client'

import { useState, useEffect } from 'react'
import api from '@/utils/api'

export default function EmployeesPage() {
  const [employees, setEmployees] = useState([])
  const [companies, setCompanies] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({ name: '', email: '', cedula: '' })

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
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.post('/api/employees', formData)
      setFormData({ name: '', email: '', cedula: '' })
      setShowForm(false)
      loadData()
    } catch (error) {
      console.error('Error creating employee:', error)
      alert('Error creando empleado')
    }
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
              <label className='block text-sm font-medium mb-1'>Cédula</label>
              <input
                type='text'
                value={formData.cedula}
                onChange={(e) => setFormData({...formData, cedula: e.target.value})}
                className='w-full p-2 border rounded-lg'
                required
              />
            </div>
            <button
              type='submit'
              className='bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700'
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
            <div className='space-y-4'>
              {employees.map(employee => (
                <div key={employee.id} className='border rounded-lg p-4'>
                  <h3 className='font-semibold'>{employee.name}</h3>
                  <p className='text-sm text-gray-600'>Email: {employee.email}</p>
                  <p className='text-sm text-gray-600'>Cédula: {employee.cedula || 'N/A'}</p>
                  <p className='text-sm text-gray-600'>ID: {employee.id}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}