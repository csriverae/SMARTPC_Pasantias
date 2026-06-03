'use client'

interface Employee {
  id: string
  full_name: string
  email: string
  phone: string
  qr_token: string
}

interface EmployeesListProps {
  employees: Employee[]
  onCreateClick: () => void
  isLoading?: boolean
}

export default function EmployeesList({ employees, onCreateClick, isLoading }: EmployeesListProps) {
  if (isLoading) {
    return (
      <div className='bg-white border border-slate-200 rounded-xl p-6'>
        <div className='animate-pulse space-y-4'>
          <div className='h-4 bg-slate-200 rounded w-1/4'></div>
          <div className='h-12 bg-slate-100 rounded'></div>
          <div className='h-12 bg-slate-100 rounded'></div>
        </div>
      </div>
    )
  }

  return (
    <div className='bg-white border border-slate-200 rounded-xl p-6'>
      <div className='flex items-center justify-between mb-4'>
        <h2 className='text-xl font-semibold text-slate-900'>Empleados</h2>
        <button
          onClick={onCreateClick}
          className='px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm font-medium transition-colors'
        >
          + Crear Empleado
        </button>
      </div>

      {employees.length === 0 ? (
        <div className='text-center py-12'>
          <p className='text-slate-500'>No hay empleados registrados</p>
          <p className='text-sm text-slate-400 mt-1'>Crea tu primer empleado para comenzar</p>
        </div>
      ) : (
        <div className='overflow-x-auto'>
          <table className='w-full text-sm'>
            <thead className='bg-slate-50 border-b border-slate-200'>
              <tr>
                <th className='text-left p-3 font-semibold text-slate-900'>Nombre</th>
                <th className='text-left p-3 font-semibold text-slate-900'>Email</th>
                <th className='text-left p-3 font-semibold text-slate-900'>Teléfono</th>
                <th className='text-left p-3 font-semibold text-slate-900'>QR Token</th>
              </tr>
            </thead>
            <tbody>
              {employees.map(emp => (
                <tr key={emp.id} className='border-t border-slate-200 hover:bg-slate-50'>
                  <td className='p-3 text-slate-900 font-medium'>{emp.full_name}</td>
                  <td className='p-3 text-slate-900'>{emp.email}</td>
                  <td className='p-3 text-slate-600'>{emp.phone || '—'}</td>
                  <td className='p-3'>
                    <code className='text-xs bg-slate-100 px-2 py-1 rounded text-slate-600'>
                      {emp.qr_token?.substring(0, 16)}...
                    </code>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
