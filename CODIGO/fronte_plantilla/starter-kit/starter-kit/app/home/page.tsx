import { Fragment } from 'react'

const stats = [
  { label: 'Users', value: '1,280', icon: 'tabler-users', change: '+14%' },
  { label: 'Revenue', value: '$25,400', icon: 'tabler-dollar-sign', change: '+8%' },
  { label: 'Orders', value: '455', icon: 'tabler-shopping-cart', change: '+5%' },
  { label: 'Sessions', value: '7,922', icon: 'tabler-activity', change: '+10%' }
]

export default function Page() {
  return (
    <Fragment>
      <div className='py-6 px-6 sm:px-8'>
        <h1 className='text-3xl font-bold tracking-tight text-slate-900 mb-2'>Dashboard</h1>
        <p className='text-sm text-slate-500 mb-8'>Welcome to Mesapass - Your meal pass management platform</p>

        {/* Quick Stats */}
        <div className='grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6'>
          {stats.map(item => (
            <article key={item.label} className='bg-white border border-slate-200 rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow'>
              <div className='flex items-center justify-between'>
                <div>
                  <p className='text-xs text-slate-400 uppercase tracking-wide'>{item.label}</p>
                  <p className='text-2xl font-semibold text-slate-900'>{item.value}</p>
                </div>
                <span className='inline-flex items-center justify-center w-10 h-10 bg-indigo-100 text-indigo-600 rounded-lg'>
                  <i className={item.icon}></i>
                </span>
              </div>
              <p className='text-xs text-emerald-500 mt-3'>{item.change} last week</p>
            </article>
          ))}
        </div>

        {/* Main Content Grid */}
        <div className='grid gap-4 lg:grid-cols-2'>
          <section className='bg-white border border-slate-200 rounded-xl p-4 shadow-sm'>
            <header className='flex items-center justify-between mb-3'>
              <h2 className='text-lg font-semibold text-slate-900'>Recent Activity</h2>
              <span className='text-xs text-slate-500'>Last 24h</span>
            </header>
            <ul className='space-y-3'>
              <li className='flex justify-between items-center p-2 rounded-md hover:bg-slate-100'>
                <span>User João completed a payment</span>
                <span className='text-xs text-slate-500'>15m</span>
              </li>
              <li className='flex justify-between items-center p-2 rounded-md hover:bg-slate-100'>
                <span>New user registration</span>
                <span className='text-xs text-slate-500'>45m</span>
              </li>
              <li className='flex justify-between items-center p-2 rounded-md hover:bg-slate-100'>
                <span>System update deployed</span>
                <span className='text-xs text-slate-500'>1h</span>
              </li>
            </ul>
          </section>

          <section className='bg-white border border-slate-200 rounded-xl p-4 shadow-sm'>
            <header className='flex items-center justify-between mb-3'>
              <h2 className='text-lg font-semibold text-slate-900'>Pending Tasks</h2>
              <span className='text-xs text-slate-500'>Progress</span>
            </header>
            <ul className='space-y-3'>
              <li>
                <p className='text-sm text-slate-700 mb-1'>Complete profile setup</p>
                <div className='h-2 rounded-full bg-slate-100 overflow-hidden'>
                  <div className='h-full w-1/4 bg-indigo-500' />
                </div>
              </li>
              <li>
                <p className='text-sm text-slate-700 mb-1'>Review system documentation</p>
                <div className='h-2 rounded-full bg-slate-100 overflow-hidden'>
                  <div className='h-full w-1/3 bg-indigo-500' />
                </div>
              </li>
              <li>
                <p className='text-sm text-slate-700 mb-1'>Test all features</p>
                <div className='h-2 rounded-full bg-slate-100 overflow-hidden'>
                  <div className='h-full w-2/3 bg-indigo-500' />
                </div>
              </li>
            </ul>
          </section>
        </div>

        {/* Features Section */}
        <div className='mt-8'>
          <h3 className='text-lg font-semibold text-slate-900 mb-4'>Available Features</h3>
          <div className='grid grid-cols-1 md:grid-cols-3 gap-4'>
            <div className='bg-gradient-to-br from-blue-50 to-blue-100 border border-blue-200 rounded-xl p-4'>
              <div className='flex items-center gap-2 mb-2'>
                <i className='tabler-user text-blue-600' style={{ fontSize: '1.5rem' }}></i>
                <h4 className='font-semibold text-slate-900'>Profile</h4>
              </div>
              <p className='text-sm text-slate-600'>View and manage your personal information</p>
            </div>

            <div className='bg-gradient-to-br from-green-50 to-green-100 border border-green-200 rounded-xl p-4'>
              <div className='flex items-center gap-2 mb-2'>
                <i className='tabler-settings text-green-600' style={{ fontSize: '1.5rem' }}></i>
                <h4 className='font-semibold text-slate-900'>Settings</h4>
              </div>
              <p className='text-sm text-slate-600'>Update your password and preferences</p>
            </div>

            <div className='bg-gradient-to-br from-purple-50 to-purple-100 border border-purple-200 rounded-xl p-4'>
              <div className='flex items-center gap-2 mb-2'>
                <i className='tabler-lock text-purple-600' style={{ fontSize: '1.5rem' }}></i>
                <h4 className='font-semibold text-slate-900'>Security</h4>
              </div>
              <p className='text-sm text-slate-600'>Manage your account security settings</p>
            </div>
          </div>
        </div>
      </div>
    </Fragment>
  )
}