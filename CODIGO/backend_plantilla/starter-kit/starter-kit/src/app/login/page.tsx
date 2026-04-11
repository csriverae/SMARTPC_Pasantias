// Component Imports
import LoginV2 from '@views/Login'

// Server Action Imports
import { getServerMode } from '@core/utils/serverHelpers'

export const metadata = {
  title: 'MesaPass - Iniciar Sesión',
  description: 'Inicia sesión en MesaPass para gestionar tu sistema de alimentación'
}

const LoginPage = async () => {
  // Vars
  const mode = await getServerMode()

  return <LoginV2 mode={mode} />
}

export default LoginPage