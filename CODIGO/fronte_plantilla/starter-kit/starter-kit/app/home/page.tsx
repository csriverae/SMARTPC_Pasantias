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
      <div className='py-6 px-6 sm:px-8 max-w-7xl mx-auto'>
        <h1 className='text-4xl font-bold tracking-tight text-slate-900 mb-2'>Dashboard</h1>
        <p className='text-base text-slate-600 mb-8'>Welcome to Mesapass - Your meal pass management platform. Here's an overview of your system's current status.</p>

        {/* Quick Stats */}
        <div className='grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-8'>
          {stats.map(item => (
            <article key={item.label} className='bg-white border border-slate-200 rounded-lg p-5 shadow-sm hover:shadow-md transition-all duration-200'>
              <div className='flex items-center justify-between mb-3'>
                <div>
                  <p className='text-xs font-semibold text-slate-500 uppercase tracking-wide'>{item.label}</p>
                  <p className='text-3xl font-bold text-slate-900 mt-1'>{item.value}</p>
                </div>
                <span className='inline-flex items-center justify-center w-12 h-12 bg-indigo-100 text-indigo-600 rounded-lg'>
                  <i className={`${item.icon} text-xl`}></i>
                </span>
              </div>
              <p className='text-xs font-medium text-emerald-600'>{item.change} last week</p>
            </article>
          ))}
        </div>

        {/* Main Content Grid */}
        <div className='grid gap-5 lg:grid-cols-2 mb-8'>
          <section className='bg-white border border-slate-200 rounded-lg p-5 shadow-sm'>
            <header className='flex items-center justify-between mb-4 pb-3 border-b border-slate-100'>
              <h2 className='text-lg font-semibold text-slate-900'>Recent Activity</h2>
              <span className='text-xs font-medium text-slate-500 bg-slate-100 px-2 py-1 rounded'>Last 24h</span>
            </header>
            <ul className='space-y-3'>
              <li className='flex justify-between items-center p-3 rounded-md hover:bg-slate-50 transition-colors'>
                <span className='text-sm text-slate-700'>User João completed a payment</span>
                <span className='text-xs font-medium text-slate-500'>15m</span>
              </li>
              <li className='flex justify-between items-center p-3 rounded-md hover:bg-slate-50 transition-colors'>
                <span className='text-sm text-slate-700'>New user registration</span>
                <span className='text-xs font-medium text-slate-500'>45m</span>
              </li>
              <li className='flex justify-between items-center p-3 rounded-md hover:bg-slate-50 transition-colors'>
                <span className='text-sm text-slate-700'>System update deployed</span>
                <span className='text-xs font-medium text-slate-500'>1h</span>
              </li>
            </ul>
          </section>

          <section className='bg-white border border-slate-200 rounded-lg p-5 shadow-sm'>
            <header className='flex items-center justify-between mb-4 pb-3 border-b border-slate-100'>
              <h2 className='text-lg font-semibold text-slate-900'>Pending Tasks</h2>
              <span className='text-xs font-medium text-slate-500 bg-slate-100 px-2 py-1 rounded'>Progress</span>
            </header>
            <ul className='space-y-4'>
              <li>
                <p className='text-sm font-medium text-slate-900 mb-2'>Complete profile setup</p>
                <div className='h-2 rounded-full bg-slate-100 overflow-hidden'>
                  <div className='h-full w-1/4 bg-indigo-500 rounded-full'></div>
                </div>
              </li>
              <li>
                <p className='text-sm font-medium text-slate-900 mb-2'>Review system documentation</p>
                <div className='h-2 rounded-full bg-slate-100 overflow-hidden'>
                  <div className='h-full w-1/3 bg-indigo-500 rounded-full'></div>
                </div>
              </li>
              <li>
                <p className='text-sm font-medium text-slate-900 mb-2'>Test all features</p>
                <div className='h-2 rounded-full bg-slate-100 overflow-hidden'>
                  <div className='h-full w-2/3 bg-indigo-500 rounded-full'></div>
                </div>
              </li>
            </ul>
          </section>
        </div>

        {/* Features Section */}
        <div>
          <h3 className='text-lg font-semibold text-slate-900 mb-4'>Available Features</h3>
          <div className='grid grid-cols-1 md:grid-cols-3 gap-4'>
            <div className='bg-gradient-to-br from-blue-50 to-blue-100/50 border border-blue-200/50 rounded-lg p-5 hover:shadow-md transition-shadow'>
              <div className='flex items-center gap-3 mb-3'>
                <span className='inline-flex items-center justify-center w-10 h-10 bg-blue-200 text-blue-700 rounded-lg'>
                  <i className='tabler-user text-lg'></i>
                </span>
                <h4 className='font-semibold text-slate-900'>Profile</h4>
              </div>
              <p className='text-sm text-slate-700'>View and manage your personal information and account settings</p>
            </div>

            <div className='bg-gradient-to-br from-green-50 to-green-100/50 border border-green-200/50 rounded-lg p-5 hover:shadow-md transition-shadow'>
              <div className='flex items-center gap-3 mb-3'>
                <span className='inline-flex items-center justify-center w-10 h-10 bg-green-200 text-green-700 rounded-lg'>
                  <i className='tabler-settings text-lg'></i>
                </span>
                <h4 className='font-semibold text-slate-900'>Settings</h4>
              </div>
              <p className='text-sm text-slate-600'>Update your password and preferences</p>
            </div>

            <div className='bg-gradient-to-br from-purple-50 to-purple-100/50 border border-purple-200/50 rounded-lg p-5 hover:shadow-md transition-shadow'>
              <div className='flex items-center gap-3 mb-3'>
                <span className='inline-flex items-center justify-center w-10 h-10 bg-purple-200 text-purple-700 rounded-lg'>
                  <i className='tabler-lock text-lg'></i>
                </span>
                <h4 className='font-semibold text-slate-900'>Security</h4>
              </div>
              <p className='text-sm text-slate-700'>Manage your account security and session settings</p>
            </div>
          </div>
        </div>
      </div>
    </Fragment>
  )
}