'use client'

import { useState, useEffect } from 'react'
import api from '@/utils/api'
import { Button } from '@/components/ui/Button'
import { Card, CardHeader, CardBody } from '@/components/ui/Card'
import { TextField, SelectField } from '@/components/ui/Form'
import { Alert } from '@/components/ui/Alert'
import { Modal, ConfirmDialog } from '@/components/ui/Modal'
import DataTable from '@/components/ui/DataTable'

export default function AgreementsPage() {
  const [agreements, setAgreements] = useState([])
  const [companies, setCompanies] = useState([])
  const [restaurants, setRestaurants] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [selectedAgreement, setSelectedAgreement] = useState(null)
  const [formData, setFormData] = useState({
    company_id: '',
    restaurant_id: '',
    start_date: '',
    end_date: ''
  })
  const [errors, setErrors] = useState({})
  const [message, setMessage] = useState(null)
  const [submitting, setSubmitting] = useState(false)

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
      setMessage(null)
    } catch (error) {
      console.error('Error loading data:', error)
      setMessage({ type: 'error', text: 'Error al cargar datos' })
    } finally {
      setLoading(false)
    }
  }

  const validateForm = () => {
    const newErrors = {}
    if (!formData.company_id) newErrors.company_id = 'La empresa es requerida'
    if (!formData.restaurant_id) newErrors.restaurant_id = 'El restaurante es requerido'
    if (!formData.start_date) newErrors.start_date = 'La fecha de inicio es requerida'
    if (!formData.end_date) newErrors.end_date = 'La fecha de fin es requerida'
    if (formData.start_date && formData.end_date && formData.start_date > formData.end_date) {
      newErrors.end_date = 'La fecha de fin debe ser posterior a la de inicio'
    }
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!validateForm()) return

    try {
      setSubmitting(true)
      await api.post('/api/agreements', {
        company_id: parseInt(formData.company_id),
        restaurant_id: parseInt(formData.restaurant_id),
        start_date: formData.start_date,
        end_date: formData.end_date
      })
      setMessage({ type: 'success', text: 'Acuerdo creado exitosamente' })
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
      setMessage({
        type: 'error',
        text: error.response?.data?.message || 'Error creando acuerdo'
      })
    } finally {
      setSubmitting(false)
    }
  }

  const confirmDelete = (agreement) => {
    setSelectedAgreement(agreement)
    setShowDeleteDialog(true)
  }

  const handleDelete = async () => {
    if (!selectedAgreement) return

    try {
      setSubmitting(true)
      await api.delete(`/api/agreements/${selectedAgreement.id}`)
      setMessage({ type: 'success', text: 'Acuerdo eliminado exitosamente' })
      setShowDeleteDialog(false)
      loadData()
    } catch (error) {
      console.error('Error deleting agreement:', error)
      setMessage({
        type: 'error',
        text: error.response?.data?.message || 'Error eliminando acuerdo'
      })
    } finally {
      setSubmitting(false)
    }
  }

  const columns = [
    { key: 'id', label: 'ID' },
    {
      key: 'company_id',
      label: 'Empresa',
      render: (id) => companies.find(c => c.id === id)?.name || 'N/A'
    },
    {
      key: 'restaurant_id',
      label: 'Restaurante',
      render: (id) => restaurants.find(r => r.id === id)?.name || 'N/A'
    },
    { key: 'start_date', label: 'Inicio' },
    { key: 'end_date', label: 'Fin' }
  ]

  return (
    <div className='p-6 sm:p-8'>
      {/* Header */}
      <div className='flex justify-between items-center mb-8'>
        <div>
          <h1 className='text-3xl font-bold text-gray-900'>Acuerdos</h1>
          <p className='text-gray-600 mt-2'>Gestiona los acuerdos entre empresas y restaurantes</p>
        </div>
        <Button
          variant='primary'
          onClick={() => {
            setShowForm(!showForm)
            setErrors({})
          }}
        >
          {showForm ? '✕ Cancelar' : '+ Nuevo Acuerdo'}
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
        title='Crear Nuevo Acuerdo'
        size='lg'
      >
        <form onSubmit={handleSubmit} className='space-y-4'>
          <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
            <SelectField
              label='Empresa'
              name='company_id'
              value={formData.company_id}
              onChange={(e) => setFormData({...formData, company_id: e.target.value})}
              options={companies.map(c => ({ value: c.id, label: c.name }))}
              error={errors.company_id}
              required
            />
            <SelectField
              label='Restaurante'
              name='restaurant_id'
              value={formData.restaurant_id}
              onChange={(e) => setFormData({...formData, restaurant_id: e.target.value})}
              options={restaurants.map(r => ({ value: r.id, label: r.name }))}
              error={errors.restaurant_id}
              required
            />
          </div>
          <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
            <TextField
              label='Fecha de Inicio'
              name='start_date'
              type='date'
              value={formData.start_date}
              onChange={(e) => setFormData({...formData, start_date: e.target.value})}
              error={errors.start_date}
              required
            />
            <TextField
              label='Fecha de Fin'
              name='end_date'
              type='date'
              value={formData.end_date}
              onChange={(e) => setFormData({...formData, end_date: e.target.value})}
              error={errors.end_date}
              required
            />
          </div>
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
              Crear Acuerdo
            </Button>
          </div>
        </form>
      </Modal>

      {/* Table */}
      <Card>
        <CardHeader>
          <h2 className='text-lg font-semibold text-gray-900'>Lista de Acuerdos</h2>
        </CardHeader>
        <CardBody>
          <DataTable
            columns={columns}
            data={agreements}
            loading={loading}
            error={null}
            onDelete={confirmDelete}
            emptyMessage='No hay acuerdos registrados'
          />
        </CardBody>
      </Card>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={showDeleteDialog}
        onClose={() => setShowDeleteDialog(false)}
        onConfirm={handleDelete}
        title='Eliminar Acuerdo'
        message={`¿Estás seguro de que deseas eliminar este acuerdo? Esta acción no se puede deshacer.`}
        loading={submitting}
      />
    </div>
  )
}
