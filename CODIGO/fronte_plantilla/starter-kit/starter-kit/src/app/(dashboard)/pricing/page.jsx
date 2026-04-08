export default function Page() {
  const plans = [
    {
      name: 'Básico',
      price: 'Gratis',
      period: 'Siempre',
      description: 'Para comenzar tu gestión de comidas',
      features: [
        '✅ Hasta 20 empleados',
        '✅ Gestión de acuerdos básica',
        '✅ Registros de consumo',
        '✅ Soporte por email',
        '❌ Reportes avanzados',
        '❌ Múltiples ubicaciones'
      ],
      cta: 'Empezar ahora',
      highlighted: false
    },
    {
      name: 'Profesional',
      price: '$99',
      period: 'por mes',
      description: 'Para restaurantes en crecimiento',
      features: [
        '✅ Hasta 200 empleados',
        '✅ Gestión completa de acuerdos',
        '✅ QR para empleados',
        '✅ Reportes de consumo',
        '✅ Soporte prioritario',
        '✅ Múltiples ubicaciones',
      ],
      cta: 'Comenzar prueba gratis',
      highlighted: true
    },
    {
      name: 'Empresarial',
      price: 'Personalizado',
      period: 'Contacta ventas',
      description: 'Para cadenas de restaurantes',
      features: [
        '✅ Empleados ilimitados',
        '✅ Todo de Profesional',
        '✅ API de integración',
        '✅ Soporte 24/7',
        '✅ Capacitación dedicada',
        '✅ SLA garantizado'
      ],
      cta: 'Contactar ventas',
      highlighted: false
    }
  ]

  return (
    <div className='min-h-screen p-6'>
      <div className='max-w-full'>
        {/* Header */}
        <div className='text-center mb-12'>
          <h1 className='text-4xl font-bold text-slate-900 mb-4'>Planes de MesaPass</h1>
          <p className='text-xl text-slate-600'>Elige el plan perfecto para tu negocio de comidas</p>
        </div>

        {/* Pricing Cards */}
        <div className='grid grid-cols-1 md:grid-cols-3 gap-8 mb-12'>
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`rounded-lg transition-all ${
                plan.highlighted
                  ? 'bg-indigo-600 text-white shadow-xl scale-105'
                  : 'bg-white border border-slate-200 shadow-md hover:shadow-lg'
              }`}
            >
              <div className='p-8'>
                <h3 className={`text-2xl font-bold mb-2 ${plan.highlighted ? 'text-white' : 'text-slate-900'}`}>
                  {plan.name}
                </h3>
                <p className={`text-sm mb-4 ${plan.highlighted ? 'text-indigo-100' : 'text-slate-600'}`}>
                  {plan.description}
                </p>

                {/* Price */}
                <div className='mb-6'>
                  <span className={`text-4xl font-bold ${plan.highlighted ? 'text-white' : 'text-slate-900'}`}>
                    {plan.price}
                  </span>
                  <span className={`text-sm ml-2 ${plan.highlighted ? 'text-indigo-100' : 'text-slate-600'}`}>
                    {plan.period}
                  </span>
                </div>

                {/* CTA Button */}
                <button
                  className={`w-full py-2 px-4 rounded-lg font-medium mb-6 transition-colors ${
                    plan.highlighted
                      ? 'bg-white text-indigo-600 hover:bg-indigo-50'
                      : 'bg-indigo-600 text-white hover:bg-indigo-700'
                  }`}
                >
                  {plan.cta}
                </button>

                {/* Features */}
                <ul className='space-y-3'>
                  {plan.features.map((feature) => (
                    <li
                      key={feature}
                      className={`text-sm ${plan.highlighted ? 'text-indigo-100' : 'text-slate-600'}`}
                    >
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>

        {/* Features Section */}
        <div className='bg-slate-50 rounded-lg p-8 border border-slate-200'>
          <h2 className='text-2xl font-bold text-slate-900 mb-6'>Características en todos los planes</h2>
          <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6'>
            <div className='bg-white rounded-lg p-6 border border-slate-200'>
              <p className='text-2xl mb-2'>👤</p>
              <h3 className='font-semibold text-slate-900 mb-2'>Gestión de Empleados</h3>
              <p className='text-sm text-slate-600'>Administra tu equipo con IDs y códigos QR únicos</p>
            </div>
            <div className='bg-white rounded-lg p-6 border border-slate-200'>
              <p className='text-2xl mb-2'>📋</p>
              <h3 className='font-semibold text-slate-900 mb-2'>Acuerdos</h3>
              <p className='text-sm text-slate-600'>Crea y gestiona acuerdos con restaurantes</p>
            </div>
            <div className='bg-white rounded-lg p-6 border border-slate-200'>
              <p className='text-2xl mb-2'>🥘</p>
              <h3 className='font-semibold text-slate-900 mb-2'>Registros de Consumo</h3>
              <p className='text-sm text-slate-600'>Válida consumos a través de códigos QR</p>
            </div>
            <div className='bg-white rounded-lg p-6 border border-slate-200'>
              <p className='text-2xl mb-2'>📊</p>
              <h3 className='font-semibold text-slate-900 mb-2'>Reportes</h3>
              <p className='text-sm text-slate-600'>Análisis detallados de consumo y facturación</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
