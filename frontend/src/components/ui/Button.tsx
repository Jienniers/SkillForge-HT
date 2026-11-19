import type { ButtonHTMLAttributes, PropsWithChildren } from 'react'

type Props = PropsWithChildren<ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary' | 'quiet' }>
const styles = {
  primary: 'bg-indigo-600 text-white hover:bg-indigo-500',
  secondary: 'border border-slate-200 bg-white text-slate-700 hover:bg-slate-50',
  quiet: 'border border-white/10 text-slate-300 hover:bg-white/5',
}
export function Button({ variant = 'secondary', className = '', children, ...props }: Props) {
  return <button className={`rounded-lg px-4 py-2 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-60 ${styles[variant]} ${className}`} {...props}>{children}</button>
}
