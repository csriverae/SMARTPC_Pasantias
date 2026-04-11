// MUI Imports
import InitColorSchemeScript from '@mui/material/InitColorSchemeScript'

// Third-party Imports
import 'react-perfect-scrollbar/dist/css/styles.css'

// Util Imports
import { getSystemMode } from '@core/utils/serverHelpers'

// Style Imports - Import from src with correct paths
import '@/app/globals.css'
import '@assets/iconify-icons/generated-icons.css'
import '@core/styles/globals.css'

export const metadata = {
  title: 'Mesapass - Sistema de Gestión de Restaurantes',
  description: 'Mesapass - Plataforma integrada para restaurantes y empresas de catering'
}

const RootLayout = async ({
  children,
}: {
  children: React.ReactNode
}) => {
  const systemMode = await getSystemMode()
  const direction = 'ltr'

  return (
    <html id='__next' lang='es' dir={direction} suppressHydrationWarning>
      <body className='flex is-full min-bs-full flex-auto flex-col'>
        <InitColorSchemeScript attribute='data' defaultMode={systemMode} />
        {children}
      </body>
    </html>
  )
}

export default RootLayout