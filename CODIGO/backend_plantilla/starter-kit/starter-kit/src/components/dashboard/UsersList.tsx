'use client'

interface User {
  user_id: string
  email: string
  full_name: string
  role: string
}

interface UsersListProps {
  users: User[]
  onInviteClick: () => void
  isLoading?: boolean
}

export default function UsersList({ users, onInviteClick, isLoading }: UsersListProps) {
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
        <h2 className='text-xl font-semibold text-slate-900'>Usuarios del Tenant</h2>
        <button
          onClick={onInviteClick}
          className='px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm font-medium transition-colors'
        >
          + Invitar Usuario
        </button>
      </div>

      {users.length === 0 ? (
        <div className='text-center py-12'>
          <p className='text-slate-500'>No hay usuarios registrados</p>
          <p className='text-sm text-slate-400 mt-1'>Invita a tu primer usuario para comenzar</p>
        </div>
      ) : (
        <div className='overflow-x-auto'>
          <table className='w-full text-sm'>
            <thead className='bg-slate-50 border-b border-slate-200'>
              <tr>
                <th className='text-left p-3 font-semibold text-slate-900'>Email</th>
                <th className='text-left p-3 font-semibold text-slate-900'>Nombre</th>
                <th className='text-left p-3 font-semibold text-slate-900'>Rol</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user, idx) => (
                <tr key={user.email || `user-${idx}`} className='border-t border-slate-200 hover:bg-slate-50'>
                  <td className='p-3 text-slate-900'>{user.email}</td>
                  <td className='p-3 text-slate-900'>{user.full_name}</td>
                  <td className='p-3'>
                    <span className='px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs font-medium capitalize'>
                      {user.role}
                    </span>
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
