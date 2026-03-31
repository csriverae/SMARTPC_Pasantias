'use client'

import { useState } from 'react'
import { usePathname, useRouter } from 'next/navigation'
import Box from '@mui/material/Box'
import Drawer from '@mui/material/Drawer'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'
import ListItemButton from '@mui/material/ListItemButton'
import ListItemIcon from '@mui/material/ListItemIcon'
import ListItemText from '@mui/material/ListItemText'
import Divider from '@mui/material/Divider'
import Avatar from '@mui/material/Avatar'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import Tooltip from '@mui/material/Tooltip'
import VuexyLogo from '@core/svg/Logo'
import themeConfig from '@configs/themeConfig'
import { useAuthUser } from '@core/hooks/useAuthUser'

const DashboardSidebar = () => {
  const router = useRouter()
  const pathname = usePathname()
  const { user, loading } = useAuthUser()
  const [mobileOpen, setMobileOpen] = useState(false)
  const [isHovered, setIsHovered] = useState(false)

  const SIDEBAR_COLLAPSED_WIDTH = 60
  const SIDEBAR_EXPANDED_WIDTH = 280

  // Menu structure based on user role
  const getMenuItems = () => {
    const baseMenu = [
      {
        id: 'dashboard',
        label: 'Dashboard',
        icon: 'tabler-layout-dashboard',
        path: '/home',
        visible: true
      },
      {
        id: 'profile',
        label: 'My Profile',
        icon: 'tabler-user',
        path: '/home/profile',
        visible: true
      },
      {
        id: 'settings',
        label: 'Settings',
        icon: 'tabler-settings',
        path: '/home/settings',
        visible: true
      }
    ]

    const adminMenu = [
      {
        id: 'tenants',
        label: 'Tenants',
        icon: 'tabler-building-community',
        path: '/home/tenants',
        visible: user?.role === 'admin'
      },
      {
        id: 'users',
        label: 'Users Management',
        icon: 'tabler-users-group',
        path: '/home/users',
        visible: user?.role === 'admin'
      },
      {
        id: 'restaurants',
        label: 'Restaurants',
        icon: 'tabler-building-store',
        path: '/home/restaurants',
        visible: user?.role === 'restaurant_admin' || user?.role === 'admin'
      },
      {
        id: 'employees',
        label: 'Employees',
        icon: 'tabler-briefcase',
        path: '/home/employees',
        visible: user?.role === 'company_admin' || user?.role === 'admin'
      },
      {
        id: 'meals',
        label: 'Meal Logs',
        icon: 'tabler-soup',
        path: '/home/meals',
        visible: user?.role !== 'admin'
      }
    ]

    return [...baseMenu, ...adminMenu].filter(item => item.visible)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    router.push('/login')
  }

  const handleMenuClick = (path) => {
    router.push(path)
  }

  const getRoleColor = (role) => {
    const colors = {
      admin: 'error',
      restaurant_admin: 'warning',
      company_admin: 'info',
      employee: 'success'
    }
    return colors[role] || 'default'
  }

  const getRoleLabel = (role) => {
    const labels = {
      admin: 'ADMINISTRATOR',
      restaurant_admin: 'RESTAURANT ADMIN',
      company_admin: 'COMPANY ADMIN',
      employee: 'EMPLOYEE'
    }
    return labels[role] || role
  }

  const menuItems = getMenuItems()

  // Desktop Animated Sidebar Content
  const sidebarContent = (
    <Box
      sx={{
        width: isHovered ? SIDEBAR_EXPANDED_WIDTH : SIDEBAR_COLLAPSED_WIDTH,
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        bgcolor: 'background.paper',
        borderRight: 1,
        borderColor: 'divider',
        boxShadow: 1,
        transition: 'width 0.3s ease-in-out',
        overflow: 'hidden'
      }}
    >
      {/* Brand Section */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', p: 1.5, borderBottom: 1, borderColor: 'divider', minHeight: 70 }}>
        <VuexyLogo className='text-2xl' style={{ color: 'var(--mui-palette-primary-main)' }} />
        {isHovered && (
          <Typography variant='h6' sx={{ fontWeight: 'bold', color: 'primary.main', ml: 1, whiteSpace: 'nowrap' }}>
            {themeConfig.templateName}
          </Typography>
        )}
      </Box>

      {/* User Profile Section */}
      <Box sx={{ p: isHovered ? 2 : 1, bgcolor: 'primary.main', color: 'white', flexShrink: 0 }}>
        {isHovered ? (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Avatar
              sx={{
                width: 48,
                height: 48,
                bgcolor: 'primary.light',
                fontSize: '1.5rem',
                fontWeight: 'bold',
                flexShrink: 0
              }}
            >
              {user?.full_name?.charAt(0).toUpperCase() || 'U'}
            </Avatar>
            <Box>
              <Typography variant='subtitle2' sx={{ fontWeight: 'bold', whiteSpace: 'nowrap' }}>
                {user?.full_name || 'User'}
              </Typography>
              <Typography variant='caption' sx={{ opacity: 0.8, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', display: 'block' }}>
                {user?.email || 'Loading...'}
              </Typography>
            </Box>
          </Box>
        ) : (
          <Box sx={{ display: 'flex', justifyContent: 'center' }}>
            <Avatar
              sx={{
                width: 40,
                height: 40,
                bgcolor: 'primary.light',
                fontSize: '1.2rem',
                fontWeight: 'bold'
              }}
            >
              {user?.full_name?.charAt(0).toUpperCase() || 'U'}
            </Avatar>
          </Box>
        )}
      </Box>

      {/* Role Badge */}
      {user && (
        <Box sx={{ px: isHovered ? 2 : 1, py: 1, display: 'flex', justifyContent: isHovered ? 'flex-start' : 'center' }}>
          <Box
            sx={{
              display: 'inline-block',
              px: 2,
              py: 0.5,
              bgcolor: `${getRoleColor(user.role)}.light`,
              color: `${getRoleColor(user.role)}.main`,
              borderRadius: 1,
              fontSize: '0.65rem',
              fontWeight: 'bold',
              textTransform: 'uppercase',
              whiteSpace: 'nowrap'
            }}
          >
            {getRoleLabel(user.role)}
          </Box>
        </Box>
      )}

      <Divider sx={{ my: 1 }} />

      {/* Menu Items */}
      <List sx={{ flex: 1, overflow: 'auto', py: 1, px: 0 }}>
        {menuItems.map(item => (
          <Tooltip key={item.id} title={!isHovered ? item.label : ''} placement='right'>
            <ListItem disablePadding sx={{ display: 'block' }}>
              <ListItemButton
                onClick={() => handleMenuClick(item.path)}
                selected={pathname === item.path}
                sx={{
                  minHeight: 48,
                  justifyContent: isHovered ? 'initial' : 'center',
                  px: isHovered ? 2 : 1,
                  '&.Mui-selected': {
                    bgcolor: 'primary.light',
                    color: 'primary.main',
                    fontWeight: 'bold',
                    '& .MuiListItemIcon-root': {
                      color: 'primary.main'
                    }
                  },
                  '&:hover': {
                    bgcolor: 'action.hover'
                  }
                }}
              >
                <ListItemIcon sx={{ minWidth: 0, mr: isHovered ? 2 : 0, justifyContent: 'center' }}>
                  <i className={item.icon} style={{ fontSize: '1.25rem' }} />
                </ListItemIcon>
                {isHovered && <ListItemText primary={item.label} sx={{ '& .MuiTypography-root': { fontSize: '0.875rem' } }} />}
              </ListItemButton>
            </ListItem>
          </Tooltip>
        ))}
      </List>

      <Divider />

      {/* Logout Button */}
      <Box sx={{ p: isHovered ? 2 : 1, display: 'flex', justifyContent: 'center' }}>
        <Tooltip title={!isHovered ? 'Logout' : ''} placement='right'>
          <Button
            fullWidth={isHovered}
            variant='outlined'
            color='error'
            onClick={handleLogout}
            sx={{
              width: isHovered ? '100%' : 40,
              height: 40,
              minWidth: 40,
              padding: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <i className='tabler-logout' style={{ fontSize: '1.2rem' }} />
          </Button>
        </Tooltip>
      </Box>
    </Box>
  )

  return (
    <>
      {/* Desktop Animated Sidebar */}
      <Box
        sx={{
          display: { xs: 'none', sm: 'none', md: 'block' },
          position: 'fixed',
          left: 0,
          top: 0,
          zIndex: 1000
        }}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        {sidebarContent}
      </Box>

      {/* Mobile Drawer */}
      <Drawer
        anchor='left'
        open={mobileOpen}
        onClose={() => setMobileOpen(false)}
      >
        <Box sx={{ width: 280, height: '100%', display: 'flex', flexDirection: 'column' }}>
          {/* Brand Section for Mobile */}
          <Box sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 1, bgcolor: 'background.paper', borderBottom: 1, borderColor: 'divider' }}>
            <VuexyLogo className='text-2xl' style={{ color: 'var(--mui-palette-primary-main)' }} />
            <Typography variant='h6' sx={{ fontWeight: 'bold', color: 'primary.main' }}>
              {themeConfig.templateName}
            </Typography>
          </Box>

          {/* User Profile Section for Mobile */}
          <Box sx={{ p: 2, bgcolor: 'primary.main', color: 'white' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
              <Avatar
                sx={{
                  width: 48,
                  height: 48,
                  bgcolor: 'primary.light',
                  fontSize: '1.5rem',
                  fontWeight: 'bold'
                }}
              >
                {user?.full_name?.charAt(0).toUpperCase() || 'U'}
              </Avatar>
              <Box>
                <Typography variant='subtitle2' sx={{ fontWeight: 'bold' }}>
                  {user?.full_name || 'User'}
                </Typography>
                <Typography variant='caption' sx={{ opacity: 0.8 }}>
                  {user?.email || 'Loading...'}
                </Typography>
              </Box>
            </Box>
          </Box>

          {/* Role Badge for Mobile */}
          {user && (
            <Box sx={{ px: 2, py: 1 }}>
              <Box
                sx={{
                  display: 'inline-block',
                  px: 2,
                  py: 0.5,
                  bgcolor: `${getRoleColor(user.role)}.light`,
                  color: `${getRoleColor(user.role)}.main`,
                  borderRadius: 1,
                  fontSize: '0.75rem',
                  fontWeight: 'bold',
                  textTransform: 'uppercase'
                }}
              >
                {getRoleLabel(user.role)}
              </Box>
            </Box>
          )}

          <Divider sx={{ my: 2 }} />

          {/* Menu Items for Mobile */}
          <List sx={{ flex: 1, overflow: 'auto' }}>
            {menuItems.map(item => (
              <ListItem key={item.id} disablePadding sx={{ display: 'block' }}>
                <ListItemButton
                  onClick={() => {
                    handleMenuClick(item.path)
                    setMobileOpen(false)
                  }}
                  selected={pathname === item.path}
                  sx={{
                    '&.Mui-selected': {
                      bgcolor: 'primary.light',
                      color: 'primary.main',
                      fontWeight: 'bold',
                      '& .MuiListItemIcon-root': {
                        color: 'primary.main'
                      }
                    },
                    '&:hover': {
                      bgcolor: 'action.hover'
                    }
                  }}
                >
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    <i className={item.icon} style={{ fontSize: '1.25rem' }} />
                  </ListItemIcon>
                  <ListItemText primary={item.label} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>

          <Divider />

          {/* Logout Button for Mobile */}
          <Box sx={{ p: 2 }}>
            <Button
              fullWidth
              variant='outlined'
              color='error'
              onClick={handleLogout}
              startIcon={<i className='tabler-logout' />}
            >
              Logout
            </Button>
          </Box>
        </Box>
      </Drawer>

      {/* Mobile Menu Button */}
      <Box
        sx={{
          display: { xs: 'flex', sm: 'flex', md: 'none' },
          position: 'fixed',
          top: 16,
          left: 16,
          zIndex: 999,
          bgcolor: 'primary.main',
          borderRadius: 1,
          p: 1,
          cursor: 'pointer'
        }}
        onClick={() => setMobileOpen(!mobileOpen)}
      >
        <i className='tabler-menu-2' style={{ color: 'white', fontSize: '1.5rem' }}></i>
      </Box>
    </>
  )
}

export default DashboardSidebar
