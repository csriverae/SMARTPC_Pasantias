'use client'

import { useState, useEffect } from 'react'
import api from '@/utils/api'
import { Button, Badge } from '@/components/ui/Button'
import { Card, CardHeader, CardBody, CardFooter } from '@/components/ui/Card'
import { TextField, SelectField } from '@/components/ui/Form'
import { Alert } from '@/components/ui/Alert'
import { Modal, ConfirmDialog } from '@/components/ui/Modal'

export default function EmployeesPage() {
  const [employees, setEmployees] = useState([])
  const [companies, setCompanies] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [showQR, setShowQR] = useState({ show: false, employee: null, imageUrl: null })
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [selectedEmployee, setSelectedEmployee] = useState(null)
  const [copiedToken, setCopiedToken] = useState(null)
  const [formData, setFormData] = useState({ name: '', email: '', company_id: '' })
  const [errors, setErrors] = useState({})
  const [message, setMessage] = useState(null)
  const [submitting, setSubmitting] = useState(false)

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
      setMessage({ type: 'error', text: 'Error cargando datos' })
    } finally {
      setLoading(false)
    }
  }

  const validateForm = () => {
    const newErrors = {}
    if (!formData.name.trim()) newErrors.name = 'El nombre es requerido'
    if (!formData.email.trim()) newErrors.email = 'El email es requerido'
    if (!formData.company_id) newErrors.company_id = 'La empresa es requerida'
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!validateForm()) return

    try {
      setSubmitting(true)
      await api.post('/api/employees', {
        ...formData,
        company_id: parseInt(formData.company_id)
      })
      setMessage({ type: 'success', text: 'Empleado creado exitosamente' })
      setFormData({ name: '', email: '', company_id: '' })
      setShowForm(false)
      loadData()
    } catch (error) {
      console.error('Error creating employee:', error)
      setMessage({
        type: 'error',
        text: error.response?.data?.message || 'Error creando empleado'
      })
    } finally {
      setSubmitting(false)
    }
  }

  const handleShowQR = async (employee) => {
    try {
      const response = await api.get(`/api/employees/${employee.id}/qr`, { responseType: 'blob' })
      const imageUrl = URL.createObjectURL(response.data)
      setShowQR({ show: true, employee, imageUrl })
    } catch (error) {
      console.error('Error fetching QR:', error)
      setMessage({ type: 'error', text: 'Error cargando QR' })
    }
  }

  const handleCloseQR = () => {
    if (showQR.imageUrl) {
      URL.revokeObjectURL(showQR.imageUrl)
    }
    setShowQR({ show: false, employee: null, imageUrl: null })
  }

  const copyToClipboard = (token) => {
    navigator.clipboard.writeText(token)
    setCopiedToken(token)
    setTimeout(() => setCopiedToken(null), 2000)
  }

  const confirmDelete = (employee) => {
    setSelectedEmployee(employee)
    setShowDeleteDialog(true)
  }

  const handleDelete = async () => {
    if (!selectedEmployee) return

    try {
      setSubmitting(true)
      await api.delete(`/api/employees/${selectedEmployee.id}`)
      setMessage({ type: 'success', text: 'Empleado eliminado exitosamente' })
      setShowDeleteDialog(false)
      loadData()
    } catch (error) {
      console.error('Error deleting employee:', error)
      setMessage({
        type: 'error',
        text: error.response?.data?.message || 'Error eliminando empleado'
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
          <h1 className='text-3xl font-bold text-gray-900'>Empleados</h1>
          <p className='text-gray-600 mt-2'>Gestiona los empleados de las empresas registradas</p>
        </div>
        <Button
          variant='primary'
          onClick={() => {
            setShowForm(!showForm)
            setErrors({})
          }}
        >
          {showForm ? '✕ Cancelar' : '+ Nuevo Empleado'}
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
        title='Crear Nuevo Empleado'
        size='md'
      >
        <form onSubmit={handleSubmit} className='space-y-4'>
          <TextField
            label='Nombre Completo'
            name='name'
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            error={errors.name}
            required
            placeholder='Ej: Juan Pérez'
          />
          <TextField
            label='Email'
            name='email'
            type='email'
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            error={errors.email}
            required
            placeholder='juan@example.com'
          />
          <SelectField
            label='Empresa'
            name='company_id'
            value={formData.company_id}
            onChange={(e) => setFormData({...formData, company_id: e.target.value})}
            options={companies.map(c => ({ value: c.id, label: c.name }))}
            error={errors.company_id}
            required
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
              Crear Empleado
            </Button>
          </div>
        </form>
      </Modal>

      {/* Loading State */}
      {loading ? (
        <div className='text-center py-12'>
          <div className='inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4'></div>
          <p className='text-gray-600'>Cargando empleados...</p>
        </div>
      ) : employees.length === 0 ? (
        <Card>
          <CardBody className='text-center py-12'>
            <p className='text-gray-400 text-4xl mb-4'>👨‍💼</p>
            <p className='text-gray-600 mb-4'>No hay empleados registrados</p>
            <Button variant='primary' onClick={() => setShowForm(true)}>
              Crear primer empleado
            </Button>
          </CardBody>
        </Card>
      ) : (
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
          {employees.map(employee => (
            <Card key={employee.id} className='hover:shadow-md transition-shadow flex flex-col'>
              <CardHeader className='border-b'>
                <div className='flex items-start justify-between'>
                  <div className='flex-1'>
                    <h3 className='text-lg font-semibold text-gray-900'>{employee.name}</h3>
                    <p className='text-sm text-gray-500 mt-1'>{employee.email}</p>
                  </div>
                  <Badge variant='success' size='sm'>Activo</Badge>
                </div>
              </CardHeader>
              <CardBody className='flex-1 space-y-4'>
                <div>
                  <p className='text-xs text-gray-500 uppercase tracking-wide'>Empresa</p>
                  <p className='text-gray-900 font-medium'>{companies.find(c => c.id === employee.company_id)?.name || 'N/A'}</p>
                </div>
                <div>
                  <p className='text-xs text-gray-500 uppercase tracking-wide mb-2'>Token QR</p>
                  <div className='space-y-2'>
                    <div className='bg-gray-50 p-2 rounded border border-gray-200 break-all'>
                      <code className='text-xs font-mono text-blue-600'>{employee.qr_token}</code>
                    </div>
                    <div className='flex gap-2'>
                      <Button
                        variant='ghost'
                        size='sm'
                        fullWidth
                        onClick={() => copyToClipboard(employee.qr_token)}
                      >
                        {copiedToken === employee.qr_token ? '✓' : '📋'} Copiar
                      </Button>
                      <Button
                        variant='ghost'
                        size='sm'
                        fullWidth
                        onClick={() => handleShowQR(employee)}
                      >
                        📱 QR
                      </Button>
                    </div>
                  </div>
                </div>
              </CardBody>
              <CardFooter>
                <Button
                  variant='danger'
                  size='sm'
                  fullWidth
                  onClick={() => confirmDelete(employee)}
                >
                  🗑️ Eliminar
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}

      {/* QR Modal */}
      <Modal
        isOpen={showQR.show}
        onClose={handleCloseQR}
        title={`Código QR - ${showQR.employee?.name}`}
        size='sm'
      >
        {showQR.imageUrl && (
          <div className='text-center'>
            <img src={showQR.imageUrl} alt='QR Code' className='mx-auto mb-4' />
            <p className='text-sm text-gray-600 mb-4'>{showQR.employee?.qr_token}</p>
            <Button
              variant='primary'
              fullWidth
              onClick={() => copyToClipboard(showQR.employee?.qr_token)}
            >
              Copiar Token
            </Button>
          </div>
        )}
      </Modal>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={showDeleteDialog}
        onClose={() => setShowDeleteDialog(false)}
        onConfirm={handleDelete}
        title='Eliminar Empleado'
        message={`¿Estás seguro de que deseas eliminar a "${selectedEmployee?.name}"? Esta acción no se puede deshacer.`}
        loading={submitting}
      />
    </div>
  )
}