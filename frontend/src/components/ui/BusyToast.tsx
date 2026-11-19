export function BusyToast({ message }: { message: string }) {
  if (!message) return null;

  return (
    <div
      role="status"
      aria-live="polite"
      className="busy-toast fixed right-4 top-4 z-[100] flex max-w-[calc(100vw-2rem)] items-center gap-3 rounded-xl border border-indigo-400/30 bg-slate-900 px-4 py-3 text-sm font-medium text-slate-100 shadow-xl shadow-black/30 md:right-6 md:top-6"
    >
      <span
        aria-hidden="true"
        className="size-4 shrink-0 animate-spin rounded-full border-2 border-indigo-300/30 border-t-indigo-300"
      />
      <span>{message}</span>
    </div>
  );
}
