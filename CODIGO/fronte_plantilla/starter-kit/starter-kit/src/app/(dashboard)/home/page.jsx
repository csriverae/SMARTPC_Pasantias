'use client'

import { Fragment, useState, useEffect } from 'react'
import api from '@/utils/api'

export default function Page() {
  const [stats, setStats] = useState([
    { label: 'Empresas', value: '0', icon: 'tabler-building', change: 'Cargando...' },
    { label: 'Empleados', value: '0', icon: 'tabler-users', change: 'Cargando...' },
    { label: 'Consumos', value: '0', icon: 'tabler-shopping-cart', change: 'Cargando...' },
    { label: 'Acuerdos', value: '0', icon: 'tabler-file-text', change: 'Cargando...' }
  ])
  const [companies, setCompanies] = useState([])
  const [employees, setEmployees] = useState([])
  const [mealLogs, setMealLogs] = useState([])
  const [agreements, setAgreements] = useState([])
  const [billingSummary, setBillingSummary] = useState({ total_billing: 0, agreements_count: 0 })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadData = async () => {
      try {
        const [companiesRes, employeesRes, mealLogsRes, agreementsRes, billingRes] = await Promise.all([
          api.get('/api/companies'),
          api.get('/api/employees'),
          api.get('/api/meal-logs'),
          api.get('/api/agreements'),
          api.get('/api/reports/billing')
        ])

        const companiesData = companiesRes.data.data || []
        const employeesData = employeesRes.data.data || []
        const mealLogsData = mealLogsRes.data.data || []
        const agreementsData = agreementsRes.data.data || []
        const billingData = billingRes.data.data || {}

        setCompanies(companiesData)
        setEmployees(employeesData)
        setMealLogs(mealLogsData)
        setAgreements(agreementsData)
        setBillingSummary(billingData.summary || { total_billing: 0, agreements_count: 0 })

        const totalConsumption = mealLogsData.reduce((sum, log) => sum + (log.total_amount || 0), 0)
        const totalBilling = billingData.summary?.total_billing || 0
        const agreementsCount = billingData.summary?.agreements_count || agreementsData.length

        setStats([
          { label: 'Empresas', value: companiesData.length.toString(), icon: 'tabler-building', change: 'Total registrado' },
          { label: 'Empleados', value: employeesData.length.toString(), icon: 'tabler-users', change: 'Total registrado' },
          { label: 'Facturación', value: `$${totalBilling.toFixed(2)}`, icon: 'tabler-cash', change: `${agreementsCount} acuerdos` },
          { label: 'Acuerdos', value: agreementsCount.toString(), icon: 'tabler-file-text', change: 'Activos' }
        ])
      } catch (error) {
        console.error('Error loading data:', error)
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [])

  if (loading) {
    return (
      <div className='py-6 px-6 sm:px-8'>
        <h1 className='text-3xl font-bold tracking-tight text-slate-900 mb-5'>Dashboard</h1>
        <p className='text-sm text-slate-500 mb-8'>Cargando datos...</p>
      </div>
    )
  }

  return (
    <Fragment>
      <div className='py-6 px-6 sm:px-8'>
        <h1 className='text-3xl font-bold tracking-tight text-slate-900 mb-5'>Dashboard</h1>
        <p className='text-sm text-slate-500 mb-8'>Bienvenido a Mesapass: tu panel principal con datos reales del backend.</p>

        <div className='grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6'>
          {stats.map(item => (
            <article key={item.label} className='bg-white border border-slate-200 rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow'>
              <div className='flex items-center justify-between'>
                <div>
                  <p className='text-xs text-slate-400 uppercase tracking-wide'>{item.label}</p>
                  <p className='text-2xl font-semibold text-slate-900'>{item.value}</p>
                </div>
                <span className='inline-flex items-center justify-center w-10 h-10 bg-indigo-100 text-indigo-600 rounded-lg'>
                  <i className={item.icon}></i>
                </span>
              </div>
              <p className='text-xs text-emerald-500 mt-3'>{item.change}</p>
            </article>
          ))}
        </div>

        <div className='grid gap-4 lg:grid-cols-2'>
          <section className='bg-white border border-slate-200 rounded-xl p-4 shadow-sm'>
            <header className='flex items-center justify-between mb-3'>
              <h2 className='text-lg font-semibold text-slate-900'>Empresas Registradas</h2>
              <span className='text-xs text-slate-500'>{companies.length} total</span>
            </header>
            <ul className='space-y-3'>
              {companies.slice(0, 5).map(company => (
                <li key={company.id} className='flex justify-between items-center p-2 rounded-md hover:bg-slate-100'>
                  <span>{company.name}</span>
                  <span className='text-xs text-slate-500'>ID: {company.id}</span>
                </li>
              ))}
              {companies.length === 0 && (
                <li className='text-sm text-slate-500'>No hay empresas registradas</li>
              )}
            </ul>
          </section>
          <section className='bg-white border border-slate-200 rounded-xl p-4 shadow-sm'>
            <header className='flex items-center justify-between mb-3'>
              <h2 className='text-lg font-semibold text-slate-900'>Empleados Registrados</h2>
              <span className='text-xs text-slate-500'>{employees.length} total</span>
            </header>
            <ul className='space-y-3'>
              {employees.slice(0, 5).map(employee => (
                <li key={employee.id} className='flex justify-between items-center p-2 rounded-md hover:bg-slate-100'>
                  <span>{employee.name} - {employee.email}</span>
                  <span className='text-xs text-slate-500'>ID: {employee.id}</span>
                </li>
              ))}
              {employees.length === 0 && (
                <li className='text-sm text-slate-500'>No hay empleados registrados</li>
              )}
            </ul>
          </section>
        </div>

        <div className='mt-6'>
          <section className='bg-white border border-slate-200 rounded-xl p-4 shadow-sm'>
            <header className='flex items-center justify-between mb-3'>
              <h2 className='text-lg font-semibold text-slate-900'>Registros de Consumo Recientes</h2>
              <span className='text-xs text-slate-500'>{mealLogs.length} total</span>
            </header>
            <ul className='space-y-3'>
              {mealLogs.slice(0, 10).map(log => (
                <li key={log.id} className='flex justify-between items-center p-2 rounded-md hover:bg-slate-100'>
                  <span>Empleado ID {log.employee_id} - {log.meal_type} - ${log.total_amount}</span>
                  <span className='text-xs text-slate-500'>{log.date}</span>
                </li>
              ))}
              {mealLogs.length === 0 && (
                <li className='text-sm text-slate-500'>No hay registros de consumo</li>
              )}
            </ul>
          </section>
        </div>
      </div>
    </Fragment>
  )
}
