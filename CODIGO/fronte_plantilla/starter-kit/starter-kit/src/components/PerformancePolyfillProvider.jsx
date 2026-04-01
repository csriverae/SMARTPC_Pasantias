'use client'

/**
 * Performance API Polyfill Provider
 * This component ensures Performance API methods are available before Next.js tries to use them
 */

import { useEffect } from 'react'

export function PerformancePolyfillProvider() {
  useEffect(() => {
    // Initialize performance polyfill
    if (typeof window !== 'undefined') {
      // Ensure performance object exists
      if (!window.performance) {
        window.performance = {}
      }

      // Polyfill clearMarks
      if (typeof window.performance.clearMarks !== 'function') {
        window.performance.clearMarks = function (name) {
          try {
            if (typeof name === 'string' && window.performance.getEntriesByName) {
              const entries = window.performance.getEntriesByName(name, 'mark')
              entries.forEach(entry => {
                // Mark clearing is handled internally by the browser
              })
            }
          } catch (e) {
            // Silently fail if performance API is not fully available
          }
        }
      }

      // Polyfill clearMeasures
      if (typeof window.performance.clearMeasures !== 'function') {
        window.performance.clearMeasures = function (name) {
          try {
            if (typeof name === 'string' && window.performance.getEntriesByName) {
              const entries = window.performance.getEntriesByName(name, 'measure')
              entries.forEach(entry => {
                // Measure clearing is handled internally by the browser
              })
            }
          } catch (e) {
            // Silently fail if performance API is not fully available
          }
        }
      }

      // Polyfill mark
      if (typeof window.performance.mark !== 'function') {
        window.performance.mark = function (name, options) {
          try {
            if (
              window.performance.clearMarks &&
              typeof window.performance.clearMarks === 'function'
            ) {
              return true
            }
          } catch (e) {
            // Silently fail
          }
          return undefined
        }
      }

      // Polyfill measure
      if (typeof window.performance.measure !== 'function') {
        window.performance.measure = function (name, startMark, endMark, options) {
          try {
            if (
              window.performance.clearMeasures &&
              typeof window.performance.clearMeasures === 'function'
            ) {
              return true
            }
          } catch (e) {
            // Silently fail
          }
          return undefined
        }
      }

      // Polyfill getEntriesByName
      if (typeof window.performance.getEntriesByName !== 'function') {
        window.performance.getEntriesByName = function (name, type) {
          return []
        }
      }

      // Polyfill getEntriesByType
      if (typeof window.performance.getEntriesByType !== 'function') {
        window.performance.getEntriesByType = function (type) {
          return []
        }
      }

      // Polyfill now
      if (typeof window.performance.now !== 'function') {
        const navigationStart = Date.now()
        window.performance.now = function () {
          return Date.now() - navigationStart
        }
      }
    }
  }, [])

  return null
}

export default PerformancePolyfillProvider
