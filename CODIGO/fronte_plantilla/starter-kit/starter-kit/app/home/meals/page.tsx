'use client'

import { useAuthUser } from '@core/hooks/useAuthUser'
import { LoadingSpinner } from '@components/dashboard/Loaders'
import { ErrorMessage } from '@components/dashboard/ErrorMessage'
import Paper from '@mui/material/Paper'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'

export default function MealsPage() {
  const { user, loading, error } = useAuthUser()

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage title="Error" message={error} />
  if (!user) return <ErrorMessage title="Not Authenticated" message="Please login first" />

  return (
    <div className='p-6 max-w-6xl mx-auto'>
      <div className='mb-8'>
        <h1 className='text-4xl font-bold text-slate-900 mb-2'>Meal Logs</h1>
        <p className='text-slate-500'>View and manage your meal logs</p>
      </div>

      <Paper className='p-8 text-center'>
        <Box sx={{ mb: 2 }}>
          <i className='tabler-soup' style={{ fontSize: '3rem', color: '#4CAF50' }}></i>
        </Box>
        <Typography variant='h6' gutterBottom>
          Coming Soon
        </Typography>
        <Typography color='textSecondary'>
          Meal log features will be available soon
        </Typography>
      </Paper>
    </div>
  )
}
