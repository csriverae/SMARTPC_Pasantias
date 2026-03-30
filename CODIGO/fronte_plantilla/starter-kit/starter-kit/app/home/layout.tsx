// MUI Imports
import Button from '@mui/material/Button'
import Box from '@mui/material/Box'

// Layout Imports
import LayoutWrapper from '@layouts/LayoutWrapper'
import VerticalLayout from '@layouts/VerticalLayout'
import HorizontalLayout from '@layouts/HorizontalLayout'

// Component Imports
import Providers from '@components/Providers'
import Header from '@components/layout/horizontal/Header'
import Navbar from '@components/layout/vertical/Navbar'
import VerticalFooter from '@components/layout/vertical/Footer'
import HorizontalFooter from '@components/layout/horizontal/Footer'
import ScrollToTop from '@core/components/scroll-to-top'
import DashboardSidebar from '@components/DashboardSidebar'

// Util Imports
import { getMode, getSystemMode } from '@core/utils/serverHelpers'

const Layout = async props => {
  const { children } = props

  // Vars
  const direction = 'ltr'
  const mode = await getMode()
  const systemMode = await getSystemMode()

  return (
    <Providers direction={direction}>
      <LayoutWrapper
        systemMode={systemMode}
        verticalLayout={
          <Box sx={{ display: 'flex' }}>
            {/* Animated Sidebar */}
            <DashboardSidebar />
            
            {/* Main Content with margin for collapsed sidebar */}
            <Box sx={{ flex: 1, ml: { xs: 0, md: '60px' }, display: 'flex', flexDirection: 'column', minHeight: '100vh', transition: 'margin-left 0.3s ease-in-out' }}>
              <VerticalLayout navbar={<Navbar />} footer={<VerticalFooter />}>
                {children}
              </VerticalLayout>
            </Box>
          </Box>
        }
        horizontalLayout={
          <Box sx={{ display: 'flex' }}>
            {/* Animated Sidebar */}
            <DashboardSidebar />
            
            {/* Main Content with margin for collapsed sidebar */}
            <Box sx={{ flex: 1, ml: { xs: 0, md: '60px' }, display: 'flex', flexDirection: 'column', minHeight: '100vh', transition: 'margin-left 0.3s ease-in-out' }}>
              <HorizontalLayout header={<Header />} footer={<HorizontalFooter />}>
                {children}
              </HorizontalLayout>
            </Box>
          </Box>
        }
      />
      <ScrollToTop className='mui-fixed'>
        <Button variant='contained' className='is-10 bs-10 rounded-full p-0 min-is-0 flex items-center justify-center'>
          <i className='tabler-arrow-up' />
        </Button>
      </ScrollToTop>
    </Providers>
  )
}

export default Layout

