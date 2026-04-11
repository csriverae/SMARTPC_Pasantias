export const LoadingSpinner = () => (
  <div className='flex justify-center items-center min-h-screen'>
    <div className='animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600'></div>
  </div>
)

export const SkeletonCard = () => (
  <div className='bg-white rounded-lg p-6 shadow-md animate-pulse'>
    <div className='h-6 bg-slate-200 rounded w-1/3 mb-4'></div>
    <div className='h-4 bg-slate-200 rounded w-2/3 mb-2'></div>
    <div className='h-4 bg-slate-200 rounded w-1/2'></div>
  </div>
)
