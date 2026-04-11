'use client'

import { useState, useEffect } from 'react'
import api from '@/utils/api'
import { Button } from '@/components/ui/Button'
import { Card, CardHeader, CardBody, CardFooter } from '@/components/ui/Card'
import { TextField } from '@/components/ui/Form'
import { Alert } from '@/components/ui/Alert'
import { Modal, ConfirmDialog } from '@/components/ui/Modal'

export default function RestaurantsPage() {
  const [restaurants, setRestaurants] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [selectedRestaurant, setSelectedRestaurant] = useState(null)
  const [formData, setFormData] = useState({ name: '' })
  const [errors, setErrors] = useState({})
  const [message, setMessage] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    loadRestaurants()
  }, [])

  const loadRestaurants = async () => {
    try {
      setLoading(true)
      const response = await api.get('/api/restaurants')
      setRestaurants(response.data.data || [])
    } catch (error) {
      console.error('Error loading restaurants:', error)
      setMessage({ type: 'error', text: ' Error al cargar restaurantes' })
    } finally {
      setLoading(false)
    }
  }

  const validateForm = () => {
    const newErrors = {}
    if (!formData.name.trim()) newErrors.name = 'El nombre es requerido'
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!validateForm()) return

    try {
      setSubmitting(true)
      await api.post('/api/restaurants', formData)
      setMessage({ type: 'success', text: 'Restaurante creado exitosamente' })
      setFormData({ name: '' })
      setShowForm(false)
      loadRestaurants()
    } catch (error) {
      console.error('Error creating restaurant:', error)
      setMessage({
        type: 'error',
        text: error.response?.data?.message || 'Error creando restaurante'
      })
    } finally {
      setSubmitting(false)
    }
  }

  const confirmDelete = (restaurant) => {
    setSelectedRestaurant(restaurant)
    setShowDeleteDialog(true)
  }

  const handleDelete = async () => {
    if (!selectedRestaurant) return

    try {
      setSubmitting(true)
      await api.delete(`/api/restaurants/${selectedRestaurant.id}`)
      setMessage({ type: 'success', text: 'Restaurante eliminado exitosamente' })
     setShowDeleteDialog(false)
      loadRestaurants()
    } catch (error) {
      console.error('Error deleting restaurant:', error)
      setMessage({
        type: 'error',
        text: error.response?.data?.message || 'Error eliminando restaurante'
      })
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className='p-6 sm:p-8'>
      {/* Header */}
      <div className='flex justify-between items-center mb-8'>
        <div>
          <h1 className='text-3xl font-bold text-gray-900'>Restaurantes</h1>
          <p className='text-gray-600 mt-2'>Gestiona los restaurantes registrados en el sistema</p>
        </div>
        <Button
          variant='primary'
          onClick={() => {
            setShowForm(!showForm)
            setErrors({})
          }}
        >
          {showForm ? '✕ Cancelar' : '+ Nuevo Restaurante'}
        </Button>
      </div>

      {/* Messages */}
      {message && (
        <div className='mb-6'>
          <Alert
            type={message.type}
            message={message.text}
            onClose={() => setMessage(null)}
          />
        </div>
      )}

      {/* Form Modal */}
      <Modal
        isOpen={showForm}
        onClose={() => setShowForm(false)}
        title='Crear Nuevo Restaurante'
        size='md'
      >
        <form onSubmit={handleSubmit} className='space-y-4'>
          <TextField
            label='Nombre del Restaurante'
            name='name'
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            error={errors.name}
            required
            placeholder='Ej: El Buen Sabor'
          />
          <div className='flex gap-3 justify-end pt-4'>
            <Button
              variant='secondary'
              onClick={() => setShowForm(false)}
            >
              Cancelar
            </Button>
            <Button
              variant='primary'
              type='submit'
              loading={submitting}
            >
              Crear Restaurante
            </Button>
          </div>
        </form>
      </Modal>

      {/* Loading State */}
      {loading ? (
        <div className='text-center py-12'>
          <div className='inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4'></div>
          <p className='text-gray-600'>Cargando restaurantes...</p>
        </div>
      ) : restaurants.length === 0 ? (
        <Card>
          <CardBody className='text-center py-12'>
            <p className='text-gray-400 text-4xl mb-4'>🍽️</p>
            <p className='text-gray-600 mb-4'>No hay restaurantes registrados</p>
            <Button variant='primary' onClick={() => setShowForm(true)}>
              Crear primer restaurante
            </Button>
          </CardBody>
        </Card>
      ) : (
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
          {restaurants.map(restaurant => (
            <Card key={restaurant.id} className='hover:shadow-md transition-shadow flex flex-col'>
              <CardHeader className='border-b'>
                <h3 className='text-lg font-semibold text-gray-900'>{restaurant.name}</h3>
              </CardHeader>
              <CardBody className='flex-1'>
                <div className='space-y-3'>
                  <div>
                    <p className='text-xs text-gray-500 uppercase tracking-wide'>ID</p>
                    <p className='text-gray-900 font-mono text-sm'>{restaurant.id}</p>
                  </div>
                  <div>
                    <p className='text-xs text-gray-500 uppercase tracking-wide'>Estado</p>
                    <p className='text-green-600 font-medium'>Activo</p>
                  </div>
                </div>
              </CardBody>
              <CardFooter>
                <Button
                  variant='ghost'
                  size='sm'
                  onClick={() => confirmDelete(restaurant)}
                >
                  🗑️ Eliminar
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={showDeleteDialog}
        onClose={() => setShowDeleteDialog(false)}
        onConfirm={handleDelete}
        title='Eliminar Restaurante'
        message={`¿Estás seguro de que deseas eliminar "${selectedRestaurant?.name}"? Esta acción no se puede deshacer.`}
        loading={submitting}
      />
    </div>
  )
}

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
