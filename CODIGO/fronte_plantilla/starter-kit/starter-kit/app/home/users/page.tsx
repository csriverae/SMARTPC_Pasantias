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
    if (user?.role !== 'admin') {
      setError('You do not have permission to access this page')
      setLoading(false)
      return
    }

    fetchUsers()
  }, [user])

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:8000/auth/users', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        setUsers(data.data || [])
      } else {
        setError('Failed to fetch users')
      }
    } catch (err) {
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
  if (userError) return <ErrorMessage title="Error" message={userError} />
  if (user?.role !== 'admin') return <ErrorMessage title="Access Denied" message="Only admins can access this page" />
  if (loading) return <LoadingSpinner />

  return (
    <div className='p-6 max-w-6xl mx-auto'>
      <div className='mb-8'>
        <h1 className='text-4xl font-bold text-slate-900 mb-2'>Users Management</h1>
        <p className='text-slate-500'>Manage all system users and their roles</p>
      </div>

      {error && (
        <Alert severity='error' onClose={() => setError('')} className='mb-4'>
          {error}
        </Alert>
      )}

      {users.length === 0 ? (
        <Paper className='p-6'>
          <Typography color='textSecondary' align='center'>
            No users found
          </Typography>
        </Paper>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow sx={{ bgcolor: 'primary.light' }}>
                <TableCell sx={{ fontWeight: 'bold' }}>ID</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Email</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Full Name</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Role</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {users.map(u => (
                <TableRow key={u.id} hover>
                  <TableCell>#{u.id}</TableCell>
                  <TableCell>{u.email}</TableCell>
                  <TableCell>{u.full_name || 'N/A'}</TableCell>
                  <TableCell>
                    <Chip
                      label={u.role}
                      color={getRoleColor(u.role)}
                      size='small'
                    />
                  </TableCell>
                  <TableCell>
                    <Button size='small' variant='outlined' color='error'>
                      Delete
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </div>
  )
}
