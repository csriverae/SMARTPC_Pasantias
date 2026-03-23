'use client'

import { Fragment, useEffect } from 'react'
import { useRouter } from 'next/navigation'

// MUI Imports
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardHeader from '@mui/material/CardHeader'
import Grid from '@mui/material/Grid'
import Typography from '@mui/material/Typography'
import Chip from '@mui/material/Chip'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Paper from '@mui/material/Paper'

const stats = [
  { label: 'Usuarios', value: '1,280', icon: 'tabler-users', change: '+14%', color: '#28c76f' },
  { label: 'Ingresos', value: '$25,400', icon: 'tabler-dollar-sign', change: '+8%', color: '#00cfe9' },
  { label: 'Órdenes', value: '455', icon: 'tabler-shopping-cart', change: '+5%', color: '#ff9f43' },
  { label: 'Sesiones', value: '7,922', icon: 'tabler-activity', change: '+10%', color: '#9f63ff' }
]

const transactions = [
  { id: '001', email: 'admin@mesapass.com', amount: '$1,250', status: 'Completado', statusColor: 'success' },
  { id: '002', email: 'user@mesapass.com', amount: '$890', status: 'Pendiente', statusColor: 'warning' },
  { id: '003', email: 'rest@mesapass.com', amount: '$2,100', status: 'Completado', statusColor: 'success' }
]

export default function HomePage() {
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
    }
  }, [router])

  return (
    <Fragment>
      <Grid container spacing={6}>
        {/* Header */}
        <Grid item xs={12}>
          <div>
            <Typography variant='h4' sx={{ mb: 1 }}>
              Dashboard
            </Typography>
            <Typography variant='body2' color='textSecondary'>
              Bienvenido a Mesapass (Fase 1): tu panel principal con datos de ejemplo y diseño Vuexy.
            </Typography>
          </div>
        </Grid>

        {/* Stats Cards */}
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card>
              <CardContent>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div>
                    <Typography variant='caption' color='textSecondary' sx={{ display: 'block', mb: 0.5 }}>
                      {stat.label}
                    </Typography>
                    <Typography variant='h6' sx={{ fontWeight: 600 }}>
                      {stat.value}
                    </Typography>
                  </div>
                  <div style={{ textAlign: 'center', padding: '8px 12px', backgroundColor: stat.color + '20', borderRadius: '8px' }}>
                    <i className={stat.icon} style={{ color: stat.color, fontSize: '24px' }}></i>
                  </div>
                </div>
                <Typography variant='caption' sx={{ color: '#28c76f', display: 'block', mt: 1 }}>
                  {stat.change} desde la última semana
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}

        {/* Transactions Table */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title='Últimas transacciones' />
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                    <TableCell>ID</TableCell>
                    <TableCell>Email</TableCell>
                    <TableCell>Monto</TableCell>
                    <TableCell>Estado</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {transactions.map((tx) => (
                    <TableRow key={tx.id}>
                      <TableCell variant='head'>{tx.id}</TableCell>
                      <TableCell>{tx.email}</TableCell>
                      <TableCell>{tx.amount}</TableCell>
                      <TableCell>
                        <Chip label={tx.status} color={tx.statusColor as any} size='small' />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Card>
        </Grid>
      </Grid>
    </Fragment>
  )
}