'use client'

import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  IconButton,
  Chip,
  Card,
  CardContent,
  Grid
} from '@mui/material'
import { Add, Edit, Delete, LocationOn, Phone, Email } from '@mui/icons-material'

interface Restaurant {
  id: number
  tenant_id: number
  name: string
  description: string
  address: string
  phone: string
  email: string
  latitude: number
  longitude: number
  is_active: boolean
  created_at: string
  updated_at: string
}

const RestaurantsPage = () => {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([])
  const [loading, setLoading] = useState(true)
  const [open, setOpen] = useState(false)
  const [editingRestaurant, setEditingRestaurant] = useState<Restaurant | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    address: '',
    phone: '',
    email: '',
    latitude: '',
    longitude: ''
  })

  useEffect(() => {
    fetchRestaurants()
  }, [])

  const fetchRestaurants = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/restaurants', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        setRestaurants(data)
      } else {
        console.error('Failed to fetch restaurants')
      }
    } catch (error) {
      console.error('Error fetching restaurants:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleOpenDialog = (restaurant?: Restaurant) => {
    if (restaurant) {
      setEditingRestaurant(restaurant)
      setFormData({
        name: restaurant.name,
        description: restaurant.description || '',
        address: restaurant.address || '',
        phone: restaurant.phone || '',
        email: restaurant.email || '',
        latitude: restaurant.latitude?.toString() || '',
        longitude: restaurant.longitude?.toString() || ''
      })
    } else {
      setEditingRestaurant(null)
      setFormData({
        name: '',
        description: '',
        address: '',
        phone: '',
        email: '',
        latitude: '',
        longitude: ''
      })
    }
    setOpen(true)
  }

  const handleCloseDialog = () => {
    setOpen(false)
    setEditingRestaurant(null)
  }

  const handleSubmit = async () => {
    try {
      const token = localStorage.getItem('token')
      const method = editingRestaurant ? 'PUT' : 'POST'
      const url = editingRestaurant ? `/api/restaurants/${editingRestaurant.id}` : '/api/restaurants'

      const payload = {
        name: formData.name,
        description: formData.description,
        address: formData.address,
        phone: formData.phone,
        email: formData.email,
        latitude: formData.latitude ? parseFloat(formData.latitude) : null,
        longitude: formData.longitude ? parseFloat(formData.longitude) : null
      }

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      })

      if (response.ok) {
        fetchRestaurants()
        handleCloseDialog()
      } else {
        const error = await response.json()
        console.error('Failed to save restaurant:', error)
        alert('Error al guardar restaurante: ' + (error.detail || 'Error desconocido'))
      }
    } catch (error) {
      console.error('Error saving restaurant:', error)
      alert('Error al guardar restaurante')
    }
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este restaurante?')) {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`/api/restaurants/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.ok) {
          fetchRestaurants()
        } else {
          console.error('Failed to delete restaurant')
        }
      } catch (error) {
        console.error('Error deleting restaurant:', error)
      }
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Typography>Cargando restaurantes...</Typography>
      </Box>
    )
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Gestión de Restaurantes
        </Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
        >
          Agregar Restaurante
        </Button>
      </Box>

      <Grid container spacing={3}>
        {restaurants.map((restaurant) => (
          <Grid item xs={12} md={6} lg={4} key={restaurant.id}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
                  <Typography variant="h6" component="h2">
                    {restaurant.name}
                  </Typography>
                  <Box>
                    <IconButton
                      size="small"
                      color="primary"
                      onClick={() => handleOpenDialog(restaurant)}
                    >
                      <Edit />
                    </IconButton>
                    <IconButton
                      size="small"
                      color="error"
                      onClick={() => handleDelete(restaurant.id)}
                    >
                      <Delete />
                    </IconButton>
                  </Box>
                </Box>

                {restaurant.description && (
                  <Typography variant="body2" color="text.secondary" mb={2}>
                    {restaurant.description}
                  </Typography>
                )}

                <Box display="flex" flexDirection="column" gap={1}>
                  {restaurant.address && (
                    <Box display="flex" alignItems="center" gap={1}>
                      <LocationOn fontSize="small" color="action" />
                      <Typography variant="body2">{restaurant.address}</Typography>
                    </Box>
                  )}

                  {restaurant.phone && (
                    <Box display="flex" alignItems="center" gap={1}>
                      <Phone fontSize="small" color="action" />
                      <Typography variant="body2">{restaurant.phone}</Typography>
                    </Box>
                  )}

                  {restaurant.email && (
                    <Box display="flex" alignItems="center" gap={1}>
                      <Email fontSize="small" color="action" />
                      <Typography variant="body2">{restaurant.email}</Typography>
                    </Box>
                  )}
                </Box>

                <Box mt={2}>
                  <Chip
                    label={restaurant.is_active ? 'Activo' : 'Inactivo'}
                    color={restaurant.is_active ? 'success' : 'error'}
                    size="small"
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {restaurants.length === 0 && (
        <Box textAlign="center" mt={3}>
          <Typography variant="body1" color="text.secondary">
            No hay restaurantes registrados aún.
          </Typography>
        </Box>
      )}

      <Dialog open={open} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingRestaurant ? 'Editar Restaurante' : 'Agregar Restaurante'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Nombre"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              fullWidth
              required
            />
            <TextField
              label="Descripción"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              fullWidth
              multiline
              rows={3}
            />
            <TextField
              label="Dirección"
              value={formData.address}
              onChange={(e) => setFormData({ ...formData, address: e.target.value })}
              fullWidth
            />
            <TextField
              label="Teléfono"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              fullWidth
            />
            <TextField
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              fullWidth
            />
            <Box display="flex" gap={2}>
              <TextField
                label="Latitud"
                type="number"
                value={formData.latitude}
                onChange={(e) => setFormData({ ...formData, latitude: e.target.value })}
                fullWidth
              />
              <TextField
                label="Longitud"
                type="number"
                value={formData.longitude}
                onChange={(e) => setFormData({ ...formData, longitude: e.target.value })}
                fullWidth
              />
            </Box>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancelar</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingRestaurant ? 'Actualizar' : 'Crear'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}

export default RestaurantsPage