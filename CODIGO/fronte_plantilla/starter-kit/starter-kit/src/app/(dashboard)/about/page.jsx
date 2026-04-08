export default function Page() {
  return (
    <div className='p-6 max-w-4xl mx-auto'>
      <div className='mb-8'>
        <h1 className='text-4xl font-bold text-slate-900 mb-2'>Acerca de MesaPass</h1>
        <p className='text-slate-500'>Sistema integral de gestión de alimentación para empresas y restaurantes</p>
      </div>

      <div className='grid grid-cols-1 md:grid-cols-2 gap-8'>
        <div className='bg-white rounded-lg shadow-md p-6'>
          <h2 className='text-2xl font-semibold text-slate-900 mb-4'>¿Qué es MesaPass?</h2>
          <p className='text-slate-600 mb-4'>
            MesaPass es una plataforma SaaS multi-tenant diseñada para gestionar sistemas de alimentación
            corporativa. Conecta empresas con restaurantes para ofrecer soluciones de catering eficientes
            y transparentes.
          </p>
          <ul className='space-y-2 text-slate-600'>
            <li>• Gestión de empleados y QR codes</li>
            <li>• Control de consumos y límites diarios</li>
            <li>• Reportes de facturación y consumo</li>
            <li>• Sistema multi-empresa seguro</li>
          </ul>
        </div>

        <div className='bg-white rounded-lg shadow-md p-6'>
          <h2 className='text-2xl font-semibold text-slate-900 mb-4'>Características Principales</h2>
          <div className='space-y-4'>
            <div className='flex items-start gap-3'>
              <span className='text-2xl'>🏢</span>
              <div>
                <h3 className='font-semibold text-slate-900'>Multi-Tenant</h3>
                <p className='text-sm text-slate-600'>Cada empresa tiene su propio espacio aislado</p>
              </div>
            </div>
            <div className='flex items-start gap-3'>
              <span className='text-2xl'>📱</span>
              <div>
                <h3 className='font-semibold text-slate-900'>QR Codes</h3>
                <p className='text-sm text-slate-600'>Validación rápida de consumos</p>
              </div>
            </div>
            <div className='flex items-start gap-3'>
              <span className='text-2xl'>📊</span>
              <div>
                <h3 className='font-semibold text-slate-900'>Reportes</h3>
                <p className='text-sm text-slate-600'>Análisis detallado de consumos y facturación</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className='mt-8 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg p-6 text-white'>
        <h2 className='text-2xl font-bold mb-2'>¡Bienvenido a MesaPass!</h2>
        <p className='text-indigo-100'>
          Gestiona tu sistema de alimentación de manera eficiente y transparente.
          MesaPass te ayuda a controlar consumos, gestionar empleados y generar reportes precisos.
        </p>
      </div>
    </div>
  )
}
