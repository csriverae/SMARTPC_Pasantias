// MUI Imports
import InitColorSchemeScript from '@mui/material/InitColorSchemeScript'

// Third-party Imports
import 'react-perfect-scrollbar/dist/css/styles.css'

// Util Imports
import { getSystemMode } from '@core/utils/serverHelpers'

// Style Imports
import '@/app/globals.css'

// Generated Icon CSS Imports
import '@assets/iconify-icons/generated-icons.css'

// Performance Polyfill Import
import '@lib/performance-polyfill'
import PerformancePolyfillProvider from '@components/PerformancePolyfillProvider'
import EarlyPerformancePolyfill from '@components/EarlyPerformancePolyfill'

export const metadata = {
  title: 'Vuexy - MUI Next.js Admin Dashboard Template',
  description:
    'Vuexy - MUI Next.js Admin Dashboard Template - is the most developer friendly & highly customizable Admin Dashboard Template based on MUI v5.'
}

const RootLayout = async props => {
  const { children } = props

  // Type guard to ensure lang is a valid Locale
  // Vars
  const systemMode = await getSystemMode()
  const direction = 'ltr'

  return (
    <html id='__next' lang='en' dir={direction} suppressHydrationWarning>
      <body className='flex is-full min-bs-full flex-auto flex-col'>
        <EarlyPerformancePolyfill />
        <InitColorSchemeScript attribute='data' defaultMode={systemMode} />
        <PerformancePolyfillProvider />
        {children}
      </body>
    </html>
  )
}

export default RootLayout
