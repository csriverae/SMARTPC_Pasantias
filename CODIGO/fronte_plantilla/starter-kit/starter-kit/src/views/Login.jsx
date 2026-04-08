'use client'

// React Imports
import { useState } from 'react'

// Next Imports
import { useRouter } from 'next/navigation'

// Utils
import api from '@/utils/api'

// MUI Imports
import useMediaQuery from '@mui/material/useMediaQuery'
import { styled, useTheme } from '@mui/material/styles'
import Typography from '@mui/material/Typography'
import IconButton from '@mui/material/IconButton'
import InputAdornment from '@mui/material/InputAdornment'
import Checkbox from '@mui/material/Checkbox'
import Button from '@mui/material/Button'
import FormControlLabel from '@mui/material/FormControlLabel'
import Divider from '@mui/material/Divider'

// Third-party Imports
import classnames from 'classnames'

// Component Imports
import Link from '@components/Link'
import Logo from '@components/layout/shared/Logo'
import CustomTextField from '@core/components/mui/TextField'

// Hook Imports
import { useImageVariant } from '@core/hooks/useImageVariant'
import { useSettings } from '@core/hooks/useSettings'

// Styled Custom Components
const LoginIllustration = styled('img')(({ theme }) => ({
  zIndex: 2,
  blockSize: 'auto',
  maxBlockSize: 680,
  maxInlineSize: '100%',
  margin: theme.spacing(12),
  [theme.breakpoints.down(1536)]: {
    maxBlockSize: 550
  },
  [theme.breakpoints.down('lg')]: {
    maxBlockSize: 450
  }
}))

const MaskImg = styled('img')({
  blockSize: 'auto',
  maxBlockSize: 355,
  inlineSize: '100%',
  position: 'absolute',
  insetBlockEnd: 0,
  zIndex: -1
})

