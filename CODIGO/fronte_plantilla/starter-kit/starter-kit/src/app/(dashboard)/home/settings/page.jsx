'use client'

import { useState, useEffect } from 'react'
import { useAuthUser } from '@core/hooks/useAuthUser'
import { LoadingSpinner } from '@components/dashboard/Loaders'
import { ErrorMessage } from '@components/dashboard/ErrorMessage'
import { RoleBadge } from '@components/dashboard/RoleBadge'
import Typography from '@mui/material/Typography'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardHeader from '@mui/material/CardHeader'
import Grid from '@mui/material/Grid'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'

export default function SettingsPage() {
  const { user, loading, error } = useAuthUser()
  const [settings, setSettings] = useState({
    notifications: true,
    theme: 'light',
    language: 'es'
  })
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    if (user) {
      // Load user settings from API
      loadSettings()
    }
  }, [user])

  const loadSettings = async () => {
    try {
      const token = localStorage.getItem('access_token')
      const response = await fetch('http://localhost:8000/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const userData = await response.json()
        // For now, use default settings
        setSettings({
          notifications: true,
          theme: 'light',
          language: 'es'
        })
      }
    } catch (err) {
      console.error('Error loading settings:', err)
    }
  }

  const handleSaveSettings = async () => {
    setSaving(true)
    setMessage('')

    try {
      // Here you would save settings to API
      setMessage('Settings saved successfully!')
      setTimeout(() => setMessage(''), 3000)
    } catch (err) {
      setMessage('Error saving settings')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage message={error} />
  if (!user) return <ErrorMessage message="User not found" />

  return (
    <div className="py-6 px-6 sm:px-8">
      <div className="mb-6">
        <Typography variant="h4" className="font-bold text-slate-900 mb-2">
          Settings
        </Typography>
        <Typography variant="body1" className="text-slate-600">
          Manage your account settings and preferences
        </Typography>
      </div>

      {message && (
        <Alert severity={message.includes('Error') ? 'error' : 'success'} className="mb-6">
          {message}
        </Alert>
      )}

      <Grid container spacing={4}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardHeader title="Account Information" />
            <CardContent>
              <Box className="space-y-4">
                <TextField
                  fullWidth
                  label="Full Name"
                  value={user.full_name || ''}
                  InputProps={{ readOnly: true }}
                />
                <TextField
                  fullWidth
                  label="Email"
                  value={user.email || ''}
                  InputProps={{ readOnly: true }}
                />
                <TextField
                  fullWidth
                  label="Role"
                  value={<RoleBadge role={user.role} />}
                  InputProps={{ readOnly: true }}
                />
              </Box>
            </CardContent>
          </Card>

          <Card className="mt-6">
            <CardHeader title="Preferences" />
            <CardContent>
              <Box className="space-y-4">
                <TextField
                  select
                  fullWidth
                  label="Theme"
                  value={settings.theme}
                  onChange={(e) => setSettings({...settings, theme: e.target.value})}
                  SelectProps={{ native: true }}
                >
                  <option value="light">Light</option>
                  <option value="dark">Dark</option>
                  <option value="auto">Auto</option>
                </TextField>

                <TextField
                  select
                  fullWidth
                  label="Language"
                  value={settings.language}
                  onChange={(e) => setSettings({...settings, language: e.target.value})}
                  SelectProps={{ native: true }}
                >
                  <option value="es">Español</option>
                  <option value="en">English</option>
                </TextField>

                <Button
                  variant="contained"
                  onClick={handleSaveSettings}
                  disabled={saving}
                >
                  {saving ? 'Saving...' : 'Save Settings'}
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader title="Security" />
            <CardContent>
              <Typography variant="body2" className="text-slate-600 mb-4">
                Keep your account secure by regularly updating your password.
              </Typography>
              <Button variant="outlined" fullWidth>
                Change Password
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  )
}