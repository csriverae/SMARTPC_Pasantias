// Component Imports
import LoginV2 from '@views/Login'

// Server Action Imports
import { getServerMode } from '@core/utils/serverHelpers'

export const metadata = {
  title: 'MesaPass - Crear Cuenta',
  description: 'Crea una nueva cuenta en MesaPass'
}

const RegisterPage = async () => {
  const mode = await getServerMode()

  return <LoginV2 mode={mode} initialRegister={true} />
}

export default RegisterPage
