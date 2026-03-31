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

interface CreateTenantModalProps {
  open: boolean
  onClose: () => void
  onSuccess: (tenantName: string) => void
  loading?: boolean
  error?: string | null
}

export const CreateTenantModal: React.FC<CreateTenantModalProps> = ({
  open,
  onClose,
  onSuccess,
  loading = false,
  error = null,
}) => {
  const [tenantName, setTenantName] = useState('')

  const handleSubmit = () => {
    if (tenantName.trim()) {
      onSuccess(tenantName)
      setTenantName('')
    }
  }

  const handleClose = () => {
    setTenantName('')
    onClose()
  }

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Crear Nuevo Tenant</DialogTitle>
      <DialogContent>
        <Box sx={{ pt: 2 }}>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <TextField
            fullWidth
            label="Nombre del Tenant"
            placeholder="ej: Quantum Restaurant Group"
            value={tenantName}
            onChange={(e) => setTenantName(e.target.value)}
            disabled={loading}
            autoFocus
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
          disabled={loading || !tenantName.trim()}
        >
          {loading ? <CircularProgress size={24} /> : 'Crear'}
        </Button>
      </DialogActions>
    </Dialog>
  )
}

export default CreateTenantModal
