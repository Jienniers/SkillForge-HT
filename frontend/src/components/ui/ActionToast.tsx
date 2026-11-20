export function ActionToast({
  message,
  onDismiss,
}: {
  message: string;
  onDismiss: () => void;
}) {
  if (!message) return null;

  return (
    <div
      role="status"
      aria-live="polite"
      className="busy-toast pointer-events-auto flex max-w-full items-center gap-3 rounded-xl border border-amber-400/30 bg-slate-900 px-4 py-3 text-sm font-medium text-slate-100 shadow-xl shadow-black/30"
    >
      <span
        aria-hidden="true"
        className="grid size-5 shrink-0 place-items-center rounded-full bg-amber-400/15 text-xs font-bold text-amber-300"
      >
        !
      </span>
      <span>{message}</span>
      <button
        type="button"
        onClick={onDismiss}
        aria-label="Dismiss message"
        className="ml-1 rounded px-1 text-slate-400 hover:text-white"
      >
        ×
      </button>
    </div>
  );
}
