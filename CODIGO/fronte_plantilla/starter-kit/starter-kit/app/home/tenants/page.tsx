'use client'

import React, { useEffect, useState } from 'react'
import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Grid,
  Alert,
  IconButton,
  Tooltip,
  Typography,
} from '@mui/material'
import { useTenants } from '@core/hooks/useApi'
import CreateTenantModal from '@components/modals/CreateTenantModal'
import DeleteIcon from '@mui/icons-material/Delete'
import EditIcon from '@mui/icons-material/Edit'

interface Tenant {
  id: number
  name: string
  created_at: string
  users_count?: number
  restaurant_count?: number
}

export default function TenantsPage() {
  const [tenants, setTenants] = useState<Tenant[]>([])
  const [openModal, setOpenModal] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [successMessage, setSuccessMessage] = useState('')

  const { createTenant, listTenants, deleteTenant, loading, error } = useTenants()

  // Cargar tenants al montar el componente
  useEffect(() => {
    loadTenants()
  }, [])

  const loadTenants = async () => {
    setIsLoading(true)
    const response = await listTenants()
    if (response) {
      // Si response.data es un array, úsalo; si es un objeto con data, úsalo
      const data = Array.isArray(response.data) ? response.data : response.data?.data || []
      setTenants(data)
    }
    setIsLoading(false)
  }

  const handleCreateTenant = async (tenantName: string) => {
    const response = await createTenant(tenantName)
    if (response && !response.error) {
      setSuccessMessage(`Tenant "${tenantName}" creado exitosamente`)
      setOpenModal(false)
      loadTenants()
      setTimeout(() => setSuccessMessage(''), 3000)
    }
  }

  const handleDeleteTenant = async (tenantId: number, tenantName: string) => {
    if (window.confirm(`¿Estás seguro de que deseas eliminar el tenant "${tenantName}"?`)) {
      const response = await deleteTenant(tenantId)
      if (response && !response.error) {
        setSuccessMessage(`Tenant eliminado exitosamente`)
        loadTenants()
        setTimeout(() => setSuccessMessage(''), 3000)
      }
    }
  }

  return (
    <Box sx={{ p: 4 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          🏢 Gestión de Tenants
        </Typography>
        <Button variant="contained" color="primary" onClick={() => setOpenModal(true)}>
          + Crear Tenant
        </Button>
      </Box>

      {/* Mensajes */}
      {successMessage && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccessMessage('')}>
          {successMessage}
        </Alert>
      )}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error.message}
        </Alert>
      )}

      {/* Loading */}
      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      ) : tenants.length === 0 ? (
        <Card>
          <CardContent>
            <Typography color="textSecondary">
              No hay tenants creados. ¡Crea uno para comenzar!
            </Typography>
          </CardContent>
        </Card>
      ) : (
        <Grid container spacing={3}>
          {tenants.map((tenant) => (
            <Grid item xs={12} sm={6} md={4} key={tenant.id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flex: 1 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                    <Typography variant="h6" component="div" sx={{ flex: 1 }}>
                      {tenant.name}
                    </Typography>
                    <Box>
                      <Tooltip title="Editar">
                        <IconButton size="small" disabled>
                          <EditIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Eliminar">
                        <IconButton
                          size="small"
                          onClick={() => handleDeleteTenant(tenant.id, tenant.name)}
                          disabled={loading}
                        >
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    </Box>
                  </Box>
                  <Typography variant="body2" color="textSecondary" sx={{ mb: 1 }}>
                    <strong>ID:</strong> {tenant.id}
                  </Typography>
                  <Typography variant="body2" color="textSecondary" sx={{ mb: 1 }}>
                    <strong>Creado:</strong> {new Date(tenant.created_at).toLocaleDateString()}
                  </Typography>
                  {tenant.users_count !== undefined && (
                    <Typography variant="body2" color="textSecondary">
                      <strong>Usuarios:</strong> {tenant.users_count}
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Modal */}
      <CreateTenantModal
        open={openModal}
        onClose={() => setOpenModal(false)}
        onSuccess={handleCreateTenant}
        loading={loading}
        error={error?.message}
      />
    </Box>
  )
}
