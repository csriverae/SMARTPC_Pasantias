'use client'

export function TextField({
  label,
  name,
  type = 'text',
  value,
  onChange,
  error = null,
  required = false,
  placeholder = '',
  disabled = false,
  help = null
}) {
  return (
    <div className='space-y-2'>
      {label && (
        <label className='block text-sm font-medium text-gray-700'>
          {label}
          {required && <span className='text-red-500 ml-1'>*</span>}
        </label>
      )}
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        disabled={disabled}
        className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed transition ${
          error ? 'border-red-500' : 'border-gray-300'
        }`}
      />
      {error && <p className='text-sm text-red-600'>{error}</p>}
      {help && <p className='text-sm text-gray-500'>{help}</p>}
    </div>
  )
}

export function SelectField({
  label,
  name,
  value,
  onChange,
  options = [],
  error = null,
  required = false,
  placeholder = 'Seleccionar...',
  disabled = false
}) {
  return (
    <div className='space-y-2'>
      {label && (
        <label className='block text-sm font-medium text-gray-700'>
          {label}
          {required && <span className='text-red-500 ml-1'>*</span>}
        </label>
      )}
      <select
        name={name}
        value={value}
        onChange={onChange}
        disabled={disabled}
        className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed transition ${
          error ? 'border-red-500' : 'border-gray-300'
        }`}
      >
        <option value=''>{placeholder}</option>
        {options.map(opt => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      {error && <p className='text-sm text-red-600'>{error}</p>}
    </div>
  )
}

export function TextAreaField({
  label,
  name,
  value,
  onChange,
  error = null,
  required = false,
  placeholder = '',
  disabled = false,
  rows = 4
}) {
  return (
    <div className='space-y-2'>
      {label && (
        <label className='block text-sm font-medium text-gray-700'>
          {label}
          {required && <span className='text-red-500 ml-1'>*</span>}
        </label>
      )}
      <textarea
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        disabled={disabled}
        rows={rows}
        className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed transition resize-none ${
          error ? 'border-red-500' : 'border-gray-300'
        }`}
      />
      {error && <p className='text-sm text-red-600'>{error}</p>}
    </div>
  )
}

export function CheckboxField({
  label,
  name,
  checked,
  onChange,
  error = null,
  disabled = false
}) {
  return (
    <div className='space-y-2'>
      <label className='flex items-center gap-2 cursor-pointer'>
        <input
          type='checkbox'
          name={name}
          checked={checked}
          onChange={onChange}
          disabled={disabled}
          className='w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-2 focus:ring-indigo-500'
        />
        <span className='text-sm text-gray-700'>{label}</span>
      </label>
      {error && <p className='text-sm text-red-600'>{error}</p>}
    </div>
  )
}
