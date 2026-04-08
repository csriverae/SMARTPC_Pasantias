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
  const [qrModal, setQrModal] = useState({ show: false, employee: null, imageUrl: null })
  const [deleteConfirm, setDeleteConfirm] = useState({ show: false, employee: null })

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

  const showQR = async (employee) => {
    try {
      const response = await api.get(`/api/employees/${employee.id}/qr`, { responseType: 'blob' })
      const imageUrl = URL.createObjectURL(response.data)
      setQrModal({ show: true, employee, imageUrl })
    } catch (error) {
      console.error('Error fetching QR:', error)
      setError('Error cargando QR')
    }
  }

  const closeQRModal = () => {
    if (qrModal.imageUrl) {
      URL.revokeObjectURL(qrModal.imageUrl)
    }
    setQrModal({ show: false, employee: null, imageUrl: null })
  }

  const confirmDelete = (employee) => {
    setDeleteConfirm({ show: true, employee })
  }

  const handleDelete = async () => {
    if (!deleteConfirm.employee) return

    try {
      setError('')
      await api.delete(`/api/employees/${deleteConfirm.employee.id}`)
      setDeleteConfirm({ show: false, employee: null })
      loadData()
    } catch (error) {
      console.error('Error deleting employee:', error)
      setError(error.response?.data?.message || 'Error eliminando empleado')
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
                      <button
                        onClick={() => showQR(employee)}
                        className='text-xs bg-green-100 text-green-700 px-2 py-1 rounded hover:bg-green-200 transition-colors'
                      >
                        Ver QR
                      </button>
                    </div>
                  </div>

                  <div className='text-xs text-gray-500 space-y-1'>
                    <p>ID: {employee.id}</p>
                    <div className='flex gap-2 mt-2'>
                      <button
                        onClick={() => confirmDelete(employee)}
                        className='text-xs bg-red-100 text-red-700 px-2 py-1 rounded hover:bg-red-200 transition-colors'
                      >
                        Eliminar
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* QR Modal */}
      {qrModal.show && (
        <div className='fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50'>
          <div className='bg-white p-6 rounded-lg shadow-lg max-w-md w-full mx-4'>
            <div className='flex justify-between items-center mb-4'>
              <h3 className='text-lg font-semibold'>QR de {qrModal.employee?.name}</h3>
              <button
                onClick={closeQRModal}
                className='text-gray-500 hover:text-gray-700 text-xl'
              >
                ×
              </button>
            </div>
            {qrModal.imageUrl && (
              <div className='flex justify-center'>
                <img src={qrModal.imageUrl} alt='QR Code' className='max-w-full h-auto' />
              </div>
            )}
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deleteConfirm.show && (
        <div className='fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50'>
          <div className='bg-white p-6 rounded-lg shadow-lg max-w-md w-full mx-4'>
            <div className='flex justify-between items-center mb-4'>
              <h3 className='text-lg font-semibold text-red-600'>Confirmar Eliminación</h3>
              <button
                onClick={() => setDeleteConfirm({ show: false, employee: null })}
                className='text-gray-500 hover:text-gray-700 text-xl'
              >
                ×
              </button>
            </div>
            <p className='text-gray-700 mb-4'>
              ¿Estás seguro de que quieres eliminar al empleado <strong>{deleteConfirm.employee?.name}</strong>?
              Esta acción no se puede deshacer.
            </p>
            <div className='flex gap-3'>
              <button
                onClick={() => setDeleteConfirm({ show: false, employee: null })}
                className='flex-1 bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300'
              >
                Cancelar
              </button>
              <button
                onClick={handleDelete}
                className='flex-1 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700'
              >
                Eliminar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}