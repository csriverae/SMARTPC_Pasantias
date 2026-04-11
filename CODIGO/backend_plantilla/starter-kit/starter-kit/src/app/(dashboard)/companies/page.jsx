'use client'

import { useState, useEffect } from 'react'
import api from '@/utils/api'

export default function CompaniesPage() {
  const [companies, setCompanies] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({ name: '', ruc: '' })

  useEffect(() => {
    loadCompanies()
  }, [])

  const loadCompanies = async () => {
    try {
      const response = await api.get('/api/companies')
      setCompanies(response.data.data || [])
    } catch (error) {
      console.error('Error loading companies:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.post('/api/companies', formData)
      setFormData({ name: '', ruc: '' })
      setShowForm(false)
      loadCompanies()
    } catch (error) {
      console.error('Error creating company:', error)
      alert('Error creando empresa')
    }
  }

  if (loading) {
    return <div className='p-6'>Cargando empresas...</div>
  }

  return (
    <div className='p-6'>
      <div className='flex justify-between items-center mb-6'>
        <h1 className='text-3xl font-bold'>Empresas</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className='bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700'
        >
          {showForm ? 'Cancelar' : 'Nueva Empresa'}
        </button>
      </div>

      {showForm && (
        <div className='bg-white p-6 rounded-lg shadow-md mb-6'>
          <h2 className='text-xl font-semibold mb-4'>Crear Nueva Empresa</h2>
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
              <label className='block text-sm font-medium mb-1'>RUC</label>
              <input
                type='text'
                value={formData.ruc}
                onChange={(e) => setFormData({...formData, ruc: e.target.value})}
                className='w-full p-2 border rounded-lg'
                required
              />
            </div>
            <button
              type='submit'
              className='bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700'
            >
              Crear Empresa
            </button>
          </form>
        </div>
      )}

      <div className='bg-white rounded-lg shadow-md'>
        <div className='p-6'>
          <h2 className='text-xl font-semibold mb-4'>Lista de Empresas</h2>
          {companies.length === 0 ? (
            <p className='text-gray-500'>No hay empresas registradas</p>
          ) : (
            <div className='space-y-4'>
              {companies.map(company => (
                <div key={company.id} className='border rounded-lg p-4'>
                  <h3 className='font-semibold'>{company.name}</h3>
                  <p className='text-sm text-gray-600'>RUC: {company.ruc || 'N/A'}</p>
                  <p className='text-sm text-gray-600'>ID: {company.id}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}