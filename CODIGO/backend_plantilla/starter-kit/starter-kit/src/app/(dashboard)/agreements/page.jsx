'use client'

import { useState, useEffect } from 'react'
import api from '@/utils/api'

export default function AgreementsPage() {
  const [agreements, setAgreements] = useState([])
  const [companies, setCompanies] = useState([])
  const [restaurants, setRestaurants] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    company_id: '',
    restaurant_id: '',
    start_date: '',
    end_date: ''
  })
  const [error, setError] = useState('')

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [agRes, compRes, restRes] = await Promise.all([
        api.get('/api/agreements'),
        api.get('/api/companies'),
        api.get('/api/restaurants')
      ])
      setAgreements(agRes.data.data || [])
      setCompanies(compRes.data.data || [])
      setRestaurants(restRes.data.data || [])
      setError('')
    } catch (error) {
      console.error('Error loading data:', error)
      setError('Error al cargar datos')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      setError('')
      await api.post('/api/agreements', formData)
      setFormData({
        company_id: '',
        restaurant_id: '',
        start_date: '',
        end_date: ''
      })
      setShowForm(false)
      loadData()
    } catch (error) {
      console.error('Error creating agreement:', error)
      setError(error.response?.data?.message || 'Error creando acuerdo')
    }
  }

  if (loading) {
    return <div className='p-6'>Cargando acuerdos...</div>
  }

  return (
    <div className='p-6'>
      <div className='flex justify-between items-center mb-6'>
        <h1 className='text-3xl font-bold'>Acuerdos</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className='bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700'
        >
          {showForm ? 'Cancelar' : 'Nuevo Acuerdo'}
        </button>
      </div>

      {error && (
        <div className='bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4'>
          {error}
        </div>
      )}

      {showForm && (
        <div className='bg-white p-6 rounded-lg shadow-md mb-6'>
          <h2 className='text-xl font-semibold mb-4'>Crear Nuevo Acuerdo</h2>
          <form onSubmit={handleSubmit} className='space-y-4'>
            <div className='grid grid-cols-2 gap-4'>
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
              <div>
                <label className='block text-sm font-medium mb-1'>Restaurante</label>
                <select
                  value={formData.restaurant_id}
                  onChange={(e) => setFormData({...formData, restaurant_id: e.target.value})}
                  className='w-full p-2 border rounded-lg'
                  required
                >
                  <option value=''>Seleccionar restaurante</option>
                  {restaurants.map(r => (
                    <option key={r.id} value={r.id}>{r.name}</option>
                  ))}
                </select>
              </div>
            </div>
            <div className='grid grid-cols-2 gap-4'>
              <div>
                <label className='block text-sm font-medium mb-1'>Fecha Inicio</label>
                <input
                  type='date'
                  value={formData.start_date}
                  onChange={(e) => setFormData({...formData, start_date: e.target.value})}
                  className='w-full p-2 border rounded-lg'
                  required
                />
              </div>
              <div>
                <label className='block text-sm font-medium mb-1'>Fecha Fin</label>
                <input
                  type='date'
                  value={formData.end_date}
                  onChange={(e) => setFormData({...formData, end_date: e.target.value})}
                  className='w-full p-2 border rounded-lg'
                  required
                />
              </div>
            </div>
            <button
              type='submit'
              className='bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 w-full'
            >
              Crear Acuerdo
            </button>
          </form>
        </div>
      )}

      <div className='bg-white rounded-lg shadow-md'>
        <div className='p-6'>
          <h2 className='text-xl font-semibold mb-4'>Lista de Acuerdos</h2>
          {agreements.length === 0 ? (
            <p className='text-gray-500'>No hay acuerdos registrados</p>
          ) : (
            <div className='overflow-x-auto'>
              <table className='w-full'>
                <thead>
                  <tr className='border-b'>
                    <th className='text-left py-2 px-4'>ID</th>
                    <th className='text-left py-2 px-4'>Empresa</th>
                    <th className='text-left py-2 px-4'>Restaurante</th>
                    <th className='text-left py-2 px-4'>Inicio</th>
                    <th className='text-left py-2 px-4'>Fin</th>
                  </tr>
                </thead>
                <tbody>
                  {agreements.map(ag => {
                    const company = companies.find(c => c.id === ag.company_id)
                    const restaurant = restaurants.find(r => r.id === ag.restaurant_id)
                    return (
                      <tr key={ag.id} className='border-b hover:bg-gray-50'>
                        <td className='py-2 px-4'>{ag.id}</td>
                        <td className='py-2 px-4'>{company?.name || 'N/A'}</td>
                        <td className='py-2 px-4'>{restaurant?.name || 'N/A'}</td>
                        <td className='py-2 px-4'>{ag.start_date}</td>
                        <td className='py-2 px-4'>{ag.end_date}</td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
