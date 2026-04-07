'use client'

import { useState, useEffect } from 'react'
import api from '@/utils/api'

export default function MealLogsPage() {
  const [mealLogs, setMealLogs] = useState([])
  const [employees, setEmployees] = useState([])
  const [agreements, setAgreements] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    employee_id: '',
    agreement_id: '',
    meal_type: 'almuerzo',
    consumption_date: new Date().toISOString().split('T')[0],
    quantity: '1'
  })
  const [error, setError] = useState('')

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [logsRes, empRes, agRes] = await Promise.all([
        api.get('/api/meal-logs'),
        api.get('/api/employees'),
        api.get('/api/agreements')
      ])
      setMealLogs(logsRes.data.data || [])
      setEmployees(empRes.data.data || [])
      setAgreements(agRes.data.data || [])
      setError('')
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
      const data = {
        ...formData,
        employee_id: parseInt(formData.employee_id),
        agreement_id: parseInt(formData.agreement_id),
        quantity: parseInt(formData.quantity)
      }
      await api.post('/api/meal-logs', data)
      setFormData({
        employee_id: '',
        agreement_id: '',
        meal_type: 'almuerzo',
        consumption_date: new Date().toISOString().split('T')[0],
        quantity: '1'
      })
      setShowForm(false)
      loadData()
    } catch (error) {
      console.error('Error creating meal log:', error)
      setError(error.response?.data?.message || 'Error registrando consumo')
    }
  }

  if (loading) {
    return <div className='p-6'>Cargando registros de consumo...</div>
  }

  return (
    <div className='p-6'>
      <div className='flex justify-between items-center mb-6'>
        <h1 className='text-3xl font-bold'>Registros de Consumo</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className='bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700'
        >
          {showForm ? 'Cancelar' : 'Nuevo Consumo'}
        </button>
      </div>

      {error && (
        <div className='bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4'>
          {error}
        </div>
      )}

      {showForm && (
        <div className='bg-white p-6 rounded-lg shadow-md mb-6'>
          <h2 className='text-xl font-semibold mb-4'>Registrar Nuevo Consumo</h2>
          <form onSubmit={handleSubmit} className='space-y-4'>
            <div className='grid grid-cols-2 gap-4'>
              <div>
                <label className='block text-sm font-medium mb-1'>Empleado</label>
                <select
                  value={formData.employee_id}
                  onChange={(e) => setFormData({...formData, employee_id: e.target.value})}
                  className='w-full p-2 border rounded-lg'
                  required
                >
                  <option value=''>Seleccionar empleado</option>
                  {employees.map(e => (
                    <option key={e.id} value={e.id}>{e.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className='block text-sm font-medium mb-1'>Acuerdo</label>
                <select
                  value={formData.agreement_id}
                  onChange={(e) => setFormData({...formData, agreement_id: e.target.value})}
                  className='w-full p-2 border rounded-lg'
                  required
                >
                  <option value=''>Seleccionar acuerdo</option>
                  {agreements.map(a => (
                    <option key={a.id} value={a.id}>
                      Acuerdo {a.id}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className='grid grid-cols-3 gap-4'>
              <div>
                <label className='block text-sm font-medium mb-1'>Tipo de Comida</label>
                <select
                  value={formData.meal_type}
                  onChange={(e) => setFormData({...formData, meal_type: e.target.value})}
                  className='w-full p-2 border rounded-lg'
                >
                  <option value='desayuno'>Desayuno</option>
                  <option value='almuerzo'>Almuerzo</option>
                  <option value='merienda'>Merienda</option>
                  <option value='cena'>Cena</option>
                </select>
              </div>

              <div>
                <label className='block text-sm font-medium mb-1'>Fecha de Consumo</label>
                <input
                  type='date'
                  value={formData.consumption_date}
                  onChange={(e) => setFormData({...formData, consumption_date: e.target.value})}
                  className='w-full p-2 border rounded-lg'
                  required
                />
              </div>

              <div>
                <label className='block text-sm font-medium mb-1'>Cantidad</label>
                <input
                  type='number'
                  min='1'
                  value={formData.quantity}
                  onChange={(e) => setFormData({...formData, quantity: e.target.value})}
                  className='w-full p-2 border rounded-lg'
                  required
                />
              </div>
            </div>

            <button
              type='submit'
              className='bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 w-full'
            >
              Registrar Consumo
            </button>
          </form>
        </div>
      )}

      <div className='bg-white rounded-lg shadow-md'>
        <div className='p-6'>
          <h2 className='text-xl font-semibold mb-4'>Listado de Consumos</h2>
          {mealLogs.length === 0 ? (
            <p className='text-gray-500'>No hay registros de consumo</p>
          ) : (
            <div className='overflow-x-auto'>
              <table className='w-full'>
                <thead>
                  <tr className='border-b'>
                    <th className='text-left py-2 px-4'>ID</th>
                    <th className='text-left py-2 px-4'>Empleado</th>
                    <th className='text-left py-2 px-4'>Tipo de Comida</th>
                    <th className='text-left py-2 px-4'>Fecha</th>
                    <th className='text-left py-2 px-4'>Cantidad</th>
                  </tr>
                </thead>
                <tbody>
                  {mealLogs.map(log => {
                    const employee = employees.find(e => e.id === log.employee_id)
                    return (
                      <tr key={log.id} className='border-b hover:bg-gray-50'>
                        <td className='py-2 px-4'>{log.id}</td>
                        <td className='py-2 px-4'>{employee?.name || 'N/A'}</td>
                        <td className='py-2 px-4 capitalize'>{log.meal_type}</td>
                        <td className='py-2 px-4'>{log.consumption_date}</td>
                        <td className='py-2 px-4'>{log.quantity}</td>
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