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
  Chip,
  Stack,
} from '@mui/material'
import { useRestaurants, useTenantFromToken } from '@core/hooks/useApi'
import CreateRestaurantModal, { RestaurantFormData } from '@components/modals/CreateRestaurantModal'

interface Restaurant {
  id: number
  name: string
  description?: string
  address?: string
  phone?: string
  email?: string
  tenant_id: number
  created_at: string
  is_active?: number
}

export default function RestaurantsPage() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([])
  const [openModal, setOpenModal] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [successMessage, setSuccessMessage] = useState('')
  const [currentTenantId, setCurrentTenantId] = useState<number | null>(null)

  const { createRestaurant, listRestaurants, deleteRestaurant, loading, error } = useRestaurants()
  const { tenantId, extractTenantId } = useTenantFromToken()

  // Extraer tenant_id del token al montar
  useEffect(() => {
    const id = extractTenantId()
    if (id) {
      setCurrentTenantId(id)
    } else {
      // Si no hay token válido, redirigir al login
      window.location.href = '/login'
    }
  }, [])

  // Cargar restaurants cuando tenemos el tenant_id
  useEffect(() => {
    if (currentTenantId) {
      loadRestaurants()
    }
  }, [currentTenantId])

  const loadRestaurants = async () => {
    setIsLoading(true)
    const response = await listRestaurants()
    if (response) {
      const data = Array.isArray(response.data) ? response.data : response.data?.data || []
      setRestaurants(data)
    }
    setIsLoading(false)
  }

  const handleCreateRestaurant = async (formData: RestaurantFormData) => {
    const response = await createRestaurant(formData)
    if (response && !response.error) {
      setSuccessMessage(`Restaurante "${formData.name}" creado exitosamente`)
      setOpenModal(false)
      loadRestaurants()
      setTimeout(() => setSuccessMessage(''), 3000)
    }
  }

  const handleDeleteRestaurant = async (restaurantId: number, restaurantName: string) => {
    if (window.confirm(`¿Estás seguro de que deseas eliminar "${restaurantName}"?`)) {
      const response = await deleteRestaurant(restaurantId)
      if (response && !response.error) {
        setSuccessMessage('Restaurante eliminado exitosamente')
        loadRestaurants()
        setTimeout(() => setSuccessMessage(''), 3000)
      }
    }
  }

  return (
    <Box sx={{ p: 4 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" component="h1">
            🍽️ Gestión de Restaurantes
          </Typography>
          {currentTenantId && (
            <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
              Tenant ID: {currentTenantId}
            </Typography>
          )}
        </Box>
        <Button variant="contained" color="primary" onClick={() => setOpenModal(true)}>
          + Crear Restaurante
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
      ) : restaurants.length === 0 ? (
        <Card>
          <CardContent>
            <Typography color="textSecondary">
              No hay restaurantes creados para este tenant. ¡Crea uno para comenzar!
            </Typography>
          </CardContent>
        </Card>
      ) : (
        <Grid container spacing={3}>
          {restaurants.map((restaurant) => (
            <Grid item xs={12} sm={6} md={4} key={restaurant.id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flex: 1 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                    <Box sx={{ flex: 1 }}>
                      <Typography variant="h6" component="div">
                        {restaurant.name}
                      </Typography>
                      {restaurant.is_active && (
                        <Chip
                          label="Activo"
                          size="small"
                          color="success"
                          variant="outlined"
                          sx={{ mt: 1 }}
                        />
                      )}
                    </Box>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <Button variant="text" size="small" disabled>
                        ✏️ Editar
                      </Button>
                      <Button
                        variant="text"
                        size="small"
                        color="error"
                        onClick={() => handleDeleteRestaurant(restaurant.id, restaurant.name)}
                        disabled={loading}
                      >
                        🗑️ Eliminar
                      </Button>
                    </Box>
                  </Box>

                  <Stack spacing={1}>
                    <Typography variant="body2" color="textSecondary">
                      <strong>ID:</strong> {restaurant.id}
                    </Typography>
                    {restaurant.description && (
                      <Typography variant="body2">
                        <strong>Descripción:</strong> {restaurant.description}
                      </Typography>
                    )}
                    {restaurant.address && (
                      <Typography variant="body2" color="textSecondary">
                        <strong>Dirección:</strong> {restaurant.address}
                      </Typography>
                    )}
                    {restaurant.phone && (
                      <Typography variant="body2" color="textSecondary">
                        <strong>Teléfono:</strong> {restaurant.phone}
                      </Typography>
                    )}
                    {restaurant.email && (
                      <Typography variant="body2" color="textSecondary">
                        <strong>Email:</strong> {restaurant.email}
                      </Typography>
                    )}
                    <Typography variant="body2" color="textSecondary">
                      <strong>Creado:</strong> {new Date(restaurant.created_at).toLocaleDateString()}
                    </Typography>
                  </Stack>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Modal */}
      <CreateRestaurantModal
        open={openModal}
        onClose={() => setOpenModal(false)}
        onSuccess={handleCreateRestaurant}
        loading={loading}
        error={error?.message}
      />
    </Box>
  )
}
