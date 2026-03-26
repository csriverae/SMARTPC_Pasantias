export const ErrorMessage = ({ title = 'Error', message }: { title?: string; message: string }) => (
  <div className='bg-red-50 border border-red-200 rounded-lg p-4 text-red-800'>
    <h3 className='font-bold text-red-900'>{title}</h3>
    <p className='text-sm mt-1'>{message}</p>
  </div>
)
