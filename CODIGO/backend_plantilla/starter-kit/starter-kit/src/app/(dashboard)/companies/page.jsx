'use client'

import { useState, useEffect } from 'react'
import api from '@/utils/api'
import { Button } from '@/components/ui/Button'
import { Card, CardHeader, CardBody, CardFooter } from '@/components/ui/Card'
import { TextField } from '@/components/ui/Form'
import { Alert } from '@/components/ui/Alert'
import { Modal, ConfirmDialog } from '@/components/ui/Modal'

export default function CompaniesPage() {
  const [companies, setCompanies] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [selectedCompany, setSelectedCompany] = useState(null)
  const [formData, setFormData] = useState({ name: '', ruc: '' })
  const [errors, setErrors] = useState({})
  const [message, setMessage] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    loadCompanies()
  }, [])

  const loadCompanies = async () => {
    try {
      setLoading(true)
      const response = await api.get('/api/companies')
      setCompanies(response.data.data || [])
    } catch (error) {
      console.error('Error loading companies:', error)
      setMessage({ type: 'error', text: 'Error al cargar empresas' })
    } finally {
      setLoading(false)
    }
  }

  const validateForm = () => {
    const newErrors = {}
    if (!formData.name.trim()) newErrors.name = 'El nombre es requerido'
    if (!formData.ruc.trim()) newErrors.ruc = 'El RUC es requerido'
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!validateForm()) return

    try {
      setSubmitting(true)
      await api.post('/api/companies', formData)
      setMessage({ type: 'success', text: 'Empresa creada exitosamente' })
      setFormData({ name: '', ruc: '' })
      setShowForm(false)
      loadCompanies()
    } catch (error) {
      console.error('Error creating company:', error)
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.message || 'Error creando empresa' 
      })
    } finally {
      setSubmitting(false)
    }
  }

  const confirmDelete = (company) => {
    setSelectedCompany(company)
    setShowDeleteDialog(true)
  }

  const handleDelete = async () => {
    if (!selectedCompany) return

    try {
      setSubmitting(true)
      await api.delete(`/api/companies/${selectedCompany.id}`)
      setMessage({ type: 'success', text: 'Empresa eliminada exitosamente' })
      setShowDeleteDialog(false)
      loadCompanies()
    } catch (error) {
      console.error('Error deleting company:', error)
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.message || 'Error eliminando empresa' 
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
          <h1 className='text-3xl font-bold text-gray-900'>Empresas</h1>
          <p className='text-gray-600 mt-2'>Gestiona las empresas registradas en el sistema</p>
        </div>
        <Button
          variant='primary'
          onClick={() => {
            setShowForm(!showForm)
            setErrors({})
          }}
        >
          {showForm ? '✕ Cancelar' : '+ Nueva Empresa'}
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
        title='Crear Nueva Empresa'
        size='md'
      >
        <form onSubmit={handleSubmit} className='space-y-4'>
          <TextField
            label='Nombre de la Empresa'
            name='name'
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            error={errors.name}
            required
            placeholder='Ej: TechCorp Solutions'
          />
          <TextField
            label='RUC'
            name='ruc'
            value={formData.ruc}
            onChange={(e) => setFormData({...formData, ruc: e.target.value})}
            error={errors.ruc}
            required
            placeholder='Ej: 1234567890'
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
              Crear Empresa
            </Button>
          </div>
        </form>
      </Modal>

      {/* Loading State */}
      {loading ? (
        <div className='text-center py-12'>
          <div className='inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4'></div>
          <p className='text-gray-600'>Cargando empresas...</p>
        </div>
      ) : companies.length === 0 ? (
        <Card>
          <CardBody className='text-center py-12'>
            <p className='text-gray-400 text-4xl mb-4'>🏢</p>
            <p className='text-gray-600 mb-4'>No hay empresas registradas</p>
            <Button variant='primary' onClick={() => setShowForm(true)}>
              Crear primera empresa
            </Button>
          </CardBody>
        </Card>
      ) : (
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
          {companies.map(company => (
            <Card key={company.id} className='hover:shadow-md transition-shadow flex flex-col'>
              <CardHeader className='border-b'>
                <h3 className='text-lg font-semibold text-gray-900'>{company.name}</h3>
              </CardHeader>
              <CardBody className='flex-1'>
                <div className='space-y-3'>
                  <div>
                    <p className='text-xs text-gray-500 uppercase tracking-wide'>RUC</p>
                    <p className='text-gray-900 font-medium'>{company.ruc || 'N/A'}</p>
                  </div>
                  <div>
                    <p className='text-xs text-gray-500 uppercase tracking-wide'>ID</p>
                    <p className='text-gray-900 font-mono text-sm'>{company.id}</p>
                  </div>
                </div>
              </CardBody>
              <CardFooter>
                <Button
                  variant='ghost'
                  size='sm'
                  onClick={() => confirmDelete(company)}
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
        title='Eliminar Empresa'
        message={`¿Estás seguro de que deseas eliminar "${selectedCompany?.name}"? Esta acción no se puede deshacer.`}
        loading={submitting}
      />
    </div>
  )
}

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