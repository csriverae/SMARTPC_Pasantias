'use client'

interface StatsCardProps {
  label: string
  value: number
  icon: string
  bgColor: string
  textColor: string
  tab: string
  onTabChange: (tab: string) => void
}

export default function StatsCard({
  label,
  value,
  icon,
  bgColor,
  textColor,
  tab,
  onTabChange
}: StatsCardProps) {
  return (
    <article
      className='bg-white border border-slate-200 rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer'
      onClick={() => onTabChange(tab)}
    >
      <div className='flex items-center justify-between'>
        <div>
          <p className='text-xs text-slate-400 uppercase tracking-wide'>{label}</p>
          <p className='text-2xl font-semibold text-slate-900'>{value}</p>
        </div>
        <span className={`inline-flex items-center justify-center w-10 h-10 ${bgColor} ${textColor} rounded-lg`}>
          <i className={icon}></i>
        </span>
      </div>
    </article>
  )
}
