'use client'

import { useState, useEffect } from 'react'
import api from '@/utils/api'

export default function UsersPage() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({ email: '', role: 'employee' })
  const [error, setError] = useState('')
  const [successMessage, setSuccessMessage] = useState('')
  const [deleteConfirm, setDeleteConfirm] = useState({ show: false, user: null })

  useEffect(() => {
    loadUsers()
  }, [])

  const loadUsers = async () => {
    try {
      setLoading(true)
      setError('')
      const response = await api.get('/api/users')
      setUsers(response.data.data || [])
    } catch (error) {
      console.error('Error loading users:', error)
      setError(error.response?.data?.message || 'Error cargando usuarios')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      setError('')
      setSuccessMessage('')

      await api.post('/api/users/invite', formData)
      setFormData({ email: '', role: 'employee' })
      setShowForm(false)
      setSuccessMessage('Invitación enviada correctamente')
      loadUsers()
    } catch (error) {
      console.error('Error inviting user:', error)
      setError(error.response?.data?.message || 'Error enviando invitación')
    }
  }

  const confirmDelete = (user) => {
    setDeleteConfirm({ show: true, user })
  }

  const handleDelete = async () => {
    if (!deleteConfirm.user) return

    try {
      setError('')
      setSuccessMessage('')
      await api.delete(`/api/users/${deleteConfirm.user.id}`)
      setDeleteConfirm({ show: false, user: null })
      setSuccessMessage('Usuario eliminado correctamente')
      loadUsers()
    } catch (error) {
      console.error('Error deleting user:', error)
      setError(error.response?.data?.message || 'Error eliminando usuario')
    }
  }

  if (loading) {
    return <div className='p-6'>Cargando usuarios...</div>
  }

  return (
    <div className='p-6'>
      <div className='flex justify-between items-center mb-6'>
        <h1 className='text-3xl font-bold'>Usuarios</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className='bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700'
        >
          {showForm ? 'Cancelar' : 'Invitar usuario'}
        </button>
      </div>

      {error && (
        <div className='bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4'>
          {error}
        </div>
      )}

      {successMessage && (
        <div className='bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-4'>
          {successMessage}
        </div>
      )}

      {showForm && (
        <div className='bg-white p-6 rounded-lg shadow-md mb-6'>
          <h2 className='text-xl font-semibold mb-4'>Invitar Nuevo Usuario</h2>
          <form onSubmit={handleSubmit} className='space-y-4'>
            <div>
              <label className='block text-sm font-medium mb-1'>Email</label>
              <input
                type='email'
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className='w-full p-2 border rounded-lg'
                required
              />
            </div>
            <div>
              <label className='block text-sm font-medium mb-1'>Rol</label>
              <select
                value={formData.role}
                onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                className='w-full p-2 border rounded-lg'
              >
                <option value='employee'>Empleado</option>
                <option value='company_admin'>Administrador Empresa</option>
                <option value='restaurant_admin'>Administrador Restaurante</option>
                <option value='admin'>Admin</option>
              </select>
            </div>
            <button
              type='submit'
              className='bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 w-full'
            >
              Enviar invitación
            </button>
          </form>
        </div>
      )}

      <div className='bg-white rounded-lg shadow-md'>
        <div className='p-6'>
          <h2 className='text-xl font-semibold mb-4'>Lista de Usuarios</h2>
          {users.length === 0 ? (
            <p className='text-gray-500'>No hay usuarios en este tenant</p>
          ) : (
            <div className='overflow-x-auto'>
              <table className='w-full'>
                <thead>
                  <tr className='border-b'>
                    <th className='text-left py-3 px-4'>Email</th>
                    <th className='text-left py-3 px-4'>Nombre</th>
                    <th className='text-left py-3 px-4'>Rol</th>
                    <th className='text-left py-3 px-4'>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user) => (
                    <tr key={user.id} className='border-b hover:bg-gray-50'>
                      <td className='py-3 px-4'>{user.email}</td>
                      <td className='py-3 px-4'>{user.full_name || '-'}</td>
                      <td className='py-3 px-4 capitalize'>{user.role}</td>
                      <td className='py-3 px-4'>
                        <button
                          onClick={() => confirmDelete(user)}
                          className='text-xs bg-red-100 text-red-700 px-2 py-1 rounded hover:bg-red-200 transition-colors'
                        >
                          Eliminar
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {deleteConfirm.show && (
        <div className='fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50'>
          <div className='bg-white p-6 rounded-lg shadow-lg max-w-md w-full mx-4'>
            <div className='flex justify-between items-center mb-4'>
              <h3 className='text-lg font-semibold text-red-600'>Confirmar Eliminación</h3>
              <button
                onClick={() => setDeleteConfirm({ show: false, user: null })}
                className='text-gray-500 hover:text-gray-700 text-xl'
              >
                ×
              </button>
            </div>
            <p className='text-gray-700 mb-4'>
              ¿Estás seguro de que quieres eliminar al usuario <strong>{deleteConfirm.user?.email}</strong>?
              Esta acción no se puede deshacer.
            </p>
            <div className='flex gap-3'>
              <button
                onClick={() => setDeleteConfirm({ show: false, user: null })}
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
