'use client'

import { useState, useEffect } from 'react'
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
import { useAuthUser } from '@core/hooks/useAuthUser'

const DashboardSidebar = () => {
  const router = useRouter()
  const pathname = usePathname()
  const { user, loading } = useAuthUser()
  const [mobileOpen, setMobileOpen] = useState(false)

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
    setMobileOpen(false)
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
      admin: 'Administrator',
      restaurant_admin: 'Restaurant Admin',
      company_admin: 'Company Admin',
      employee: 'Employee'
    }
    return labels[role] || role
  }

  const menuItems = getMenuItems()

  const drawerContent = (
    <Box sx={{ width: 280, height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* User Profile Section */}
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

      {/* Role Badge */}
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

      {/* Menu Items */}
      <List sx={{ flex: 1, overflow: 'auto' }}>
        {menuItems.map(item => (
          <ListItem key={item.id} disablePadding sx={{ display: 'block' }}>
            <ListItemButton
              onClick={() => handleMenuClick(item.path)}
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

      {/* Logout Button */}
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
  )

  return (
    <>
      {/* Desktop Sidebar */}
      <Box
        sx={{
          display: { xs: 'none', sm: 'none', md: 'block' },
          width: 280,
          height: '100vh',
          position: 'fixed',
          left: 0,
          top: 0,
          bgcolor: 'background.paper',
          borderRight: 1,
          borderColor: 'divider',
          boxShadow: 1,
          zIndex: 1000
        }}
      >
        {drawerContent}
      </Box>

      {/* Mobile Drawer */}
      <Drawer
        anchor='left'
        open={mobileOpen}
        onClose={() => setMobileOpen(false)}
        sx={{
          display: { xs: 'block', sm: 'block', md: 'none' }
        }}
      >
        {drawerContent}
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
