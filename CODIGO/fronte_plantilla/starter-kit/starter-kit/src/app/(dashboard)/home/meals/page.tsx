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
  MenuItem,
  IconButton,
  Chip
} from '@mui/material'
import { Add, Edit, Delete } from '@mui/icons-material'
import { DatePicker } from '@mui/x-date-pickers/DatePicker'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import dayjs from 'dayjs'

interface MealLog {
  id: number
  employee_id: number
  agreement_id: number
  date: string
  meal_type: string
  employee_name?: string
  agreement_name?: string
}

const MealsPage = () => {
  const [mealLogs, setMealLogs] = useState<MealLog[]>([])
  const [loading, setLoading] = useState(true)
  const [open, setOpen] = useState(false)
  const [editingLog, setEditingLog] = useState<MealLog | null>(null)
  const [formData, setFormData] = useState({
    employee_id: '',
    agreement_id: '',
    date: dayjs(),
    meal_type: ''
  })

  useEffect(() => {
    fetchMealLogs()
  }, [])

  const fetchMealLogs = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/meal-logs', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        setMealLogs(data)
      } else {
        console.error('Failed to fetch meal logs')
      }
    } catch (error) {
      console.error('Error fetching meal logs:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleOpenDialog = (log?: MealLog) => {
    if (log) {
      setEditingLog(log)
      setFormData({
        employee_id: log.employee_id.toString(),
        agreement_id: log.agreement_id.toString(),
        date: dayjs(log.date),
        meal_type: log.meal_type
      })
    } else {
      setEditingLog(null)
      setFormData({
        employee_id: '',
        agreement_id: '',
        date: dayjs(),
        meal_type: ''
      })
    }
    setOpen(true)
  }

  const handleCloseDialog = () => {
    setOpen(false)
    setEditingLog(null)
  }

  const handleSubmit = async () => {
    try {
      const token = localStorage.getItem('token')
      const method = editingLog ? 'PUT' : 'POST'
      const url = editingLog ? `/api/meal-logs/${editingLog.id}` : '/api/meal-logs'

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          ...formData,
          employee_id: parseInt(formData.employee_id),
          agreement_id: parseInt(formData.agreement_id),
          date: formData.date.format('YYYY-MM-DD')
        })
      })

      if (response.ok) {
        fetchMealLogs()
        handleCloseDialog()
      } else {
        console.error('Failed to save meal log')
      }
    } catch (error) {
      console.error('Error saving meal log:', error)
    }
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este registro de comida?')) {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`/api/meal-logs/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.ok) {
          fetchMealLogs()
        } else {
          console.error('Failed to delete meal log')
        }
      } catch (error) {
        console.error('Error deleting meal log:', error)
      }
    }
  }

  const getMealTypeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case 'lunch':
        return 'primary'
      case 'dinner':
        return 'secondary'
      default:
        return 'default'
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Typography>Cargando registros de comidas...</Typography>
      </Box>
    )
  }

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Box sx={{ p: 3 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h4" component="h1">
            Registros de Comidas
          </Typography>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => handleOpenDialog()}
          >
            Agregar Registro
          </Button>
        </Box>

        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Empleado</TableCell>
                <TableCell>Acuerdo</TableCell>
                <TableCell>Fecha</TableCell>
                <TableCell>Tipo de Comida</TableCell>
                <TableCell>Acciones</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {mealLogs.map((log) => (
                <TableRow key={log.id}>
                  <TableCell>{log.id}</TableCell>
                  <TableCell>{log.employee_name || `Empleado ${log.employee_id}`}</TableCell>
                  <TableCell>{log.agreement_name || `Acuerdo ${log.agreement_id}`}</TableCell>
                  <TableCell>{dayjs(log.date).format('DD/MM/YYYY')}</TableCell>
                  <TableCell>
                    <Chip
                      label={log.meal_type}
                      color={getMealTypeColor(log.meal_type)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <IconButton
                      color="primary"
                      onClick={() => handleOpenDialog(log)}
                    >
                      <Edit />
                    </IconButton>
                    <IconButton
                      color="error"
                      onClick={() => handleDelete(log.id)}
                    >
                      <Delete />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        {mealLogs.length === 0 && (
          <Box textAlign="center" mt={3}>
            <Typography variant="body1" color="text.secondary">
              No hay registros de comidas aún.
            </Typography>
          </Box>
        )}

        <Dialog open={open} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
          <DialogTitle>
            {editingLog ? 'Editar Registro de Comida' : 'Agregar Registro de Comida'}
          </DialogTitle>
          <DialogContent>
            <Box sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
              <TextField
                label="ID de Empleado"
                type="number"
                value={formData.employee_id}
                onChange={(e) => setFormData({ ...formData, employee_id: e.target.value })}
                fullWidth
              />
              <TextField
                label="ID de Acuerdo"
                type="number"
                value={formData.agreement_id}
                onChange={(e) => setFormData({ ...formData, agreement_id: e.target.value })}
                fullWidth
              />
              <DatePicker
                label="Fecha"
                value={formData.date}
                onChange={(date) => setFormData({ ...formData, date: date || dayjs() })}
                slotProps={{ textField: { fullWidth: true } }}
              />
              <TextField
                select
                label="Tipo de Comida"
                value={formData.meal_type}
                onChange={(e) => setFormData({ ...formData, meal_type: e.target.value })}
                fullWidth
              >
                <MenuItem value="lunch">Almuerzo</MenuItem>
                <MenuItem value="dinner">Cena</MenuItem>
              </TextField>
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Cancelar</Button>
            <Button onClick={handleSubmit} variant="contained">
              {editingLog ? 'Actualizar' : 'Crear'}
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </LocalizationProvider>
  )
}

export default MealsPage