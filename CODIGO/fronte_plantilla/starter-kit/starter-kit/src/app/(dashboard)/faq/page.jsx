'use client'

import { useState } from 'react'

export default function Page() {
  const [openIndex, setOpenIndex] = useState(null)

  const faqs = [
    {
      category: 'General',
      questions: [
        {
          q: '¿Qué es Mesapass?',
          a: 'Mesapass es una plataforma integral de gestión de restaurantes que te ayuda a administrar empleados, crear menús, gestionar órdenes y mucho más.'
        },
        {
          q: '¿Cómo puedo empezar?',
          a: 'Puedes crear una cuenta gratuita en nuestra página principal. El plan Starter es perfecto para comenzar sin costo.'
        },
        {
          q: '¿Necesito tarjeta de crédito para probar?',
          a: 'No, puedes probar Mesapass completamente gratis durante 14 días sin proporcionar tu información de pago.'
        }
      ]
    },
    {
      category: 'Operaciones',
      questions: [
        {
          q: '¿Cómo agrego empleados a mi restaurante?',
          a: 'Ve a la sección de Empleados, haz clic en "Agregar Empleado" e ingresa su información. Ellos recibirán un enlace de invitación por correo electrónico.'
        },
        {
          q: '¿Puedo tener múltiples ubicaciones?',
          a: 'Sí, nuestro plan Professional incluye soporte para múltiples ubicaciones. Cada ubicación puede tener su propio menú y empleados.'
        },
        {
          q: '¿Cómo funciona la gestión de órdenes?',
          a: 'Los clientes pueden realizar órdenes a través del sistema. Tu equipo recibe notificaciones en tiempo real y puede rastrear el estado.'
        }
      ]
    },
    {
      category: 'Seguridad y Datos',
      questions: [
        {
          q: '¿Mis datos están seguros?',
          a: 'Sí, usamos encriptación de nivel empresarial (SSL/TLS) y cumplimos con estándares de seguridad internacionales.'
        },
        {
          q: '¿Puedo exportar mis datos?',
          a: 'Claro, puedes descargar todos tus datos en formato CSV o JSON en cualquier momento.'
        },
        {
          q: '¿Qué sucede si olvido mi contraseña?',
          a: 'Puedes usar la opción "Olvidé mi contraseña" en la pantalla de inicio de sesión para restablecerla fácilmente.'
        }
      ]
    },
    {
      category: 'Facturación',
      questions: [
        {
          q: '¿Cómo funciona la facturación?',
          a: 'Se te facturará mensualmente en el aniversario de tu suscripción. Recibirás una factura por correo electrónico.'
        },
        {
          q: '¿Puedo cambiar mi plan en cualquier momento?',
          a: 'Sí, puedes cambiar o cancelar tu plan en cualquier momento desde tu panel de configuración.'
        },
        {
          q: '¿Hay un contrato a largo plazo?',
          a: 'No, no hay contrato a largo plazo. Puedes cancelar en cualquier momento sin penalización.'
        }
      ]
    }
  ]

  const toggleQuestion = (index) => {
    setOpenIndex(openIndex === index ? null : index)
  }

  return (
    <div className='min-h-screen p-6 bg-slate-50'>
      <div className='max-w-3xl mx-auto'>
        {/* Header */}
        <div className='text-center mb-12'>
          <h1 className='text-4xl font-bold text-slate-900 mb-4'>Frequently Asked Questions</h1>
          <p className='text-xl text-slate-600'>
            Encuentra respuestas a preguntas comunes sobre Mesapass
          </p>
        </div>

        {/* Search Box */}
        <div className='mb-12'>
          <input
            type='text'
            placeholder='Busca una pregunta...'
            className='w-full px-6 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm'
          />
        </div>

        {/* FAQ Categories */}
        <div className='space-y-8'>
          {faqs.map((category, categoryIdx) => (
            <div key={categoryIdx}>
              <h2 className='text-2xl font-bold text-slate-900 mb-4 flex items-center gap-2'>
                <span className='text-indigo-600'>📋</span>
                {category.category}
              </h2>
              
              <div className='space-y-3 bg-white rounded-lg shadow-md overflow-hidden'>
                {category.questions.map((item, idx) => {
                  const globalIndex = faqs
                    .slice(0, categoryIdx)
                    .reduce((sum, cat) => sum + cat.questions.length, 0) + idx

                  return (
                    <details
                      key={idx}
                      className='border-b border-slate-200 last:border-b-0 group'
                      open={openIndex === globalIndex}
                    >
                      <summary
                        onClick={() => toggleQuestion(globalIndex)}
                        className='flex items-center justify-between px-6 py-4 cursor-pointer hover:bg-indigo-50 transition-colors'
                      >
                        <span className='font-medium text-slate-900 text-lg'>{item.q}</span>
                        <span className='text-indigo-600 text-2xl transition-transform group-open:rotate-180'>
                          ↓
                        </span>
                      </summary>
                      <div className='px-6 py-4 bg-slate-50 border-t border-slate-200 text-slate-700 leading-relaxed'>
                        {item.a}
                      </div>
                    </details>
                  )
                })}
              </div>
            </div>
          ))}
        </div>

        {/* Contact Section */}
        <div className='mt-12 bg-indigo-50 border border-indigo-200 rounded-lg p-8 text-center'>
          <h3 className='text-2xl font-bold text-slate-900 mb-2'>¿No encontraste tu respuesta?</h3>
          <p className='text-slate-600 mb-6'>
            Nuestro equipo de soporte está aquí para ayudarte
          </p>
          <button className='px-8 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium'>
            Contacta al Soporte
          </button>
        </div>
      </div>
    </div>
  )
}
