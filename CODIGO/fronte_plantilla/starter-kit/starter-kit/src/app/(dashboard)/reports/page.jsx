'use client'

import { useState } from 'react'
import api from '@/utils/api'

export default function ReportsPage() {
  const [reportType, setReportType] = useState('consumption')
  const [loading, setLoading] = useState(false)
  const [reportData, setReportData] = useState(null)
  const [error, setError] = useState('')

  const generateReport = async (type) => {
    try {
      setLoading(true)
      setError('')
      setReportData(null)

      const endpoint = type === 'consumption' 
        ? '/api/reports/consumption'
        : '/api/reports/billing'

      const response = await api.get(endpoint)
      setReportData(response.data.data)
    } catch (error) {
      console.error('Error generating report:', error)
      setError(error.response?.data?.message || 'Error generando reporte')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className='p-6'>
      <h1 className='text-3xl font-bold mb-6'>Reportes</h1>

      <div className='grid grid-cols-1 md:grid-cols-2 gap-4 mb-6'>
        <button
          onClick={() => {
            setReportType('consumption')
            generateReport('consumption')
          }}
          className={`p-6 rounded-lg font-semibold transition-all ${
            reportType === 'consumption'
              ? 'bg-indigo-600 text-white shadow-lg'
              : 'bg-white border-2 border-gray-200 text-gray-700 hover:border-indigo-600'
          }`}
        >
          📊 Reporte de Consumo
        </button>

        <button
          onClick={() => {
            setReportType('billing')
            generateReport('billing')
          }}
          className={`p-6 rounded-lg font-semibold transition-all ${
            reportType === 'billing'
              ? 'bg-indigo-600 text-white shadow-lg'
              : 'bg-white border-2 border-gray-200 text-gray-700 hover:border-indigo-600'
          }`}
        >
          💳 Reporte de Facturación
        </button>
      </div>

      {error && (
        <div className='bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4'>
          {error}
        </div>
      )}

      {loading && (
        <div className='bg-blue-50 border border-blue-200 text-blue-700 px-4 py-3 rounded-lg mb-4'>
          Generando reporte...
        </div>
      )}

      {reportData && (
        <div className='bg-white rounded-lg shadow-md p-6'>
          <h2 className='text-2xl font-semibold mb-4'>
            {reportType === 'consumption' ? 'Reporte de Consumo' : 'Reporte de Facturación'}
          </h2>

          {Array.isArray(reportData) && reportData.length === 0 ? (
            <p className='text-gray-500'>No hay datos para mostrar</p>
          ) : Array.isArray(reportData) ? (
            <div className='overflow-x-auto'>
              <table className='w-full'>
                <thead>
                  <tr className='border-b'>
                    <th className='text-left py-3 px-4 font-semibold'>Empleado</th>
                    <th className='text-left py-3 px-4 font-semibold'>Total Consumos</th>
                    <th className='text-left py-3 px-4 font-semibold'>Monto Total</th>
                  </tr>
                </thead>
                <tbody>
                  {reportData.map((row, idx) => (
                    <tr key={idx} className='border-b hover:bg-gray-50'>
                      <td className='py-3 px-4'>{row.employee_name || row.name}</td>
                      <td className='py-3 px-4'>{row.total_meals || row.count || '-'}</td>
                      <td className='py-3 px-4'>${(row.total_amount || row.amount || 0).toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <pre className='bg-gray-100 p-4 rounded overflow-auto'>
              {JSON.stringify(reportData, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  )
}
