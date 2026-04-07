'use client'

import { useEffect, useState } from 'react'
import api from '@/utils/api'

export default function TenantsPage() {
  const [companies, setCompanies] = useState([])
  const [restaurants, setRestaurants] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadData = async () => {
      try {
        const [companiesRes, restaurantsRes] = await Promise.all([
          api.get('/api/companies'),
          api.get('/api/restaurants')
        ])

        setCompanies(companiesRes.data.data || [])
        setRestaurants(restaurantsRes.data.data || [])
        setError('')
      } catch (err) {
        console.error('Error loading tenants:', err)
        setError('Error cargando empresas y restaurantes')
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [])

  if (loading) {
    return <div className='p-6'>Cargando empresas y restaurantes...</div>
  }

  return (
    <div className='p-6'>
      <div className='flex flex-col gap-3 mb-6'>
        <h1 className='text-3xl font-bold'>Tenants</h1>
        <p className='text-slate-500'>Datos reales de empresas y restaurantes asociados al tenant actual.</p>
      </div>

      {error && (
        <div className='bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4'>
          {error}
        </div>
      )}

      <div className='grid gap-6 lg:grid-cols-2'>
        <section className='bg-white border border-slate-200 rounded-xl p-6 shadow-sm'>
          <div className='flex items-center justify-between mb-4'>
            <div>
              <h2 className='text-xl font-semibold text-slate-900'>Empresas</h2>
              <p className='text-sm text-slate-500'>{companies.length} empresas registradas</p>
            </div>
          </div>
          {companies.length === 0 ? (
            <p className='text-gray-500'>No hay empresas disponibles</p>
          ) : (
            <div className='space-y-3'>
              {companies.map(company => (
                <div key={company.id} className='border rounded-lg p-4'>
                  <h3 className='font-semibold text-slate-900'>{company.name}</h3>
                  <p className='text-sm text-slate-500'>RUC: {company.ruc || 'N/A'}</p>
                  <p className='text-sm text-slate-500'>ID: {company.id}</p>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className='bg-white border border-slate-200 rounded-xl p-6 shadow-sm'>
          <div className='flex items-center justify-between mb-4'>
            <div>
              <h2 className='text-xl font-semibold text-slate-900'>Restaurantes</h2>
              <p className='text-sm text-slate-500'>{restaurants.length} registros</p>
            </div>
          </div>
          {restaurants.length === 0 ? (
            <p className='text-gray-500'>No hay restaurantes disponibles</p>
          ) : (
            <div className='space-y-3'>
              {restaurants.map(restaurant => (
                <div key={restaurant.id} className='border rounded-lg p-4'>
                  <h3 className='font-semibold text-slate-900'>{restaurant.name}</h3>
                  <p className='text-sm text-slate-500'>ID: {restaurant.id}</p>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  )
}
