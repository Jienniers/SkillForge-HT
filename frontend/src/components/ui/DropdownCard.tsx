import type { PropsWithChildren } from 'react'

export function DropdownCard({ title, children, open = false }: PropsWithChildren<{ title: string; open?: boolean }>) {
  return <details open={open} className="self-start rounded-xl border border-slate-200 bg-white">
    <summary className="flex cursor-pointer list-none items-center justify-between gap-3 p-4 font-semibold">{title}<span className="shrink-0 text-slate-400">⌄</span></summary>
    <div className="border-t border-slate-100 px-4 py-3 text-sm">{children}</div>
  </details>
}
