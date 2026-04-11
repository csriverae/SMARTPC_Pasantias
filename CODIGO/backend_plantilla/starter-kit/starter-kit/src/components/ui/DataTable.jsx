'use client'

import { useState } from 'react'

export default function DataTable({
  columns,
  data,
  loading = false,
  error = null,
  onDelete = null,
  onEdit = null,
  emptyMessage = 'No hay datos disponibles'
}) {
  const [selectedIds, setSelectedIds] = useState(new Set())

  const toggleSelectAll = (e) => {
    if (e.target.checked) {
      setSelectedIds(new Set(data.map(item => item.id)))
    } else {
      setSelectedIds(new Set())
    }
  }

  const toggleSelect = (id, e) => {
    e.stopPropagation()
    const newSelected = new Set(selectedIds)
    if (newSelected.has(id)) {
      newSelected.delete(id)
    } else {
      newSelected.add(id)
    }
    setSelectedIds(newSelected)
  }

  if (loading) {
    return (
      <div className='flex justify-center items-center py-12'>
        <div className='text-center'>
          <div className='inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600'></div>
          <p className='mt-4 text-gray-600'>Cargando datos...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className='bg-red-50 border-l-4 border-red-500 p-4'>
        <p className='text-red-700'>{error}</p>
      </div>
    )
  }

  if (data.length === 0) {
    return (
      <div className='text-center py-12'>
        <div className='text-gray-400 text-4xl mb-2'>📋</div>
        <p className='text-gray-600'>{emptyMessage}</p>
      </div>
    )
  }

  return (
    <div className='overflow-x-auto'>
      <table className='w-full'>
        <thead className='bg-gray-50 border-b border-gray-200'>
          <tr>
            {columns.map(col => (
              <th
                key={col.key}
                className='px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider'
              >
                {col.label}
              </th>
            ))}
            {(onEdit || onDelete) && (
              <th className='px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider'>
                Acciones
              </th>
            )}
          </tr>
        </thead>
        <tbody className='divide-y divide-gray-200'>
          {data.map(item => (
            <tr key={item.id} className='hover:bg-gray-50 transition-colors'>
              {columns.map(col => (
                <td key={col.key} className='px-6 py-4 whitespace-nowrap text-sm text-gray-900'>
                  {col.render ? col.render(item[col.key], item) : item[col.key]}
                </td>
              ))}
              {(onEdit || onDelete) && (
                <td className='px-6 py-4 whitespace-nowrap text-sm'>
                  <div className='flex gap-2'>
                    {onEdit && (
                      <button
                        onClick={() => onEdit(item)}
                        className='text-indigo-600 hover:text-indigo-900 font-medium'
                      >
                        Editar
                      </button>
                    )}
                    {onDelete && (
                      <button
                        onClick={() => onDelete(item)}
                        className='text-red-600 hover:text-red-900 font-medium'
                      >
                        Eliminar
                      </button>
                    )}
                  </div>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
