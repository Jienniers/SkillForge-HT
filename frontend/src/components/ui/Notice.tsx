export function Notice({ children, onDismiss }: { children: string; onDismiss: () => void }) {
  return <div role="status" className="mb-5 flex items-start justify-between gap-3 rounded-xl border border-amber-400/30 bg-amber-500/10 p-4 text-sm text-amber-200"><span>{children}</span><button onClick={onDismiss} aria-label="Dismiss notice" className="text-amber-200 hover:text-white">×</button></div>
}
