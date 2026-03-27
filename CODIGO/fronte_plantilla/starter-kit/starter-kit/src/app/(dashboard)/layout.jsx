// MUI Imports
import Button from '@mui/material/Button'

// Component Imports
import Providers from '@components/Providers'
import DashboardLayoutClientWrapper from '@components/layout/DashboardLayoutClientWrapper'
import ScrollToTop from '@core/components/scroll-to-top'

const Layout = async props => {
  const { children } = props

  return (
    <Providers direction='ltr'>
      <DashboardLayoutClientWrapper>
        {children}
      </DashboardLayoutClientWrapper>
      <ScrollToTop className='mui-fixed'>
        <Button variant='contained' className='is-10 bs-10 rounded-full p-0 min-is-0 flex items-center justify-center'>
          <i className='tabler-arrow-up' />
        </Button>
      </ScrollToTop>
    </Providers>
  )
}

export default Layout
