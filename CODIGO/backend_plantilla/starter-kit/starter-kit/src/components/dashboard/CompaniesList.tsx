'use client'

interface Company {
  id: string
  name: string
  ruc: string
}

interface CompaniesListProps {
  companies: Company[]
  onCreateClick: () => void
  isLoading?: boolean
}

export default function CompaniesList({ companies, onCreateClick, isLoading }: CompaniesListProps) {
  if (isLoading) {
    return (
      <div className='bg-white border border-slate-200 rounded-xl p-6'>
        <div className='animate-pulse space-y-4'>
          <div className='h-4 bg-slate-200 rounded w-1/4'></div>
          <div className='grid grid-cols-3 gap-4'>
            <div className='h-24 bg-slate-100 rounded'></div>
            <div className='h-24 bg-slate-100 rounded'></div>
            <div className='h-24 bg-slate-100 rounded'></div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className='bg-white border border-slate-200 rounded-xl p-6'>
      <div className='flex items-center justify-between mb-4'>
        <h2 className='text-xl font-semibold text-slate-900'>Empresas</h2>
        <button
          onClick={onCreateClick}
          className='px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm font-medium transition-colors'
        >
          + Crear Empresa
        </button>
      </div>

      {companies.length === 0 ? (
        <div className='text-center py-12'>
          <p className='text-slate-500'>No hay empresas registradas</p>
          <p className='text-sm text-slate-400 mt-1'>Crea tu primera empresa para comenzar</p>
        </div>
      ) : (
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
          {companies.map(company => (
            <div
              key={company.id}
              className='border border-slate-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer'
            >
              <h3 className='font-semibold text-slate-900 truncate'>{company.name}</h3>
              <p className='text-sm text-slate-500 mt-2'>
                <span className='text-xs text-slate-400 uppercase'>RUC:</span> {company.ruc}
              </p>
              <div className='mt-4 pt-4 border-t border-slate-100'>
                <button className='text-sm text-indigo-600 hover:text-indigo-700 font-medium'>
                  Ver detalles →
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
