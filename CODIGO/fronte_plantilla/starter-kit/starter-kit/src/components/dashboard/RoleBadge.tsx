export const RoleBadge = ({ role }: { role: 'admin' | 'employee' }) => {
  const isAdmin = role === 'admin'
  return (
    <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
      isAdmin
        ? 'bg-purple-100 text-purple-800'
        : 'bg-blue-100 text-blue-800'
    }`}>
      {isAdmin ? '👨‍💼 Admin' : '👤 Employee'}
    </span>
  )
}
