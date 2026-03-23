import { redirect } from 'next/navigation'

export const metadata = {
  title: 'Home',
  description: 'Home page'
}

const HomePage = () => {
  redirect('/')
}

export default HomePage