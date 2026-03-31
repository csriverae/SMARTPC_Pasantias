'use client'

import React, { useState } from 'react'
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material'

interface CreateRestaurantModalProps {
  open: boolean
  onClose: () => void
  onSuccess: (data: RestaurantFormData) => void
  loading?: boolean
  error?: string | null
}

export interface RestaurantFormData {
  name: string
  description?: string
  address?: string
  phone?: string
  email?: string
}

export const CreateRestaurantModal: React.FC<CreateRestaurantModalProps> = ({
  open,
  onClose,
  onSuccess,
  loading = false,
  error = null,
}) => {
  const [formData, setFormData] = useState<RestaurantFormData>({
    name: '',
    description: '',
    address: '',
    phone: '',
    email: '',
  })

  const handleChange = (field: keyof RestaurantFormData, value: string) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }))
  }

  const handleSubmit = () => {
    if (formData.name.trim()) {
      onSuccess(formData)
      setFormData({
        name: '',
        description: '',
        address: '',
        phone: '',
        email: '',
      })
    }
  }

  const handleClose = () => {
    setFormData({
      name: '',
      description: '',
      address: '',
      phone: '',
      email: '',
    })
    onClose()
  }

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Crear Nuevo Restaurante</DialogTitle>
      <DialogContent>
        <Box sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          {error && <Alert severity="error">{error}</Alert>}
          <TextField
            fullWidth
            label="Nombre *"
            placeholder="ej: Pizza Paradise"
            value={formData.name}
            onChange={(e) => handleChange('name', e.target.value)}
            disabled={loading}
            autoFocus
          />
          <TextField
            fullWidth
            label="Descripción"
            placeholder="ej: Pizzería de fuego lento"
            value={formData.description}
            onChange={(e) => handleChange('description', e.target.value)}
            disabled={loading}
            multiline
            rows={2}
          />
          <TextField
            fullWidth
            label="Dirección"
            placeholder="ej: Calle Principal 123, Ciudad"
            value={formData.address}
            onChange={(e) => handleChange('address', e.target.value)}
            disabled={loading}
          />
          <TextField
            fullWidth
            label="Teléfono"
            placeholder="ej: +34-912345678"
            value={formData.phone}
            onChange={(e) => handleChange('phone', e.target.value)}
            disabled={loading}
          />
          <TextField
            fullWidth
            label="Email"
            placeholder="ej: contact@pizza.com"
            value={formData.email}
            onChange={(e) => handleChange('email', e.target.value)}
            disabled={loading}
            type="email"
          />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} disabled={loading}>
          Cancelar
        </Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={loading || !formData.name.trim()}
        >
          {loading ? <CircularProgress size={24} /> : 'Crear'}
        </Button>
      </DialogActions>
    </Dialog>
  )
}

export default CreateRestaurantModal
