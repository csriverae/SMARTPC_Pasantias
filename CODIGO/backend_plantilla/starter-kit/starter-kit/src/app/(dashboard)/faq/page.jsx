'use client'

import { useState } from 'react'

export default function Page() {
  const [openIndex, setOpenIndex] = useState(null)

  const faqs = [
    {
      category: 'General',
      questions: [
        {
          q: '¿Qué es MesaPass?',
          a: 'MesaPass es una plataforma integral para gestionar empleados, acuerdos con restaurantes, registros de consumo y reportes de facturación.'
        },
        {
          q: '¿Cómo puedo empezar?',
          a: 'Crea una cuenta gratuita en el plan Básico. Puedes crear empresas, agregar empleados y comenzar a registrar consumos inmediatamente.'
        },
        {
          q: '¿Necesito tarjeta de crédito para la prueba?',
          a: 'No, el plan Básico es completamente gratuito y sin límite de tiempo. Los planes pagados incluyen una prueba de 14 días.'
        }
      ]
    },
    {
      category: 'Empleados y Documentos',
      questions: [
        {
          q: '¿Cómo agregó empleados a mi empresa?',
          a: 'Ve a Empleados, haz clic en "Nuevo Empleado" e ingresa nombre y email. Cada empleado recibe un código QR único para registrar consumos.'
        },
        {
          q: '¿Qué es el código QR del empleado?',
          a: 'Es un identificador único que permite validar el consumo del empleado en los restaurantes. Cada empleado puede descargar o imprimir su QR.'
        },
        {
          q: '¿Puedo tener varios empleados en una empresa?',
          a: 'Sí, según tu plan. El Básico permite hasta 20 empleados y el Profesional hasta 200. El Empresarial es ilimitado.'
        }
      ]
    },
    {
      category: 'Acuerdos y Consumo',
      questions: [
        {
          q: '¿Qué es un acuerdo en MesaPass?',
          a: 'Un acuerdo es la relación entre tu empresa y un restaurante. Define el tipo de consumo permitido y el período del acuerdo.'
        },
        {
          q: '¿Cómo registro un consumo?',
          a: 'Los consumos se registran usando el código QR del empleado en un restaurante. El sistema valida automáticamente el acuerdo vigente.'
        },
        {
          q: '¿Puedo tener múltiples acuerdos?',
          a: 'Sí, puedes crear tantos acuerdos como necesites con diferentes restaurantes. Cada uno gestiona sus períodos y límites independientemente.'
        }
      ]
    },
    {
      category: 'Reportes y Facturación',
      questions: [
        {
          q: '¿Qué información muestran los reportes?',
          a: 'MesaPass proporciona reportes de consumo por empleado, tipo de comida, acuerdo y período. También incluye resúmenes de facturación.'
        },
        {
          q: '¿Cómo accedo a mis reportes?',
          a: 'Ve a Reportes en tu panel. Puedes generar reportes de consumo y facturación en el rango de fechas que necesites.'
        },
        {
          q: '¿Puedo exportar datos?',
          a: 'Sí, todos reportes se pueden descargar en formatos PDF o Excel para uso externo o auditoría.'
        }
      ]
    },
    {
      category: 'Seguridad y Datos',
      questions: [
        {
          q: '¿Mis datos están seguros?',
          a: 'Sí, MesaPass usa encriptación SSL/TLS y cumple con estándares internacionales de seguridad de datos.'
        },
        {
          q: '¿Qué pasa si olvido mi contraseña?',
          a: 'Usa la opción "Olvidé mi contraseña" en el login. Recibirás un enlace para restablecerla en tu correo.'
        },
        {
          q: '¿Cómo cambio mi contraseña?',
          a: 'Ve a Configuración > Seguridad y usa la sección "Cambiar contraseña". Necesitarás tu contraseña actual para confirmar.'
        }
      ]
    }
  ]

  const toggleQuestion = (index) => {
    setOpenIndex(openIndex === index ? null : index)
  }

  return (
    <div className='min-h-screen p-6 bg-slate-50'>
      <div className='max-w-full'>
        {/* Header */}
        <div className='text-center mb-12'>
          <h1 className='text-4xl font-bold text-slate-900 mb-4'>Preguntas Frecuentes</h1>
          <p className='text-xl text-slate-600'>
            Resuelve tus dudas sobre MesaPass
          </p>
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
            Contacta a Soporte
          </button>
        </div>
      </div>
    </div>
  )
}}
