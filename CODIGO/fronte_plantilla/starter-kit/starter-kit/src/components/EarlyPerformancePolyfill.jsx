'use client'

import Script from 'next/script'

/**
 * Early Performance Polyfill Script
 * Loads the performance polyfill inline to ensure it's available before any code runs
 */

export function EarlyPerformancePolyfill() {
  const polyfillScript = `
    (function() {
      if (typeof window !== 'undefined') {
        if (!window.performance) {
          window.performance = {}
        }
        
        if (typeof window.performance.clearMarks !== 'function') {
          window.performance.clearMarks = function(name) {
            try {
              if (typeof name === 'string' && window.performance.getEntriesByName) {
                window.performance.getEntriesByName(name, 'mark')
              }
            } catch (e) {}
          }
        }
        
        if (typeof window.performance.clearMeasures !== 'function') {
          window.performance.clearMeasures = function(name) {
            try {
              if (typeof name === 'string' && window.performance.getEntriesByName) {
                window.performance.getEntriesByName(name, 'measure')
              }
            } catch (e) {}
          }
        }
        
        if (typeof window.performance.mark !== 'function') {
          window.performance.mark = function(name, options) {
            return undefined
          }
        }
        
        if (typeof window.performance.measure !== 'function') {
          window.performance.measure = function(name, startMark, endMark) {
            return undefined
          }
        }
        
        if (typeof window.performance.getEntriesByName !== 'function') {
          window.performance.getEntriesByName = function(name, type) {
            return []
          }
        }
        
        if (typeof window.performance.getEntriesByType !== 'function') {
          window.performance.getEntriesByType = function(type) {
            return []
          }
        }
        
        if (typeof window.performance.now !== 'function') {
          var navigationStart = Date.now()
          window.performance.now = function() {
            return Date.now() - navigationStart
          }
        }
      }
    })()
  `

  return <Script id='performance-polyfill' strategy='beforeInteractive' dangerouslySetInnerHTML={{ __html: polyfillScript }} />
}

export default EarlyPerformancePolyfill
