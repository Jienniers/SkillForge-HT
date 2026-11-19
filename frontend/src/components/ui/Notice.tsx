export function Notice({ children, onDismiss }: { children: string; onDismiss: () => void }) {
  return <div role="status" className="mb-5 flex items-start justify-between gap-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900"><span>{children}</span><button onClick={onDismiss} aria-label="Dismiss notice">×</button></div>
}
