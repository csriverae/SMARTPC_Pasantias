'use client'

import { useState, useEffect } from 'react'
import api from '@/utils/api'

export default function RestaurantsPage() {
  const [restaurants, setRestaurants] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({ name: '' })
  const [error, setError] = useState('')

  useEffect(() => {
    loadRestaurants()
  }, [])

  const loadRestaurants = async () => {
    try {
      setLoading(true)
      const response = await api.get('/api/restaurants')
      setRestaurants(response.data.data || [])
      setError('')
    } catch (error) {
      console.error('Error loading restaurants:', error)
      setError('Error al cargar restaurantes')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      setError('')
      await api.post('/api/restaurants', formData)
      setFormData({ name: '' })
      setShowForm(false)
      loadRestaurants()
    } catch (error) {
      console.error('Error creating restaurant:', error)
      setError(error.response?.data?.message || 'Error creando restaurante')
    }
  }

  if (loading) {
    return <div className='p-6'>Cargando restaurantes...</div>
  }

  return (
    <div className='p-6'>
      <div className='flex justify-between items-center mb-6'>
        <h1 className='text-3xl font-bold'>Restaurantes</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className='bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700'
        >
          {showForm ? 'Cancelar' : 'Nuevo Restaurante'}
        </button>
      </div>

      {error && (
        <div className='bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4'>
          {error}
        </div>
      )}

      {showForm && (
        <div className='bg-white p-6 rounded-lg shadow-md mb-6'>
          <h2 className='text-xl font-semibold mb-4'>Crear Nuevo Restaurante</h2>
          <form onSubmit={handleSubmit} className='space-y-4'>
            <div>
              <label className='block text-sm font-medium mb-1'>Nombre del Restaurante</label>
              <input
                type='text'
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                className='w-full p-2 border rounded-lg'
                required
              />
            </div>
            <button
              type='submit'
              className='bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700'
            >
              Crear Restaurante
            </button>
          </form>
        </div>
      )}

      <div className='bg-white rounded-lg shadow-md'>
        <div className='p-6'>
          <h2 className='text-xl font-semibold mb-4'>Lista de Restaurantes</h2>
          {restaurants.length === 0 ? (
            <p className='text-gray-500'>No hay restaurantes registrados</p>
          ) : (
            <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
              {restaurants.map(restaurant => (
                <div key={restaurant.id} className='border rounded-lg p-4 hover:shadow-lg transition-shadow'>
                  <h3 className='font-semibold text-lg'>{restaurant.name}</h3>
                  <p className='text-sm text-gray-600'>ID: {restaurant.id}</p>
                  <p className='text-sm text-gray-600'>Usuario: {restaurant.user_id}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
