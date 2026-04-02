'use client'

import { useState, useEffect } from 'react'
import api from '@/utils/api'

export default function MealLogsPage() {
  const [mealLogs, setMealLogs] = useState([])
  const [employees, setEmployees] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    employee_id: '',
    agreement_id: '',
    meal_type: 'almuerzo',
    total_amount: ''
  })

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [logsRes, empRes] = await Promise.all([
        api.get('/api/meal-logs'),
        api.get('/api/employees')
      ])
      setMealLogs(logsRes.data.data || [])
      setEmployees(empRes.data.data || [])
    } catch (error) {
      console.error('Error loading data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = {
        ...formData,
        employee_id: parseInt(formData.employee_id),
        agreement_id: parseInt(formData.agreement_id),
        total_amount: parseFloat(formData.total_amount)
      }
      await api.post('/api/meal-logs', data)
      setFormData({
        employee_id: '',
        agreement_id: '',
        meal_type: 'almuerzo',
        total_amount: ''
      })
      setShowForm(false)
      loadData()
    } catch (error) {
      console.error('Error creating meal log:', error)
      alert('Error creando registro de consumo')
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
          {showForm ? 'Cancelar' : 'Nuevo Registro'}
        </button>
      </div>

      {showForm && (
        <div className='bg-white p-6 rounded-lg shadow-md mb-6'>
          <h2 className='text-xl font-semibold mb-4'>Crear Nuevo Registro de Consumo</h2>
          <form onSubmit={handleSubmit} className='space-y-4'>
            <div>
              <label className='block text-sm font-medium mb-1'>Empleado</label>
              <select
                value={formData.employee_id}
                onChange={(e) => setFormData({...formData, employee_id: e.target.value})}
                className='w-full p-2 border rounded-lg'
                required
              >
                <option value=''>Seleccionar empleado</option>
                {employees.map(emp => (
                  <option key={emp.id} value={emp.id}>{emp.name} - {emp.email}</option>
                ))}
              </select>
            </div>
            <div>
              <label className='block text-sm font-medium mb-1'>ID del Acuerdo</label>
              <input
                type='number'
                value={formData.agreement_id}
                onChange={(e) => setFormData({...formData, agreement_id: e.target.value})}
                className='w-full p-2 border rounded-lg'
                placeholder='Ingrese ID del acuerdo'
                required
              />
            </div>
            <div>
              <label className='block text-sm font-medium mb-1'>Tipo de Comida</label>
              <select
                value={formData.meal_type}
                onChange={(e) => setFormData({...formData, meal_type: e.target.value})}
                className='w-full p-2 border rounded-lg'
              >
                <option value='almuerzo'>Almuerzo</option>
                <option value='cena'>Cena</option>
              </select>
            </div>
            <div>
              <label className='block text-sm font-medium mb-1'>Monto Total</label>
              <input
                type='number'
                step='0.01'
                value={formData.total_amount}
                onChange={(e) => setFormData({...formData, total_amount: e.target.value})}
                className='w-full p-2 border rounded-lg'
                required
              />
            </div>
            <button
              type='submit'
              className='bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700'
            >
              Crear Registro
            </button>
          </form>
        </div>
      )}

      <div className='bg-white rounded-lg shadow-md'>
        <div className='p-6'>
          <h2 className='text-xl font-semibold mb-4'>Lista de Registros de Consumo</h2>
          {mealLogs.length === 0 ? (
            <p className='text-gray-500'>No hay registros de consumo</p>
          ) : (
            <div className='space-y-4'>
              {mealLogs.map(log => (
                <div key={log.id} className='border rounded-lg p-4'>
                  <div className='flex justify-between'>
                    <div>
                      <p className='font-semibold'>Empleado ID: {log.employee_id}</p>
                      <p className='text-sm text-gray-600'>Tipo: {log.meal_type}</p>
                      <p className='text-sm text-gray-600'>Fecha: {log.date}</p>
                    </div>
                    <div className='text-right'>
                      <p className='font-semibold'>${log.total_amount}</p>
                      <p className='text-sm text-gray-600'>ID: {log.id}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}