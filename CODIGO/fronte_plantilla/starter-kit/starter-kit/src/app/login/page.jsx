// Component Imports
import LoginV2 from '@views/Login'

// Server Action Imports
import { getServerMode } from '@core/utils/serverHelpers'

export const metadata = {
  title: 'Login',
  description: 'Login to your account'
}

const LoginPage = async () => {
  const mode = await getServerMode()

  return <LoginV2 mode={mode} />
}

export default LoginPage
