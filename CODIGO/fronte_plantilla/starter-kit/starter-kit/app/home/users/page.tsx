'use client'

import { useAuthUser } from '@core/hooks/useAuthUser'
import { LoadingSpinner } from '@components/dashboard/Loaders'
import { ErrorMessage } from '@components/dashboard/ErrorMessage'
import { useState, useEffect } from 'react'
import Box from '@mui/material/Box'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Paper from '@mui/material/Paper'
import Chip from '@mui/material/Chip'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import Alert from '@mui/material/Alert'

export default function UsersPage() {
  const { user, loading: userLoading, error: userError } = useAuthUser()
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!userLoading) {
      if (user?.role !== 'admin') {
        setError('You do not have permission to access this page. Only administrators can view this section.')
        setLoading(false)
        return
      }
      fetchUsers()
    }
  }, [user, userLoading])

  const fetchUsers = async () => {
    try {
      setLoading(true)
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:8000/auth/users', {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        const data = await response.json()
        setUsers(Array.isArray(data.data) ? data.data : [])
        setError('')
      } else if (response.status === 403) {
        setError('Access Denied: Only admins can view users')
      } else {
        setError('Failed to fetch users')
      }
    } catch (err) {
      console.error('Fetch error:', err)
      setError('Error fetching users: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const getRoleColor = (role) => {
    const colors = {
      admin: 'error',
      restaurant_admin: 'warning',
      company_admin: 'info',
      employee: 'success'
    }
    return colors[role] || 'default'
  }

  if (userLoading) return <LoadingSpinner />
  if (userError) return <ErrorMessage title="Error Loading Profile" message={userError} />
  if (user?.role !== 'admin') return <ErrorMessage title="Access Denied" message="Only administrators can access the Users Management section" />
  
  if (loading) {
    return (
      <div className='p-6'>
        <LoadingSpinner />
      </div>
    )
  }

  return (
    <div className='p-6 lg:p-8 max-w-7xl mx-auto'>
      {/* Header */}
      <div className='mb-8'>
        <h1 className='text-4xl font-bold text-slate-900 mb-2'>Users Management</h1>
        <p className='text-slate-600'>Manage all system users, view their roles, and handle permissions</p>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert severity='error' onClose={() => setError('')} className='mb-6' sx={{ backgroundColor: '#fee', borderColor: '#fcc' }}>
          <Typography variant='body2' sx={{ color: '#c33' }}>
            <strong>Error:</strong> {error}
          </Typography>
        </Alert>
      )}

      {/* No Users Found */}
      {!error && users.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center', backgroundColor: '#f9fafb', border: '1px solid #e5e7eb' }}>
          <i className='tabler-users' style={{ fontSize: '3rem', color: '#9ca3af', marginBottom: '1rem', display: 'block' }}></i>
          <Typography variant='h6' sx={{ color: '#6b7280', fontWeight: 600 }}>
            No users found
          </Typography>
          <Typography variant='body2' sx={{ color: '#9ca3af', mt: 1 }}>
            The system currently has no registered users
          </Typography>
        </Paper>
      ) : (
        <Paper sx={{ boxShadow: 2, borderRadius: 2, overflow: 'hidden' }}>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow sx={{ backgroundColor: '#f3f4f6', borderBottom: '2px solid #e5e7eb' }}>
                  <TableCell sx={{ fontWeight: '700', color: '#374151', textTransform: 'uppercase', fontSize: '0.75rem', letterSpacing: '0.5px' }}>ID</TableCell>
                  <TableCell sx={{ fontWeight: '700', color: '#374151', textTransform: 'uppercase', fontSize: '0.75rem', letterSpacing: '0.5px' }}>Email</TableCell>
                  <TableCell sx={{ fontWeight: '700', color: '#374151', textTransform: 'uppercase', fontSize: '0.75rem', letterSpacing: '0.5px' }}>Full Name</TableCell>
                  <TableCell sx={{ fontWeight: '700', color: '#374151', textTransform: 'uppercase', fontSize: '0.75rem', letterSpacing: '0.5px' }}>Role</TableCell>
                  <TableCell sx={{ fontWeight: '700', color: '#374151', textTransform: 'uppercase', fontSize: '0.75rem', letterSpacing: '0.5px' }}>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {users.map((u, idx) => (
                  <TableRow key={u.id} hover sx={{
                    '&:hover': { backgroundColor: '#f9fafb' },
                    borderBottom: '1px solid #e5e7eb',
                    '&:last-child td, &:last-child th': { border: 0 }
                  }}>
                    <TableCell sx={{ color: '#6b7280', fontWeight: 500 }}>#{u.id}</TableCell>
                    <TableCell sx={{ color: '#1f2937', fontWeight: 500 }}>{u.email}</TableCell>
                    <TableCell sx={{ color: '#374151' }}>{u.full_name || '—'}</TableCell>
                    <TableCell>
                      <Chip
                        label={u.role?.replace(/_/g, ' ').toUpperCase()}
                        color={getRoleColor(u.role)}
                        size='small'
                        sx={{ fontWeight: 600 }}
                      />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', gap: 1 }}>
                        <Button size='small' variant='outlined' color='primary' sx={{ textTransform: 'none' }}>
                          Edit
                        </Button>
                        <Button size='small' variant='outlined' color='error' sx={{ textTransform: 'none' }}>
                          Delete
                        </Button>
                      </Box>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      )}

      {/* Stats Footer */}
      {!error && users.length > 0 && (
        <div className='mt-6 grid grid-cols-2 md:grid-cols-4 gap-4'>
          <div className='bg-blue-50 border border-blue-200 rounded-lg p-4'>
            <Typography variant='caption' sx={{ color: '#6b7280', textTransform: 'uppercase' }}>Total Users</Typography>
            <Typography variant='h5' sx={{ color: '#1f2937', fontWeight: 'bold', mt: 1 }}>{users.length}</Typography>
          </div>
          <div className='bg-red-50 border border-red-200 rounded-lg p-4'>
            <Typography variant='caption' sx={{ color: '#6b7280', textTransform: 'uppercase' }}>Admins</Typography>
            <Typography variant='h5' sx={{ color: '#1f2937', fontWeight: 'bold', mt: 1 }}>{users.filter(u => u.role === 'admin').length}</Typography>
          </div>
          <div className='bg-green-50 border border-green-200 rounded-lg p-4'>
            <Typography variant='caption' sx={{ color: '#6b7280', textTransform: 'uppercase' }}>Employees</Typography>
            <Typography variant='h5' sx={{ color: '#1f2937', fontWeight: 'bold', mt: 1 }}>{users.filter(u => u.role === 'employee').length}</Typography>
          </div>
          <div className='bg-amber-50 border border-amber-200 rounded-lg p-4'>
            <Typography variant='caption' sx={{ color: '#6b7280', textTransform: 'uppercase' }}>Other Roles</Typography>
            <Typography variant='h5' sx={{ color: '#1f2937', fontWeight: 'bold', mt: 1 }}>{users.filter(u => u.role !== 'admin' && u.role !== 'employee').length}</Typography>
          </div>
        </div>
      )}
    </div>
  )
}
