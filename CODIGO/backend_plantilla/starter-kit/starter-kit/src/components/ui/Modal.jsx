'use client'

export function Modal({ isOpen, onClose, title, children, size = 'md' }) {
  if (!isOpen) return null

  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    '2xl': 'max-w-2xl'
  }

  return (
    <div className='fixed inset-0 z-50 flex items-center justify-center'>
      <div className='fixed inset-0 bg-black/50' onClick={onClose}></div>
      <div className={`bg-white rounded-lg shadow-xl max-h-[90vh] overflow-y-auto ${sizeClasses[size]}`}>
        <div className='sticky top-0 flex items-center justify-between p-6 border-b border-gray-200 bg-white'>
          <h2 className='text-lg font-semibold text-gray-900'>{title}</h2>
          <button
            onClick={onClose}
            className='text-gray-400 hover:text-gray-600 text-2xl leading-none'
          >
            ×
          </button>
        </div>
        <div className='p-6'>
          {children}
        </div>
      </div>
    </div>
  )
}

export function ConfirmDialog({ isOpen, onClose, onConfirm, title, message, loading = false }) {
  return (
    <Modal isOpen={isOpen} onClose={onClose} title={title} size='sm'>
      <div className='space-y-4'>
        <p className='text-gray-600'>{message}</p>
        <div className='flex gap-3 justify-end'>
          <button
            onClick={onClose}
            className='px-4 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50'
          >
            Cancelar
          </button>
          <button
            onClick={onConfirm}
            disabled={loading}
            className='px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700 disabled:opacity-50'
          >
            {loading ? 'Eliminando...' : 'Eliminar'}
          </button>
        </div>
      </div>
    </Modal>
  )
}
