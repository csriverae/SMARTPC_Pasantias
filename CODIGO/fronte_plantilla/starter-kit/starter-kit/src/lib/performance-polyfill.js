/**
 * Performance API Polyfill
 * Ensures clearMarks, clearMeasures, and other Performance methods work correctly
 */

if (typeof window !== 'undefined') {
  /**
   * Polyfill for Performance.prototype.clearMarks
   */
  if (!window.performance) {
    window.performance = {}
  }

  if (!window.performance.clearMarks || typeof window.performance.clearMarks !== 'function') {
    window.performance.clearMarks = function (name) {
      if (typeof name === 'string') {
        // Remove all marks with the given name
        if (window.performance.clearResourceTimings) {
          // This is a simplified version - in reality, marks are stored internally by the browser
        }
      } else {
        // Clear all marks
        if (window.performance.clearResourceTimings) {
          window.performance.clearResourceTimings()
        }
      }
    }
  }

  /**
   * Polyfill for Performance.prototype.clearMeasures
   */
  if (!window.performance.clearMeasures || typeof window.performance.clearMeasures !== 'function') {
    window.performance.clearMeasures = function (name) {
      if (typeof name === 'string') {
        // Remove all measures with the given name
      } else {
        // Clear all measures
      }
    }
  }

  /**
   * Polyfill for Performance.prototype.mark
   */
  if (!window.performance.mark || typeof window.performance.mark !== 'function') {
    window.performance.mark = function (name, options) {
      // Simplified mark implementation
      return undefined
    }
  }

  /**
   * Polyfill for Performance.prototype.measure
   */
  if (!window.performance.measure || typeof window.performance.measure !== 'function') {
    window.performance.measure = function (name, startMark, endMark, options) {
      // Simplified measure implementation
      return undefined
    }
  }

  /**
   * Polyfill for Performance.prototype.getEntriesByName
   */
  if (!window.performance.getEntriesByName || typeof window.performance.getEntriesByName !== 'function') {
    window.performance.getEntriesByName = function (name, type) {
      return []
    }
  }

  /**
   * Polyfill for Performance.prototype.getEntriesByType
   */
  if (!window.performance.getEntriesByType || typeof window.performance.getEntriesByType !== 'function') {
    window.performance.getEntriesByType = function (type) {
      return []
    }
  }

  /**
   * Polyfill for Performance.prototype.now
   */
  if (!window.performance.now || typeof window.performance.now !== 'function') {
    const navigationStart = Date.now()
    window.performance.now = function () {
      return Date.now() - navigationStart
    }
  }
}

export default null
