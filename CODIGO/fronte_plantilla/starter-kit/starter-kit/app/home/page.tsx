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
        <h1 className='text-3xl font-bold tracking-tight text-slate-900 mb-5'>Dashboard</h1>
        <p className='text-sm text-slate-500 mb-8'>Bienvenido a Mesapass (fase 1): tu panel principal con datos de ejemplo y diseño Vuexy.</p>

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
              <p className='text-xs text-emerald-500 mt-3'>{item.change} desde la última semana</p>
            </article>
          ))}
        </div>

        <div className='grid gap-4 lg:grid-cols-2'>
          <section className='bg-white border border-slate-200 rounded-xl p-4 shadow-sm'>
            <header className='flex items-center justify-between mb-3'>
              <h2 className='text-lg font-semibold text-slate-900'>Actividad reciente</h2>
              <span className='text-xs text-slate-500'>Últimas 24h</span>
            </header>
            <ul className='space-y-3'>
              <li className='flex justify-between items-center p-2 rounded-md hover:bg-slate-100'>
                <span>Usuario Juan completó un pago</span>
                <span className='text-xs text-slate-500'>15m</span>
              </li>
              <li className='flex justify-between items-center p-2 rounded-md hover:bg-slate-100'>
                <span>Nuevo registro en el portal</span>
                <span className='text-xs text-slate-500'>45m</span>
              </li>
              <li className='flex justify-between items-center p-2 rounded-md hover:bg-slate-100'>
                <span>Reporte de error en API</span>
                <span className='text-xs text-slate-500'>1h</span>
              </li>
            </ul>
          </section>
          <section className='bg-white border border-slate-200 rounded-xl p-4 shadow-sm'>
            <header className='flex items-center justify-between mb-3'>
              <h2 className='text-lg font-semibold text-slate-900'>Tareas pendientes</h2>
              <span className='text-xs text-slate-500'>Progreso</span>
            </header>
            <ul className='space-y-3'>
              <li>
                <p className='text-sm text-slate-700 mb-1'>Integrar login con PostgreSQL</p>
                <div className='h-2 rounded-full bg-slate-100 overflow-hidden'>
                  <div className='h-full w-1/4 bg-indigo-500' />
                </div>
              </li>
              <li>
                <p className='text-sm text-slate-700 mb-1'>Crear tablas de usuario y sesión</p>
                <div className='h-2 rounded-full bg-slate-100 overflow-hidden'>
                  <div className='h-full w-1/3 bg-indigo-500' />
                </div>
              </li>
              <li>
                <p className='text-sm text-slate-700 mb-1'>Validación de frontend en fase 1</p>
                <div className='h-2 rounded-full bg-slate-100 overflow-hidden'>
                  <div className='h-full w-2/3 bg-indigo-500' />
                </div>
              </li>
            </ul>
          </section>
        </div>
      </div>
    </Fragment>
  )
}