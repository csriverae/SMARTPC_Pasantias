// Util Imports
import { getMode, getSettingsFromCookie, getSystemMode } from '@core/utils/serverHelpers'

// Component Imports
import ClientProviders from '@components/ClientProviders'

const Providers = async props => {
  // Props
  const { children, direction } = props

  // Vars
  const mode = await getMode()
  const settingsCookie = await getSettingsFromCookie()
  const systemMode = await getSystemMode()

  return (
    <ClientProviders
      settingsCookie={settingsCookie}
      mode={mode}
      systemMode={systemMode}
      direction={direction}
    >
      {children}
    </ClientProviders>
  )
}

export default Providers
