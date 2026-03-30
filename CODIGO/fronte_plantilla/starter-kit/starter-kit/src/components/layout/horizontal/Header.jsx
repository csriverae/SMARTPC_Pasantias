'use client'

// Component Imports
import NavbarContent from './NavbarContent'
import Navbar from '@layouts/components/horizontal/Navbar'
import LayoutHeader from '@layouts/components/horizontal/Header'

const Header = () => {
  return (
    <LayoutHeader>
      <Navbar>
        <NavbarContent />
      </Navbar>
    </LayoutHeader>
  )
}

export default Header
