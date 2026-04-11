'use client'

// Next Imports
import Link from 'next/link'

// Third-party Imports
import classnames from 'classnames'

// Hook Imports
import useHorizontalNav from '@menu/hooks/useHorizontalNav'

// Util Imports
import { horizontalLayoutClasses } from '@layouts/utils/layoutClasses'

const FooterContent = () => {
  // Hooks
  const { isBreakpointReached } = useHorizontalNav()

  return (
    <div
      className={classnames(horizontalLayoutClasses.footerContent, 'flex items-center justify-between flex-wrap gap-4')}
    >
      <p>
        <span className='text-textSecondary'>{`© ${new Date().getFullYear()}, `}</span>
        <span className='text-primary uppercase'>MesaPass</span>
      </p>
      {!isBreakpointReached && (
        <div className='flex items-center gap-4'>
          <Link href='/faq' className='text-primary'>
            Ayuda
          </Link>
          <Link href='/pricing' className='text-primary'>
            Planes
          </Link>
          <Link href='/settings' className='text-primary'>
            Configuración
          </Link>
        </div>
      )}
    </div>
  )
}

export default FooterContent