const LoginV2 = ({ mode, initialRegister = false }) => {
  // States
  const [isPasswordShown, setIsPasswordShown] = useState(false)
  const [isRegister, setIsRegister] = useState(initialRegister)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [tenantName, setTenantName] = useState('')
  const [loading, setLoading] = useState(false)
  const [tenants, setTenants] = useState([])
  const [showTenantSelector, setShowTenantSelector] = useState(false)
  const [selectedTenant, setSelectedTenant] = useState(null)

  // Vars
  const darkImg = '/images/pages/auth-mask-dark.png'
  const lightImg = '/images/pages/auth-mask-light.png'
  const darkIllustration = '/images/illustrations/auth/v2-login-dark.png'
  const lightIllustration = '/images/illustrations/auth/v2-login-light.png'
  const borderedDarkIllustration = '/images/illustrations/auth/v2-login-dark-border.png'
  const borderedLightIllustration = '/images/illustrations/auth/v2-login-light-border.png'

  // Hooks
  const router = useRouter()
  const { settings } = useSettings()
  const theme = useTheme()
  const hidden = useMediaQuery(theme.breakpoints.down('md'))
  const authBackground = useImageVariant(mode, lightImg, darkImg)

  const characterIllustration = useImageVariant(
    mode,
    lightIllustration,
    darkIllustration,
    borderedLightIllustration,
    borderedDarkIllustration
  )

  const handleClickShowPassword = () => setIsPasswordShown(show => !show)

  const completeLogin = async (authData, backendUser, tenantData) => {
    const normalizedUser = {
      ...backendUser,
      role: tenantData.role || backendUser.tenant_role || backendUser.role,
      tenant_name: tenantData.tenant_name,
      tenant_id: tenantData.tenant_id
    }

    localStorage.setItem('token', authData.access_token)
    if (authData.refresh_token) {
      localStorage.setItem('refresh_token', authData.refresh_token)
    }
    localStorage.setItem('tenant_id', tenantData.tenant_id)
    localStorage.setItem('user', JSON.stringify(normalizedUser))

    try {
      const meResponse = await api.get('/auth/me')
      const parsedUser = meResponse.data?.data?.data || meResponse.data?.data || meResponse.data
      const normalizedMeUser = {
        ...parsedUser,
        role: parsedUser.role || parsedUser.tenant_role || normalizedUser.role,
        tenant_name: tenantData.tenant_name,
        tenant_id: tenantData.tenant_id
      }
      localStorage.setItem('user', JSON.stringify(normalizedMeUser))
    } catch (err) {
      console.warn('No se pudo obtener el usuario después del login:', err)
    }

    router.push('/home')
  }

  const handleTenantSelect = async (tenant) => {
    const tempToken = localStorage.getItem('temp_token')
    const tempRefreshToken = localStorage.getItem('temp_refresh_token')
    const tempUser = localStorage.getItem('temp_user')

    if (!tempToken || !tempUser) {
      alert('Error: No se encontraron datos temporales de autenticación')
      return
    }

    const authData = {
      access_token: tempToken,
      refresh_token: tempRefreshToken
    }

    const backendUser = JSON.parse(tempUser)
    await completeLogin(authData, backendUser, tenant)

    // Limpiar datos temporales
    localStorage.removeItem('temp_token')
    localStorage.removeItem('temp_refresh_token')
    localStorage.removeItem('temp_user')
  }

  return (
    <div className='flex bs-full justify-center'>
      <div
        className={classnames(
          'flex bs-full items-center justify-center flex-1 min-bs-[100dvh] relative p-6 max-md:hidden',
          {
            'border-ie': settings.skin === 'bordered'
          }
        )}
      >
        <LoginIllustration src={characterIllustration} alt='character-illustration' />
        {!hidden && (
          <MaskImg
            alt='mask'
            src={authBackground}
            className={classnames({ 'scale-x-[-1]': theme.direction === 'rtl' })}
          />
        )}
      </div>
      <div className='flex justify-center items-center bs-full bg-backgroundPaper !min-is-full p-6 md:!min-is-[unset] md:p-12 md:is-[480px]'>
        <Link className='absolute block-start-5 sm:block-start-[33px] inline-start-6 sm:inline-start-[38px]'>
          <Logo />
        </Link>
        <div className='flex flex-col gap-6 is-full sm:is-auto md:is-full sm:max-is-[400px] md:max-is-[unset] mbs-11 sm:mbs-14 md:mbs-0'>
          <div className='flex flex-col gap-1'>
            <Typography variant='h4'>Bienvenido a MesaPass 👋🏻</Typography>
            <Typography>Inicia sesión en tu cuenta para gestionar tu sistema de alimentación</Typography>
          </div>
          <form
            noValidate
            autoComplete='off'
            onSubmit={async (e) => {
              e.preventDefault()
              setLoading(true)

                  const endpoint = isRegister ? '/auth/register' : '/auth/login'
              const body = isRegister
                ? {
                    email,
                    password,
                    full_name: `${firstName} ${lastName}`.trim(),
                    tenant_name: tenantName
                  }
                : { email, password }

              try {
                const response = await api.post(endpoint, body)
                const data = response.data
                const authData = data?.data?.data || data?.data || data

                if (!authData.access_token) {
                  throw new Error('No se recibió access_token del servidor')
                }

                const backendUser = authData.user || authData
                const userTenants = backendUser.tenants || []

                if (userTenants.length > 1) {
                  setTenants(userTenants)
                  setShowTenantSelector(true)
                  localStorage.setItem('temp_token', authData.access_token)
                  localStorage.setItem('temp_refresh_token', authData.refresh_token || '')
                  localStorage.setItem('temp_user', JSON.stringify(backendUser))
                  setLoading(false)
                  return
                }

                const selectedTenantData = userTenants.length === 1 ? userTenants[0] : {
                  tenant_id: authData.tenant_id,
                  tenant_name: authData.tenant_name || backendUser.tenant_name || tenantName,
                  role: backendUser.tenant_role || backendUser.role
                }

                await completeLogin(authData, backendUser, selectedTenantData)
              } catch (error) {
                console.error(isRegister ? 'Register error:' : 'Login error:', error)
                alert((isRegister ? 'Registro error:' : 'Login error:') + ' ' + (error.message || 'Error en la autenticación'))
              } finally {
                setLoading(false)
              }
            }}
            className='flex flex-col gap-5'
          >
            {isRegister && (
              <>
                <CustomTextField
                  fullWidth
                  label='Nombre'
                  placeholder='Ingrese su nombre'
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  required
                />
                <CustomTextField
                  fullWidth
                  label='Apellido'
                  placeholder='Ingrese su apellido'
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  required
                />
                <CustomTextField
                  fullWidth
                  label='Nombre de la empresa'
                  placeholder='Ingrese el nombre de la empresa'
                  value={tenantName}
                  onChange={(e) => setTenantName(e.target.value)}
                  required
                />
              </>
            )}
            <CustomTextField 
              autoFocus 
              fullWidth 
              label='Email' 
              placeholder='Ingrese su email' 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <CustomTextField
              fullWidth
              label='Contraseña'
              placeholder='············'
              id='outlined-adornment-password'
              type={isPasswordShown ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              slotProps={{
                input: {
                  endAdornment: (
                    <InputAdornment position='end'>
                      <IconButton edge='end' onClick={handleClickShowPassword} onMouseDown={e => e.preventDefault()}>
                        <i className={isPasswordShown ? 'tabler-eye-off' : 'tabler-eye'} />
                      </IconButton>
                    </InputAdornment>
                  )
                }
              }}
            />
            <div className='flex justify-between items-center gap-x-3 gap-y-1 flex-wrap'>
              <FormControlLabel control={<Checkbox />} label='Recordarme' />
              <Typography className='text-end' color='primary.main' component={Link}>
                ¿Olvidaste tu contraseña?
              </Typography>
            </div>
            <Button fullWidth variant='contained' type='submit' disabled={loading}>
              {loading ? (isRegister ? 'Creando cuenta...' : 'Iniciando sesión...') : (isRegister ? 'Crear cuenta' : 'Iniciar sesión')}
            </Button>
            <div className='flex justify-center items-center flex-wrap gap-2'>
              <Typography>{isRegister ? '¿Ya tienes cuenta?' : '¿Nuevo en la plataforma?'}</Typography>
              <Typography
                component={Link}
                color='primary.main'
                onClick={() => {
                  setIsRegister(!isRegister)
                  setEmail('')
                  setPassword('')
                  setFirstName('')
                  setLastName('')
                  setTenantName('')
                  setTenants([])
                  setShowTenantSelector(false)
                  setSelectedTenant(null)
                }}
              >
                {isRegister ? 'Ir al login' : 'Crear una cuenta'}
              </Typography>
            </div>
            <Divider className='gap-2 text-textPrimary'>or</Divider>
            <div className='flex justify-center items-center gap-1.5'>
              <IconButton className='text-facebook' size='small'>
                <i className='tabler-brand-facebook-filled' />
              </IconButton>
              <IconButton className='text-twitter' size='small'>
                <i className='tabler-brand-twitter-filled' />
              </IconButton>
              <IconButton className='text-textPrimary' size='small'>
                <i className='tabler-brand-github-filled' />
              </IconButton>
              <IconButton className='text-error' size='small'>
                <i className='tabler-brand-google-filled' />
              </IconButton>
            </div>
          </form>
        </div>
      </div>

      {/* Tenant Selector Modal */}
      {showTenantSelector && (
        <div className='fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50'>
          <div className='bg-white p-6 rounded-lg shadow-lg max-w-md w-full mx-4'>
            <div className='flex justify-between items-center mb-4'>
              <h3 className='text-lg font-semibold'>Seleccionar Empresa</h3>
              <button
                onClick={() => {
                  setShowTenantSelector(false)
                  setTenants([])
                  localStorage.removeItem('temp_token')
                  localStorage.removeItem('temp_refresh_token')
                  localStorage.removeItem('temp_user')
                }}
                className='text-gray-500 hover:text-gray-700 text-xl'
              >
                ×
              </button>
            </div>
            <p className='text-gray-600 mb-4'>Selecciona la empresa con la que quieres trabajar:</p>
            <div className='space-y-3'>
              {tenants.map((tenant) => (
                <button
                  key={tenant.tenant_id}
                  onClick={() => handleTenantSelect(tenant)}
                  className='w-full p-3 border rounded-lg hover:bg-indigo-50 hover:border-indigo-300 transition-colors text-left'
                >
                  <div className='font-medium text-gray-900'>{tenant.tenant_name}</div>
                  <div className='text-sm text-gray-500 capitalize'>Rol: {tenant.role}</div>
                  <div className='text-xs text-gray-400'>Tipo: {tenant.tenant_type}</div>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default LoginV2
