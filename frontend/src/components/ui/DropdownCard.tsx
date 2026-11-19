import { useId, useState, type PropsWithChildren } from "react";

type DropdownCardProps = PropsWithChildren<{
  title: string;
  defaultOpen?: boolean;
  className?: string;
}>;

export function DropdownCard({
  title,
  children,
  defaultOpen = false,
  className = "",
}: DropdownCardProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const contentId = useId();

  return (
    <section
      className={`self-start overflow-hidden rounded-xl border bg-gradient-to-br from-slate-900 to-slate-900/70 shadow-lg shadow-black/10 transition-colors duration-200 ${isOpen ? "border-indigo-400/50" : "border-slate-700 hover:border-slate-500"} ${className}`}
    >
      <button
        type="button"
        aria-expanded={isOpen}
        aria-controls={contentId}
        onClick={() => setIsOpen((open) => !open)}
        className="group flex w-full items-center justify-between gap-3 px-4 py-3.5 text-left font-semibold text-slate-100 transition-colors hover:bg-white/[0.035] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-indigo-400"
      >
        <span>{title}</span>
        <span
          aria-hidden="true"
          className="grid size-8 shrink-0 place-items-center rounded-lg border border-slate-700 bg-slate-800 text-slate-300"
        >
          <svg
            viewBox="0 0 20 20"
            fill="none"
            className={`size-4 transition-transform duration-200 ease-out ${isOpen ? "rotate-180" : "rotate-0"}`}
          >
            <path
              d="m5 7.5 5 5 5-5"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </span>
      </button>
      <div
        id={contentId}
        aria-hidden={!isOpen}
        inert={!isOpen}
        data-open={isOpen}
        className="dropdown-panel"
      >
        <div className="dropdown-panel-inner">
          <div className="border-t border-slate-700/80 px-4 py-3 text-sm text-slate-300">
            {children}
          </div>
        </div>
      </div>
    </section>
  );
}
