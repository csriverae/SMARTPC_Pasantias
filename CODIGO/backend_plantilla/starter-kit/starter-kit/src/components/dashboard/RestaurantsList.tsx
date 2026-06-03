'use client'

interface Restaurant {
  id: string
  name: string
}

interface RestaurantsListProps {
  restaurants: Restaurant[]
  onCreateClick: () => void
  isLoading?: boolean
}

export default function RestaurantsList({ restaurants, onCreateClick, isLoading }: RestaurantsListProps) {
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
        <h2 className='text-xl font-semibold text-slate-900'>Restaurantes</h2>
        <button
          onClick={onCreateClick}
          className='px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm font-medium transition-colors'
        >
          + Crear Restaurante
        </button>
      </div>

      {restaurants.length === 0 ? (
        <div className='text-center py-12'>
          <p className='text-slate-500'>No hay restaurantes registrados</p>
          <p className='text-sm text-slate-400 mt-1'>Agrega tu primer restaurante para comenzar</p>
        </div>
      ) : (
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
          {restaurants.map(restaurant => (
            <div
              key={restaurant.id}
              className='border border-slate-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer'
            >
              <div className='flex items-start justify-between'>
                <h3 className='font-semibold text-slate-900 flex-1 truncate'>{restaurant.name}</h3>
                <i className='tabler-utensils text-indigo-600 text-lg'></i>
              </div>
              <p className='text-xs text-slate-400 mt-2'>ID: {restaurant.id?.substring(0, 8)}...</p>
              <div className='mt-4 pt-4 border-t border-slate-100'>
                <button className='text-sm text-indigo-600 hover:text-indigo-700 font-medium'>
                  Gestionar →
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
