'use client'

import { useAuthUser } from '@core/hooks/useAuthUser'
import { LoadingSpinner } from '@components/dashboard/Loaders'
import { ErrorMessage } from '@components/dashboard/ErrorMessage'
import { RoleBadge } from '@components/dashboard/RoleBadge'

export default function Page() {
  const { user, loading, error } = useAuthUser()

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage title="Error Loading Profile" message={error} />
  if (!user) return <ErrorMessage title="Not Authenticated" message="Please login first" />

  return (
    <div className='p-6 max-w-4xl mx-auto'>
      <div className='mb-8'>
        <h1 className='text-4xl font-bold text-slate-900 mb-2'>My Profile</h1>
        <p className='text-slate-500'>Manage your personal information and account settings</p>
      </div>

      {/* Main Profile Card */}
      <div className='bg-white rounded-lg shadow-md p-8 mb-6'>
        <div className='flex items-start justify-between mb-8'>
          <div className='flex items-center gap-6'>
            {/* Avatar */}
            <div className='w-24 h-24 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center'>
              <span className='text-4xl font-bold text-white'>
                {user.name.charAt(0).toUpperCase()}
              </span>
            </div>
            {/* User Info */}
            <div>
              <h2 className='text-3xl font-bold text-slate-900'>{user.name}</h2>
              <p className='text-slate-600 mb-2'>{user.email}</p>
              <div className='mt-3'>
                <RoleBadge role={user.role} />
              </div>
            </div>
          </div>
        </div>

        {/* User Details Grid */}
        <div className='grid grid-cols-1 md:grid-cols-2 gap-6 pt-6 border-t border-slate-200'>
          <div>
            <label className='block text-sm font-medium text-slate-700 mb-1'>Full Name</label>
            <p className='text-slate-900 font-medium'>{user.full_name}</p>
          </div>
          <div>
            <label className='block text-sm font-medium text-slate-700 mb-1'>Email Address</label>
            <p className='text-slate-900 font-medium'>{user.email}</p>
          </div>
          <div>
            <label className='block text-sm font-medium text-slate-700 mb-1'>Role</label>
            <p className='text-slate-900 font-medium capitalize'>{user.role}</p>
          </div>
          <div>
            <label className='block text-sm font-medium text-slate-700 mb-1'>Status</label>
            <div className='flex items-center gap-2'>
              <span className='w-3 h-3 bg-green-500 rounded-full'></span>
              <span className='text-slate-900 font-medium'>Active</span>
            </div>
          </div>
        </div>
      </div>

      {/* Account Info Card */}
      <div className='bg-white rounded-lg shadow-md p-6'>
        <h3 className='text-xl font-bold text-slate-900 mb-4'>Account Information</h3>
        <div className='space-y-4'>
          {user.role === 'admin' && (
            <div className='flex items-center p-3 bg-purple-50 border border-purple-200 rounded-lg'>
              <span className='text-lg mr-3'>🔐</span>
              <div>
                <p className='font-medium text-slate-900'>Administrator Access</p>
                <p className='text-sm text-slate-600'>You have full administrative privileges</p>
              </div>
            </div>
          )}
          <div className='flex items-center p-3 bg-blue-50 border border-blue-200 rounded-lg'>
            <span className='text-lg mr-3'>✅</span>
            <div>
              <p className='font-medium text-slate-900'>Email Verified</p>
              <p className='text-sm text-slate-600'>{user.email}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
