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
import Alert from '@mui/material/Alert'
import CircularProgress from '@mui/material/CircularProgress'
import Box from '@mui/material/Box'

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

const LoginV2 = ({ mode }) => {
  // States
  const [isPasswordShown, setIsPasswordShown] = useState(false)
  const [isRegister, setIsRegister] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [role, setRole] = useState('employee')
  const [loading, setLoading] = useState(false)
  const [errors, setErrors] = useState({})
  const [successMessage, setSuccessMessage] = useState('')

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

  // Validation functions
  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  const validatePassword = (pwd) => pwd.length >= 6

  const validateRegisterForm = () => {
    const newErrors = {}

    if (!email.trim()) {
      newErrors.email = 'Email is required'
    } else if (!validateEmail(email)) {
      newErrors.email = 'Please enter a valid email'
    }

    if (!firstName.trim()) {
      newErrors.firstName = 'First name is required'
    }

    if (!lastName.trim()) {
      newErrors.lastName = 'Last name is required'
    }

    if (!password.trim()) {
      newErrors.password = 'Password is required'
    } else if (!validatePassword(password)) {
      newErrors.password = 'Password must be at least 6 characters'
    }

    if (!role) {
      newErrors.role = 'Role is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const validateLoginForm = () => {
    const newErrors = {}

    if (!email.trim()) {
      newErrors.email = 'Email is required'
    } else if (!validateEmail(email)) {
      newErrors.email = 'Please enter a valid email'
    }

    if (!password.trim()) {
      newErrors.password = 'Password is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleRegister = async (e) => {
    e.preventDefault()
    setErrors({})
    setSuccessMessage('')

    if (!validateRegisterForm()) {
      return
    }

    setLoading(true)

    try {
      const response = await fetch('http://localhost:8000/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
          first_name: firstName,
          last_name: lastName,
          role,
          tenant_id: 1, // Default tenant for now
        }),
      })

      if (response.ok) {
        setSuccessMessage('✓ Usuario creado con éxito. Ahora puedes iniciar sesión.')
        setEmail('')
        setPassword('')
        setFirstName('')
        setLastName('')
        setRole('employee')
        setTimeout(() => {
          setIsRegister(false)
          setSuccessMessage('')
        }, 2000)
      } else {
        const errorData = await response.json()
        const errorMessage = errorData?.detail || 'Registro fallido'
        
        // Handle specific error messages
        if (errorMessage.includes('already registered') || errorMessage.includes('Email already')) {
          setErrors({ email: 'Este email ya está registrado' })
        } else if (errorMessage.includes('password')) {
          setErrors({ password: 'La contraseña no cumple los requisitos' })
        } else {
          setErrors({ general: errorMessage })
        }
      }
    } catch (error) {
      console.error('Register error:', error)
      setErrors({ general: 'Error en el registro: ' + error.message })
    } finally {
      setLoading(false)
    }
  }

  const handleLogin = async (e) => {
    e.preventDefault()
    setErrors({})
    setSuccessMessage('')

    if (!validateLoginForm()) {
      return
    }

    setLoading(true)

    try {
      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })

      if (response.ok) {
        const data = await response.json()

        localStorage.setItem('token', data.data.access_token)

        if (data.data.refresh_token) {
          localStorage.setItem('refresh_token', data.data.refresh_token)
        }

        try {
          const meResponse = await fetch('http://localhost:8000/auth/me', {
            headers: {
              Authorization: `Bearer ${data.data.access_token}`,
              'Content-Type': 'application/json'
            }
          })

          if (meResponse.ok) {
            const currentUserData = await meResponse.json()
            const userData = currentUserData.data || currentUserData
            localStorage.setItem('user', JSON.stringify(userData))
          }
        } catch (err) {
          console.warn('Could not fetch user data after login:', err)
        }

        setSuccessMessage('✓ Login exitoso')
        setTimeout(() => {
          router.push('/home')
        }, 500)
      } else {
        const errorData = await response.json()
        const errorMessage = errorData?.detail || 'Login fallido'
        
        if (errorMessage.includes('Incorrect') || errorMessage.includes('incorrect')) {
          setErrors({ general: 'Email o contraseña incorrectos' })
        } else {
          setErrors({ general: errorMessage })
        }
      }
    } catch (error) {
      console.error('Login error:', error)
      setErrors({ general: 'Error en el login: ' + error.message })
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = (e) => {
    if (isRegister) {
      handleRegister(e)
    } else {
      handleLogin(e)
    }
  }

  const handleToggleMode = () => {
    setIsRegister(!isRegister)
    setEmail('')
    setPassword('')
    setFirstName('')
    setLastName('')
    setRole('employee')
    setErrors({})
    setSuccessMessage('')
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
            <Typography variant='h4'>{`Welcome to ${themeConfig.templateName}! 👋🏻`}</Typography>
            <Typography>
              {isRegister ? 'Create your account to get started' : 'Please sign-in to your account and start the adventure'}
            </Typography>
          </div>

          {successMessage && (
            <Alert severity='success' onClose={() => setSuccessMessage('')}>
              {successMessage}
            </Alert>
          )}

          {errors.general && (
            <Alert severity='error' onClose={() => setErrors({})}>
              {errors.general}
            </Alert>
          )}

          <form noValidate autoComplete='off' onSubmit={handleSubmit} className='flex flex-col gap-5'>
            {isRegister && (
              <>
                <Box>
                  <CustomTextField
                    fullWidth
                    label='First Name'
                    placeholder='Enter your first name'
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    error={!!errors.firstName}
                    slotProps={{
                      formHelperText: {
                        children: errors.firstName
                      }
                    }}
                  />
                  {errors.firstName && <Typography className='text-error text-xs mt-1'>{errors.firstName}</Typography>}
                </Box>

                <Box>
                  <CustomTextField
                    fullWidth
                    label='Last Name'
                    placeholder='Enter your last name'
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    error={!!errors.lastName}
                    slotProps={{
                      formHelperText: {
                        children: errors.lastName
                      }
                    }}
                  />
                  {errors.lastName && <Typography className='text-error text-xs mt-1'>{errors.lastName}</Typography>}
                </Box>

                <Box>
                  <CustomTextField
                    fullWidth
                    label='Full Name'
                    placeholder='Auto-generated'
                    value={`${firstName} ${lastName}`.trim()}
                    InputProps={{
                      readOnly: true,
                    }}
                  />
                </Box>

                <Box>
                  <CustomTextField
                    fullWidth
                    label='Role'
                    select
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                    error={!!errors.role}
                    slotProps={{
                      htmlSelect: {
                        children: (
                          <>
                            <option value='employee'>Employee</option>
                            <option value='admin'>Admin</option>
                          </>
                        )
                      },
                      formHelperText: {
                        children: errors.role
                      }
                    }}
                  />
                  {errors.role && <Typography className='text-error text-xs mt-1'>{errors.role}</Typography>}
                </Box>
              </>
            )}

            <Box>
              <CustomTextField
                autoFocus
                fullWidth
                label='Email'
                placeholder='Enter your email'
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                error={!!errors.email}
                slotProps={{
                  formHelperText: {
                    children: errors.email
                  }
                }}
              />
              {errors.email && <Typography className='text-error text-xs mt-1'>{errors.email}</Typography>}
            </Box>

            <Box>
              <CustomTextField
                fullWidth
                label='Password'
                placeholder='············'
                id='outlined-adornment-password'
                type={isPasswordShown ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                error={!!errors.password}
                slotProps={{
                  formHelperText: {
                    children: errors.password
                  },
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
              {errors.password && <Typography className='text-error text-xs mt-1'>{errors.password}</Typography>}
            </Box>

            {!isRegister && (
              <div className='flex justify-between items-center gap-x-3 gap-y-1 flex-wrap'>
                <FormControlLabel control={<Checkbox />} label='Remember me' />
                <Typography className='text-end' color='primary.main' component={Link}>
                  Forgot password?
                </Typography>
              </div>
            )}

            <Button
              fullWidth
              variant='contained'
              type='submit'
              disabled={loading}
              startIcon={loading && <CircularProgress size={20} />}
            >
              {loading ? (isRegister ? 'Creating...' : 'Logging in...') : (isRegister ? 'Register' : 'Login')}
            </Button>

            <div className='flex justify-center items-center flex-wrap gap-2'>
              <Typography>{isRegister ? 'Already have an account?' : 'New on our platform?'}</Typography>
              <Typography component={Link} color='primary.main' onClick={handleToggleMode} className='cursor-pointer'>
                {isRegister ? 'Go to login' : 'Create an account'}
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
