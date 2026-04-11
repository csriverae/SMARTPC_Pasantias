'use client'

import { useState, useEffect } from 'react'

export function Alert({ type = 'info', message, onClose = null, autoClose = true, timeout = 5000 }) {
  const [isVisible, setIsVisible] = useState(true)

  useEffect(() => {
    if (autoClose && timeout > 0) {
      const timer = setTimeout(() => {
        setIsVisible(false)
        onClose?.()
      }, timeout)
      return () => clearTimeout(timer)
    }
  }, [autoClose, timeout, onClose])

  if (!isVisible) return null

  const bgColors = {
    success: 'bg-green-50 border-green-200',
    error: 'bg-red-50 border-red-200',
    warning: 'bg-yellow-50 border-yellow-200',
    info: 'bg-blue-50 border-blue-200'
  }

  const textColors = {
    success: 'text-green-700',
    error: 'text-red-700',
    warning: 'text-yellow-700',
    info: 'text-blue-700'
  }

  const iconColors = {
    success: 'text-green-600',
    error: 'text-red-600',
    warning: 'text-yellow-600',
    info: 'text-blue-600'
  }

  const icons = {
    success: '✓',
    error: '✕',
    warning: '!',
    info: 'ℹ'
  }

  return (
    <div className={`border-l-4 p-4 rounded flex items-center gap-3 ${bgColors[type]}`}>
      <span className={`text-lg font-bold ${iconColors[type]}`}>{icons[type]}</span>
      <p className={`flex-1 ${textColors[type]}`}>{message}</p>
      {onClose && (
        <button
          onClick={() => {
            setIsVisible(false)
            onClose()
          }}
          className={`${textColors[type]} hover:opacity-70`}
        >
          ✕
        </button>
      )}
    </div>
  )
}

export function AlertContainer({ alerts, clearAlert }) {
  return (
    <div className='fixed top-4 right-4 z-50 space-y-2 max-w-md'>
      {alerts.map((alert, idx) => (
        <Alert
          key={idx}
          type={alert.type}
          message={alert.message}
          onClose={() => clearAlert(idx)}
          autoClose={true}
        />
      ))}
    </div>
  )
}
