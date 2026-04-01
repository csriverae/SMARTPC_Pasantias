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
import { Add, Edit, Delete, Business } from '@mui/icons-material'

interface Tenant {
  id: number
  name: string
  slug: string
  description: string
  is_active: boolean
  created_at: string
  updated_at: string
}

const TenantsPage = () => {
  const [tenants, setTenants] = useState<Tenant[]>([])
  const [loading, setLoading] = useState(true)
  const [open, setOpen] = useState(false)
  const [editingTenant, setEditingTenant] = useState<Tenant | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    slug: '',
    description: ''
  })

  useEffect(() => {
    fetchTenants()
  }, [])

  const fetchTenants = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/tenants', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        setTenants(data)
      } else {
        console.error('Failed to fetch tenants')
      }
    } catch (error) {
      console.error('Error fetching tenants:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleOpenDialog = (tenant?: Tenant) => {
    if (tenant) {
      setEditingTenant(tenant)
      setFormData({
        name: tenant.name,
        slug: tenant.slug,
        description: tenant.description || ''
      })
    } else {
      setEditingTenant(null)
      setFormData({
        name: '',
        slug: '',
        description: ''
      })
    }
    setOpen(true)
  }

  const handleCloseDialog = () => {
    setOpen(false)
    setEditingTenant(null)
  }

  const handleSubmit = async () => {
    try {
      const token = localStorage.getItem('token')
      const method = editingTenant ? 'PUT' : 'POST'
      const url = editingTenant ? `/api/tenants/${editingTenant.id}` : '/api/tenants'

      const payload = {
        name: formData.name,
        slug: formData.slug,
        description: formData.description
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
        fetchTenants()
        handleCloseDialog()
      } else {
        const error = await response.json()
        console.error('Failed to save tenant:', error)
        alert('Error al guardar tenant: ' + (error.detail || 'Error desconocido'))
      }
    } catch (error) {
      console.error('Error saving tenant:', error)
      alert('Error al guardar tenant')
    }
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este tenant?')) {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`/api/tenants/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.ok) {
          fetchTenants()
        } else {
          console.error('Failed to delete tenant')
        }
      } catch (error) {
        console.error('Error deleting tenant:', error)
      }
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Typography>Cargando tenants...</Typography>
      </Box>
    )
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Gestión de Tenants
        </Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
        >
          Agregar Tenant
        </Button>
      </Box>

      <Grid container spacing={3}>
        {tenants.map((tenant) => (
          <Grid item xs={12} md={6} lg={4} key={tenant.id}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
                  <Box>
                    <Typography variant="h6" component="h2">
                      {tenant.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Slug: {tenant.slug}
                    </Typography>
                  </Box>
                  <Box>
                    <IconButton
                      size="small"
                      color="primary"
                      onClick={() => handleOpenDialog(tenant)}
                    >
                      <Edit />
                    </IconButton>
                    <IconButton
                      size="small"
                      color="error"
                      onClick={() => handleDelete(tenant.id)}
                    >
                      <Delete />
                    </IconButton>
                  </Box>
                </Box>

                {tenant.description && (
                  <Typography variant="body2" color="text.secondary" mb={2}>
                    {tenant.description}
                  </Typography>
                )}

                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <Business fontSize="small" color="action" />
                  <Typography variant="body2">
                    ID: {tenant.id}
                  </Typography>
                </Box>

                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Chip
                    label={tenant.is_active ? 'Activo' : 'Inactivo'}
                    color={tenant.is_active ? 'success' : 'error'}
                    size="small"
                  />
                  <Typography variant="caption" color="text.secondary">
                    Creado: {new Date(tenant.created_at).toLocaleDateString('es-ES')}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {tenants.length === 0 && (
        <Box textAlign="center" mt={3}>
          <Typography variant="body1" color="text.secondary">
            No hay tenants registrados aún.
          </Typography>
        </Box>
      )}

      <Dialog open={open} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingTenant ? 'Editar Tenant' : 'Agregar Tenant'}
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
              label="Slug"
              value={formData.slug}
              onChange={(e) => setFormData({ ...formData, slug: e.target.value.toLowerCase().replace(/\s+/g, '-') })}
              fullWidth
              required
              helperText="Identificador único (solo letras, números y guiones)"
            />
            <TextField
              label="Descripción"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              fullWidth
              multiline
              rows={3}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancelar</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingTenant ? 'Actualizar' : 'Crear'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}

export default TenantsPage