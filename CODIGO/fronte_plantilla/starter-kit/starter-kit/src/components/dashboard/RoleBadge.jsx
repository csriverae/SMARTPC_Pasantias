export const RoleBadge = ({ role }) => {
  const colors = {
    admin: 'bg-red-100 text-red-800',
    user: 'bg-blue-100 text-blue-800',
    default: 'bg-gray-100 text-gray-800'
  }

  return (
    <span className={`px-2 py-1 text-xs font-medium rounded-full ${colors[role] || colors.default}`}>
      {role}
    </span>
  )
}