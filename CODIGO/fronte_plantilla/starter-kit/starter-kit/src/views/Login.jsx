'use client'

// React Imports
import { useState } from 'react'

// Next Imports
import { useRouter } from 'next/navigation'

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

// Config Imports
import themeConfig from '@configs/themeConfig'

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

              const apiUrl = isRegister ? 'http://localhost:8000/auth/register' : 'http://localhost:8000/auth/login'

              const body = isRegister
                ? JSON.stringify({
                    email,
                    password,
                    full_name: `${firstName} ${lastName}`.trim(),
                    tenant_name: tenantName
                  })
                : JSON.stringify({ email, password })

              try {
                const response = await fetch(apiUrl, {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                  },
                  body,
                })

                if (response.ok) {
                  const data = await response.json()
                  const authData = data?.data?.data || {}

                  if (!authData.access_token) {
                    throw new Error('No se recibió access_token del servidor')
                  }

                  const backendUser = authData.user || {}
                  const normalizedUser = {
                    ...backendUser,
                    role: backendUser.role || backendUser.tenant_role || backendUser.role
                  }

                  localStorage.setItem('token', authData.access_token)

                  if (authData.refresh_token) {
                    localStorage.setItem('refresh_token', authData.refresh_token)
                  }

                  localStorage.setItem('tenant_id', authData.tenant_id)
                  localStorage.setItem('user', JSON.stringify(normalizedUser))

                  try {
                    const meResponse = await fetch('http://localhost:8000/auth/me', {
                      headers: {
                        Authorization: `Bearer ${authData.access_token}`,
                        'X-Tenant-ID': authData.tenant_id,
                        'Content-Type': 'application/json'
                      }
                    })

                    if (meResponse.ok) {
                      const currentUser = await meResponse.json()
                      const parsedUser = currentUser?.data?.data || currentUser
                      const normalizedMeUser = {
                        ...parsedUser,
                        role: parsedUser.role || parsedUser.tenant_role || normalizedUser.role
                      }
                      localStorage.setItem('user', JSON.stringify(normalizedMeUser))
                    }
                  } catch (err) {
                    console.warn('No se pudo obtener el usuario después del login/registro:', err)
                  }

                  router.push('/home')
                } else {
                  const errorData = await response.json()
                  alert(errorData.detail || errorData.message || (isRegister ? 'Registro fallido' : 'Login fallido'))
                }
              } catch (error) {
                console.error(isRegister ? 'Register error:' : 'Login error:', error)
                alert((isRegister ? 'Registro error:' : 'Login error:') + ' ' + error.message)
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
    </div>
  )
}

export default LoginV2
