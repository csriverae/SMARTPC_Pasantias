export default function PricingPage() {
  const plans = [
    {
      name: 'Starter',
      price: '$0',
      period: 'Forever free',
      description: 'Perfect for getting started',
      features: [
        '✅ Up to 5 employees',
        '✅ Basic restaurant menu',
        '✅ Order management',
        '✅ Email support',
        '❌ Advanced analytics',
        '❌ API access'
      ],
      cta: 'Get Started',
      highlighted: false
    },
    {
      name: 'Professional',
      price: '$29',
      period: 'per month',
      description: 'Best for growing businesses',
      features: [
        '✅ Unlimited employees',
        '✅ Advanced menu builder',
        '✅ Multi-location support',
        '✅ Priority support',
        '✅ Advanced analytics',
        '❌ API access',
      ],
      cta: 'Start Free Trial',
      highlighted: true
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      period: 'Contact sales',
      description: 'For large organizations',
      features: [
        '✅ Everything in Professional',
        '✅ Full API access',
        '✅ Custom integrations',
        '✅ Dedicated account manager',
        '✅ 24/7 phone support',
        '✅ SLA guarantee'
      ],
      cta: 'Contact Sales',
      highlighted: false
    }
  ]

  return (
    <div className='min-h-screen p-6'>
      <div className='max-w-5xl mx-auto'>
        {/* Header */}
        <div className='text-center mb-12'>
          <h1 className='text-4xl font-bold text-slate-900 mb-4'>Simple, Transparent Pricing</h1>
          <p className='text-xl text-slate-600'>Choose the perfect plan for your restaurant business</p>
        </div>

        {/* Billing Toggle */}
        <div className='flex justify-center mb-12'>
          <div className='inline-flex bg-slate-200 rounded-lg p-1'>
            <button className='px-6 py-2 bg-white text-slate-900 rounded-md font-medium shadow-sm'>
              Monthly
            </button>
            <button className='px-6 py-2 text-slate-700 font-medium'>
              Yearly
              <span className='ml-2 bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full ml-2'>
                Save 20%
              </span>
            </button>
          </div>
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

        {/* FAQ Section */}
        <div className='bg-slate-50 rounded-lg p-8 border border-slate-200'>
          <h2 className='text-2xl font-bold text-slate-900 mb-6'>Frequently Asked Questions</h2>
          <div className='space-y-4'>
            <details className='border-b border-slate-200 pb-4'>
              <summary className='font-medium text-slate-900 cursor-pointer hover:text-indigo-600'>
                Can I change plans anytime?
              </summary>
              <p className='text-slate-600 mt-2'>
                Yes! You can upgrade or downgrade your plan at any time. Changes take effect on your next billing cycle.
              </p>
            </details>
            <details className='border-b border-slate-200 pb-4'>
              <summary className='font-medium text-slate-900 cursor-pointer hover:text-indigo-600'>
                Is there a free trial?
              </summary>
              <p className='text-slate-600 mt-2'>
                Yes, all paid plans come with a 14-day free trial. No credit card required.
              </p>
            </details>
          </div>
        </div>
      </div>
    </div>
  )
}
