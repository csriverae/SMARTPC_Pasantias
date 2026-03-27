'use client'

import { useState } from 'react'
import { useAuthUser } from '@core/hooks/useAuthUser'
import { LoadingSpinner } from '@components/dashboard/Loaders'
import { ErrorMessage } from '@components/dashboard/ErrorMessage'
import { RoleBadge } from '@components/dashboard/RoleBadge'

export default function SettingsPage() {
  const { user, loading, error } = useAuthUser()
  const [activeTab, setActiveTab] = useState<'account' | 'security' | 'preferences'>('account')

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage title='Error Loading Settings' message={error} />
  if (!user) return <ErrorMessage title='Not Authenticated' message='Please login first' />

  // Password change form state
  const [passwordForm, setPasswordForm] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  })
  const [passwordLoading, setPasswordLoading] = useState(false)
  const [passwordError, setPasswordError] = useState<string | null>(null)
  const [passwordSuccess, setPasswordSuccess] = useState(false)

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault()
    setPasswordError(null)
    setPasswordSuccess(false)

    // Validation
    if (!passwordForm.currentPassword || !passwordForm.newPassword || !passwordForm.confirmPassword) {
      setPasswordError('All fields are required')
      return
    }

    if (passwordForm.newPassword.length < 6) {
      setPasswordError('New password must be at least 6 characters')
      return
    }

    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      setPasswordError('New passwords do not match')
      return
    }

    try {
      setPasswordLoading(true)
      const token = localStorage.getItem('token')
      
      const response = await fetch('http://localhost:8000/auth/change-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          current_password: passwordForm.currentPassword,
          new_password: passwordForm.newPassword,
          confirm_password: passwordForm.confirmPassword,
        }),
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || 'Failed to change password')
      }

      setPasswordSuccess(true)
      setPasswordForm({ currentPassword: '', newPassword: '', confirmPassword: '' })
      setTimeout(() => setPasswordSuccess(false), 5000)
    } catch (err) {
      setPasswordError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setPasswordLoading(false)
    }
  }

  return (
    <div className='p-6 max-w-4xl mx-auto'>
      <div className='mb-8'>
        <h1 className='text-4xl font-bold text-slate-900 mb-2'>Settings</h1>
        <p className='text-slate-500'>Manage your account settings and preferences</p>
      </div>

      {/* Tabs Navigation */}
      <div className='flex gap-2 mb-6 border-b border-slate-200'>
        <button
          onClick={() => setActiveTab('account')}
          className={`px-4 py-2 font-medium border-b-2 transition-colors ${
            activeTab === 'account'
              ? 'border-indigo-600 text-indigo-600'
              : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          👤 Account
        </button>
        <button
          onClick={() => setActiveTab('security')}
          className={`px-4 py-2 font-medium border-b-2 transition-colors ${
            activeTab === 'security'
              ? 'border-indigo-600 text-indigo-600'
              : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          🔐 Security
        </button>
        <button
          onClick={() => setActiveTab('preferences')}
          className={`px-4 py-2 font-medium border-b-2 transition-colors ${
            activeTab === 'preferences'
              ? 'border-indigo-600 text-indigo-600'
              : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          ⚙️ Preferences
        </button>
      </div>

      {/* Account Tab */}
      {activeTab === 'account' && (
        <div className='space-y-6'>
          <div className='bg-white rounded-lg shadow-md p-6'>
            <h2 className='text-2xl font-bold text-slate-900 mb-6'>Account Information</h2>
            
            <form className='space-y-6'>
              <div className='grid grid-cols-1 md:grid-cols-2 gap-6'>
                <div>
                  <label className='block text-sm font-medium text-slate-700 mb-2'>Full Name</label>
                  <input
                    type='text'
                    defaultValue={user.full_name}
                    className='w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500'
                    disabled
                  />
                </div>
                <div>
                  <label className='block text-sm font-medium text-slate-700 mb-2'>Email Address</label>
                  <input
                    type='email'
                    defaultValue={user.email}
                    className='w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500'
                    disabled
                  />
                </div>
              </div>

              <div>
                <label className='block text-sm font-medium text-slate-700 mb-2'>User Role</label>
                <div className='flex items-center gap-2'>
                  <RoleBadge role={user.role} />
                  <span className='text-sm text-slate-600'>(System-assigned)</span>
                </div>
              </div>

              <div className='text-sm text-slate-600 bg-blue-50 p-4 rounded-lg border border-blue-200'>
                📋 Contact your administrator to change account details
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Security Tab */}
      {activeTab === 'security' && (
        <div className='space-y-6'>
          <div className='bg-white rounded-lg shadow-md p-6'>
            <h2 className='text-2xl font-bold text-slate-900 mb-6'>Security Settings</h2>
            
            <div className='space-y-6'>
              {/* Change Password */}
              <div className='border-b border-slate-200 pb-6'>
                <h3 className='text-lg font-semibold text-slate-900 mb-4'>Change Password</h3>
                
                {passwordSuccess && (
                  <div className='mb-4 p-4 bg-green-50 border border-green-200 rounded-lg'>
                    <p className='text-green-800'>✓ Password changed successfully!</p>
                  </div>
                )}
                
                {passwordError && (
                  <div className='mb-4 p-4 bg-red-50 border border-red-200 rounded-lg'>
                    <p className='text-red-800'>✗ {passwordError}</p>
                  </div>
                )}

                <form onSubmit={handlePasswordChange} className='space-y-4'>
                  <div>
                    <label className='block text-sm font-medium text-slate-700 mb-2'>Current Password</label>
                    <input
                      type='password'
                      placeholder='Enter current password'
                      value={passwordForm.currentPassword}
                      onChange={(e) => setPasswordForm({ ...passwordForm, currentPassword: e.target.value })}
                      disabled={passwordLoading}
                      className='w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-slate-100'
                    />
                  </div>
                  <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
                    <div>
                      <label className='block text-sm font-medium text-slate-700 mb-2'>New Password</label>
                      <input
                        type='password'
                        placeholder='Enter new password'
                        value={passwordForm.newPassword}
                        onChange={(e) => setPasswordForm({ ...passwordForm, newPassword: e.target.value })}
                        disabled={passwordLoading}
                        className='w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-slate-100'
                      />
                    </div>
                    <div>
                      <label className='block text-sm font-medium text-slate-700 mb-2'>Confirm Password</label>
                      <input
                        type='password'
                        placeholder='Confirm new password'
                        value={passwordForm.confirmPassword}
                        onChange={(e) => setPasswordForm({ ...passwordForm, confirmPassword: e.target.value })}
                        disabled={passwordLoading}
                        className='w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-slate-100'
                      />
                    </div>
                  </div>
                  <button
                    type='submit'
                    disabled={passwordLoading}
                    className='px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium disabled:bg-slate-400 disabled:cursor-not-allowed'
                  >
                    {passwordLoading ? 'Updating...' : 'Update Password'}
                  </button>
                </form>
              </div>

              {/* Two-Factor Authentication */}
              <div className='border-b border-slate-200 pb-6'>
                <h3 className='text-lg font-semibold text-slate-900 mb-4'>Two-Factor Authentication</h3>
                <div className='flex items-center justify-between'>
                  <div>
                    <p className='text-slate-700'>Add an extra layer of security to your account</p>
                    <p className='text-sm text-slate-600 mt-1'>Not currently enabled</p>
                  </div>
                  <button className='px-6 py-2 border border-indigo-600 text-indigo-600 rounded-lg hover:bg-indigo-50 transition-colors font-medium'>
                    Enable 2FA
                  </button>
                </div>
              </div>

              {/* Active Sessions */}
              <div>
                <h3 className='text-lg font-semibold text-slate-900 mb-4'>Active Sessions</h3>
                <div className='bg-slate-50 border border-slate-200 rounded-lg p-4'>
                  <div className='flex items-center justify-between'>
                    <div>
                      <p className='font-medium text-slate-900'>Current Session</p>
                      <p className='text-sm text-slate-600'>Windows • Chrome • Last active 2 minutes ago</p>
                    </div>
                    <span className='text-green-600 font-medium'>Active</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Preferences Tab */}
      {activeTab === 'preferences' && (
        <div className='space-y-6'>
          <div className='bg-white rounded-lg shadow-md p-6'>
            <h2 className='text-2xl font-bold text-slate-900 mb-6'>Preferences</h2>
            
            <div className='space-y-6'>
              {/* Theme Preferences */}
              <div className='border-b border-slate-200 pb-6'>
                <h3 className='text-lg font-semibold text-slate-900 mb-4'>Appearance</h3>
                <div className='space-y-4'>
                  <div>
                    <label className='block text-sm font-medium text-slate-700 mb-3'>Theme</label>
                    <div className='flex gap-4'>
                      <label className='flex items-center'>
                        <input type='radio' name='theme' defaultChecked className='mr-2' />
                        <span className='text-slate-700'>Light</span>
                      </label>
                      <label className='flex items-center'>
                        <input type='radio' name='theme' className='mr-2' />
                        <span className='text-slate-700'>Dark</span>
                      </label>
                      <label className='flex items-center'>
                        <input type='radio' name='theme' className='mr-2' />
                        <span className='text-slate-700'>System</span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              {/* Notification Preferences */}
              <div className='border-b border-slate-200 pb-6'>
                <h3 className='text-lg font-semibold text-slate-900 mb-4'>Notifications</h3>
                <div className='space-y-3'>
                  <label className='flex items-center p-3 border border-slate-200 rounded-lg cursor-pointer hover:bg-slate-50'>
                    <input type='checkbox' defaultChecked className='mr-3' />
                    <div>
                      <p className='font-medium text-slate-900'>Email Notifications</p>
                      <p className='text-sm text-slate-600'>Receive updates via email</p>
                    </div>
                  </label>
                  <label className='flex items-center p-3 border border-slate-200 rounded-lg cursor-pointer hover:bg-slate-50'>
                    <input type='checkbox' defaultChecked className='mr-3' />
                    <div>
                      <p className='font-medium text-slate-900'>Security Alerts</p>
                      <p className='text-sm text-slate-600'>Get notified of security events</p>
                    </div>
                  </label>
                  <label className='flex items-center p-3 border border-slate-200 rounded-lg cursor-pointer hover:bg-slate-50'>
                    <input type='checkbox' className='mr-3' />
                    <div>
                      <p className='font-medium text-slate-900'>Marketing Emails</p>
                      <p className='text-sm text-slate-600'>Receive product updates and news</p>
                    </div>
                  </label>
                </div>
              </div>

              {/* Admin Settings */}
              {user.role === 'admin' && (
                <div className='pt-6'>
                  <h3 className='text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2'>
                    🔐 <span>Administrator Settings</span>
                  </h3>
                  <div className='bg-purple-50 border border-purple-200 rounded-lg p-4 space-y-3'>
                    <label className='flex items-center cursor-pointer'>
                      <input type='checkbox' defaultChecked className='mr-3' />
                      <span className='text-slate-700'>Enable system logs</span>
                    </label>
                    <label className='flex items-center cursor-pointer'>
                      <input type='checkbox' defaultChecked className='mr-3' />
                      <span className='text-slate-700'>Monitor user activities</span>
                    </label>
                    <label className='flex items-center cursor-pointer'>
                      <input type='checkbox' className='mr-3' />
                      <span className='text-slate-700'>Send admin digests</span>
                    </label>
                  </div>
                </div>
              )}

              <div className='pt-6 flex gap-3'>
                <button className='px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium'>
                  Save Preferences
                </button>
                <button className='px-6 py-2 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition-colors font-medium'>
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
