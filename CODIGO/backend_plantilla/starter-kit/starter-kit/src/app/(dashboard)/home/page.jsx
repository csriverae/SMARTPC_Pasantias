'use client'

import { Fragment, useState, useEffect } from 'react'
import api from '@/utils/api'
import { StatCard, Badge } from '@/components/ui/Button'
import { Card, CardHeader, CardBody } from '@/components/ui/Card'
import Link from 'next/link'

export default function Dashboard() {
  const [stats, setStats] = useState({
    companies: 0,
    employees: 0,
    billing: 0,
    agreements: 0
  })
  const [recentData, setRecentData] = useState({
    companies: [],
    employees: [],
    mealLogs: [],
    agreements: []
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [companiesRes, employeesRes, mealLogsRes, agreementsRes] = await Promise.all([
        api.get('/api/companies'),
        api.get('/api/employees'),
        api.get('/api/meal-logs'),
        api.get('/api/agreements')
      ])

      const companiesData = companiesRes.data.data || []
      const employeesData = employeesRes.data.data || []
      const mealLogsData = mealLogsRes.data.data || []
      const agreementsData = agreementsRes.data.data || []

      const totalBilling = mealLogsData.reduce((sum, log) => sum + (log.total_amount || 0), 0)

      setStats({
        companies: companiesData.length,
        employees: employeesData.length,
        billing: totalBilling,
        agreements: agreementsData.length
      })

      setRecentData({
        companies: companiesData.slice(0, 5),
        employees: employeesData.slice(0, 5),
        mealLogs: mealLogsData.slice(0, 5),
        agreements: agreementsData.slice(0, 5)
      })
    } catch (error) {
      console.error('Error loading data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className='min-h-screen bg-gradient-to-br from-indigo-50 to-blue-50 flex items-center justify-center'>
        <div className='text-center'>
          <div className='inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4'></div>
          <p className='text-gray-600'>Cargando dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <Fragment>
      <div className='pt-6 px-6 sm:px-8 pb-8'>
        {/* Header */}
        <div className='mb-8'>
          <h1 className='text-4xl font-bold text-gray-900'>Dashboard</h1>
          <p className='text-gray-600 mt-2'>Bienvenido a MesaPass - Panel de control</p>
        </div>

        {/* Stats Grid */}
        <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8'>
          <Link href='/companies'>
            <StatCard
              icon='🏢'
              label='Empresas'
              value={stats.companies}
              trend={stats.companies > 0 ? '+0%' : 'Sin registros'}
            />
          </Link>
          <Link href='/employees'>
            <StatCard
              icon='👨‍💼'
              label='Empleados'
              value={stats.employees}
              trend={stats.employees > 0 ? '+0%' : 'Sin registros'}
            />
          </Link>
          <Link href='/meal-logs'>
            <StatCard
              icon='💰'
              label='Facturación'
              value={`$${stats.billing.toFixed(2)}`}
              trend={stats.billing > 0 ? '↑ Activo' : 'Sin movimiento'}
              trendUp={true}
            />
          </Link>
          <Link href='/agreements'>
            <StatCard
              icon='📋'
              label='Acuerdos'
              value={stats.agreements}
              trend={stats.agreements > 0 ? 'Activos' : 'Sin registros'}
            />
          </Link>
        </div>

        {/* Main Content Grid */}
        <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
          {/* Empresas Registradas */}
          <Card>
            <CardHeader>
              <div className='flex items-center justify-between'>
                <div>
                  <h2 className='text-lg font-semibold text-gray-900'>Empresas Registradas</h2>
                  <p className='text-sm text-gray-600 mt-1'>Últimas empresas añadidas</p>
                </div>
                <Link href='/companies' className='text-indigo-600 hover:text-indigo-700 font-medium text-sm'>
                  Ver más →
                </Link>
              </div>
            </CardHeader>
            <CardBody>
              {recentData.companies.length === 0 ? (
                <div className='text-center py-8 text-gray-500'>
                  <p>No hay empresas registradas</p>
                  <Link href='/companies' className='text-indigo-600 hover:text-indigo-700 font-medium text-sm mt-2 inline-block'>
                    Crear empresa
                  </Link>
                </div>
              ) : (
                <div className='space-y-3'>
                  {recentData.companies.map(company => (
                    <div key={company.id} className='flex items-center justify-between p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition'>
                      <div>
                        <p className='font-medium text-gray-900'>{company.name}</p>
                        <p className='text-xs text-gray-500'>RUC: {company.ruc || 'N/A'}</p>
                      </div>
                      <Badge variant='primary' size='sm'>ID: {company.id}</Badge>
                    </div>
                  ))}
                </div>
              )}
            </CardBody>
          </Card>

          {/* Empleados Registrados */}
          <Card>
            <CardHeader>
              <div className='flex items-center justify-between'>
                <div>
                  <h2 className='text-lg font-semibold text-gray-900'>Empleados Registrados</h2>
                  <p className='text-sm text-gray-600 mt-1'>Últimos empleados añadidos</p>
                </div>
                <Link href='/employees' className='text-indigo-600 hover:text-indigo-700 font-medium text-sm'>
                  Ver más →
                </Link>
              </div>
            </CardHeader>
            <CardBody>
              {recentData.employees.length === 0 ? (
                <div className='text-center py-8 text-gray-500'>
                  <p>No hay empleados registrados</p>
                  <Link href='/employees' className='text-indigo-600 hover:text-indigo-700 font-medium text-sm mt-2 inline-block'>
                    Crear empleado
                  </Link>
                </div>
              ) : (
                <div className='space-y-3'>
                  {recentData.employees.map(employee => (
                    <div key={employee.id} className='flex items-center justify-between p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition'>
                      <div className='flex-1'>
                        <p className='font-medium text-gray-900'>{employee.name}</p>
                        <p className='text-xs text-gray-500'>{employee.email}</p>
                      </div>
                      <Badge variant='success' size='sm'>Activo</Badge>
                    </div>
                  ))}
                </div>
              )}
            </CardBody>
          </Card>

          {/* Acuerdos */}
          <Card>
            <CardHeader>
              <div className='flex items-center justify-between'>
                <div>
                  <h2 className='text-lg font-semibold text-gray-900'>Acuerdos</h2>
                  <p className='text-sm text-gray-600 mt-1'>Acuerdos empresa-restaurante</p>
                </div>
                <Link href='/agreements' className='text-indigo-600 hover:text-indigo-700 font-medium text-sm'>
                  Ver más →
                </Link>
              </div>
            </CardHeader>
            <CardBody>
              {recentData.agreements.length === 0 ? (
                <div className='text-center py-8 text-gray-500'>
                  <p>No hay acuerdos registrados</p>
                  <Link href='/agreements' className='text-indigo-600 hover:text-indigo-700 font-medium text-sm mt-2 inline-block'>
                    Crear acuerdo
                  </Link>
                </div>
              ) : (
                <div className='space-y-3'>
                  {recentData.agreements.map(agreement => (
                    <div key={agreement.id} className='flex items-center justify-between p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition'>
                      <div>
                        <p className='font-medium text-gray-900'>Acuerdo #{agreement.id}</p>
                        <p className='text-xs text-gray-500'>Vigente</p>
                      </div>
                      <Badge variant='default' size='sm'>#{agreement.id}</Badge>
                    </div>
                  ))}
                </div>
              )}
            </CardBody>
          </Card>

          {/* Consumos Recientes */}
          <Card>
            <CardHeader>
              <div className='flex items-center justify-between'>
                <div>
                  <h2 className='text-lg font-semibold text-gray-900'>Consumos Recientes</h2>
                  <p className='text-sm text-gray-600 mt-1'>Últimos registros de comidas</p>
                </div>
                <Link href='/meal-logs' className='text-indigo-600 hover:text-indigo-700 font-medium text-sm'>
                  Ver más →
                </Link>
              </div>
            </CardHeader>
            <CardBody>
              {recentData.mealLogs.length === 0 ? (
                <div className='text-center py-8 text-gray-500'>
                  <p>No hay registros de consumo</p>
                  <Link href='/meal-logs' className='text-indigo-600 hover:text-indigo-700 font-medium text-sm mt-2 inline-block'>
                    Registrar consumo
                  </Link>
                </div>
              ) : (
                <div className='space-y-3'>
                  {recentData.mealLogs.map(log => (
                    <div key={log.id} className='flex items-center justify-between p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition'>
                      <div>
                        <p className='font-medium text-gray-900'>Empleado #{log.employee_id}</p>
                        <p className='text-xs text-gray-500'>{log.meal_type} - {log.date}</p>
                      </div>
                      <Badge variant='primary' size='sm'>${log.total_amount}</Badge>
                    </div>
                  ))}
                </div>
              )}
            </CardBody>
          </Card>
        </div>
      </div>
    </Fragment>
  )
}

      </div>
    </Fragment>
  )
}
