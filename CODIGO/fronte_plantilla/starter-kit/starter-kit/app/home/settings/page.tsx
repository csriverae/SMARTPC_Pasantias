'use client'

import { useAuthUser } from '@core/hooks/useAuthUser'
import { LoadingSpinner } from '@components/dashboard/Loaders'
import { ErrorMessage } from '@components/dashboard/ErrorMessage'
import { useState } from 'react'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import Typography from '@mui/material/Typography'
import Alert from '@mui/material/Alert'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardHeader from '@mui/material/CardHeader'
import Divider from '@mui/material/Divider'

export default function SettingsPage() {
  const { user, loading, error } = useAuthUser()
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [passwordMessage, setPasswordMessage] = useState('')
  const [passwordError, setPasswordError] = useState('')
  const [passwordLoading, setPasswordLoading] = useState(false)

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage title="Error Loading Settings" message={error} />
  if (!user) return <ErrorMessage title="Not Authenticated" message="Please login first" />

  const handleChangePassword = async (e) => {
    e.preventDefault()
    setPasswordMessage('')
    setPasswordError('')

    // Validate
    if (!currentPassword.trim()) {
      setPasswordError('Current password is required')
      return
    }
    if (!newPassword.trim()) {
      setPasswordError('New password is required')
      return
    }
    if (newPassword.length < 6) {
      setPasswordError('Password must be at least 6 characters')
      return
    }
    if (newPassword !== confirmPassword) {
      setPasswordError('Passwords do not match')
      return
    }

    setPasswordLoading(true)

    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:8000/auth/change-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
          confirm_password: confirmPassword
        })
      })

      if (response.ok) {
        setPasswordMessage('✓ Password changed successfully')
        setCurrentPassword('')
        setNewPassword('')
        setConfirmPassword('')
      } else {
        const errorData = await response.json()
        setPasswordError(errorData.detail || 'Failed to change password')
      }
    } catch (error) {
      setPasswordError('Error: ' + error.message)
    } finally {
      setPasswordLoading(false)
    }
  }

  return (
    <div className='p-6 max-w-2xl mx-auto'>
      <div className='mb-8'>
        <h1 className='text-4xl font-bold text-slate-900 mb-2'>Settings</h1>
        <p className='text-base text-slate-600'>Manage your account settings, security preferences, and personal information</p>
      </div>

      {/* Change Password Card */}
      <Card className='mb-6'>
        <CardHeader title='Change Password' />
        <Divider />
        <CardContent>
          {passwordMessage && (
            <Alert severity='success' onClose={() => setPasswordMessage('')} className='mb-4'>
              {passwordMessage}
            </Alert>
          )}
          {passwordError && (
            <Alert severity='error' onClose={() => setPasswordError('')} className='mb-4'>
              {passwordError}
            </Alert>
          )}

          <form onSubmit={handleChangePassword} className='space-y-4'>
            <TextField
              fullWidth
              label='Current Password'
              type='password'
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              variant='outlined'
              disabled={passwordLoading}
            />

            <TextField
              fullWidth
              label='New Password'
              type='password'
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              variant='outlined'
              disabled={passwordLoading}
              helperText='Minimum 6 characters'
            />

            <TextField
              fullWidth
              label='Confirm Password'
              type='password'
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              variant='outlined'
              disabled={passwordLoading}
            />

            <Button
              type='submit'
              variant='contained'
              color='primary'
              disabled={passwordLoading}
            >
              {passwordLoading ? 'Updating...' : 'Update Password'}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Notification Settings Card */}
      <Card className='mb-6'>
        <CardHeader title='Notification Settings' />
        <Divider />
        <CardContent>
          <Typography variant='body2' color='textSecondary' className='mb-4'>
            Notification preferences will be added soon
          </Typography>
        </CardContent>
      </Card>

      {/* Privacy Settings Card */}
      <Card>
        <CardHeader title='Privacy & Security' />
        <Divider />
        <CardContent>
          <Typography variant='body2' color='textSecondary'>
            Advanced privacy and security settings coming soon
          </Typography>
        </CardContent>
      </Card>
    </div>
  )
}
