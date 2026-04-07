'use client'

import { useState } from 'react'
import api from '@/utils/api'

export default function QRValidatorPage() {
  const [qrToken, setQrToken] = useState('')
  const [employeeData, setEmployeeData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  const handleValidate = async (e) => {
    e.preventDefault()
    if (!qrToken.trim()) {
      setError('Por favor ingresa un token QR')
      return
    }

    try {
      setLoading(true)
      setError('')
      setSuccess(false)
      setEmployeeData(null)

      const response = await api.post('/api/validate-qr', { qr_token: qrToken })
      setEmployeeData(response.data.data.data)
      setSuccess(true)
      setQrToken('')
    } catch (error) {
      console.error('Error validating QR:', error)
      setError(error.response?.data?.message || 'Token QR inválido o expirado')
      setEmployeeData(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className='p-6 max-w-2xl mx-auto'>
      <h1 className='text-3xl font-bold mb-6'>Validador de QR</h1>

      <div className='bg-white rounded-lg shadow-md p-6 mb-6'>
        <h2 className='text-xl font-semibold mb-4'>Escanear o Ingresar Token QR</h2>
        
        <form onSubmit={handleValidate} className='space-y-4'>
          <div>
            <label className='block text-sm font-medium mb-2'>Token QR</label>
            <input
              type='text'
              value={qrToken}
              onChange={(e) => setQrToken(e.target.value.toUpperCase())}
              placeholder='Ej: 342AD2A8FD614E3D'
              className='w-full p-3 border-2 border-gray-300 rounded-lg focus:border-indigo-600 focus:outline-none text-center text-lg font-mono'
              autoFocus
              disabled={loading}
            />
          </div>

          <button
            type='submit'
            disabled={loading}
            className='w-full bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 disabled:bg-gray-400'
          >
            {loading ? 'Validando...' : 'Validar QR'}
          </button>
        </form>
      </div>

      {error && (
        <div className='bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4'>
          ❌ {error}
        </div>
      )}

      {success && employeeData && (
        <div className='bg-green-50 border border-green-200 rounded-lg p-6'>
          <h2 className='text-xl font-semibold text-green-700 mb-4'>✅ QR Válido</h2>
          
          <div className='space-y-4'>
            <div className='bg-white p-4 rounded-lg'>
              <h3 className='text-sm font-medium text-gray-600 mb-1'>Nombre del Empleado</h3>
              <p className='text-2xl font-bold text-gray-900'>{employeeData.employee_name}</p>
            </div>

            <div className='grid grid-cols-2 gap-4'>
              <div className='bg-white p-4 rounded-lg'>
                <h3 className='text-sm font-medium text-gray-600 mb-1'>Email</h3>
                <p className='text-lg font-semibold'>{employeeData.employee_email}</p>
              </div>

              <div className='bg-white p-4 rounded-lg'>
                <h3 className='text-sm font-medium text-gray-600 mb-1'>ID Empleado</h3>
                <p className='text-lg font-semibold'>{employeeData.employee_id}</p>
              </div>
            </div>

            <div className='grid grid-cols-2 gap-4'>
              <div className='bg-white p-4 rounded-lg'>
                <h3 className='text-sm font-medium text-gray-600 mb-1'>Token QR</h3>
                <p className='text-lg font-semibold font-mono'>{employeeData.qr_token}</p>
              </div>

              <div className='bg-white p-4 rounded-lg'>
                <h3 className='text-sm font-medium text-gray-600 mb-1'>Empresa ID</h3>
                <p className='text-lg font-semibold'>{employeeData.company_id}</p>
              </div>
            </div>

            <div className='bg-blue-50 border border-blue-200 rounded-lg p-4 mt-4'>
              <p className='text-sm text-blue-700'>
                ✓ Empleado verificado. Puedes registrar su consumo de comida.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
