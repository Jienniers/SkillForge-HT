import { useEffect, useId, useRef, useState } from "react";

export type SelectOption = { value: string; label: string };

export function Select({
  id,
  value,
  options,
  onChange,
  ariaLabel,
  className = "",
  placement = "bottom",
}: {
  id?: string;
  value: string;
  options: SelectOption[];
  onChange: (value: string) => void;
  ariaLabel: string;
  className?: string;
  placement?: "top" | "bottom";
}) {
  const rootRef = useRef<HTMLDivElement>(null);
  const listId = useId();
  const selectedIndex = Math.max(
    options.findIndex((option) => option.value === value),
    0,
  );
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(selectedIndex);
  const selected = options[selectedIndex];

  useEffect(() => {
    if (!isOpen) return;
    const handlePointerDown = (event: PointerEvent) => {
      if (!rootRef.current?.contains(event.target as Node)) setIsOpen(false);
    };
    document.addEventListener("pointerdown", handlePointerDown);
    return () => document.removeEventListener("pointerdown", handlePointerDown);
  }, [isOpen]);

  function choose(option: SelectOption) {
    onChange(option.value);
    setActiveIndex(options.findIndex((item) => item.value === option.value));
    setIsOpen(false);
  }

  function handleKeyDown(event: React.KeyboardEvent<HTMLButtonElement>) {
    if (event.key === "Escape") {
      setIsOpen(false);
      return;
    }
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      if (!isOpen) {
        setActiveIndex(selectedIndex);
        setIsOpen(true);
      } else {
        const offset = event.key === "ArrowDown" ? 1 : -1;
        setActiveIndex(
          (index) => (index + offset + options.length) % options.length,
        );
      }
      return;
    }
    if (event.key === "Home" || event.key === "End") {
      event.preventDefault();
      setActiveIndex(event.key === "Home" ? 0 : options.length - 1);
      setIsOpen(true);
      return;
    }
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      if (!isOpen) {
        setActiveIndex(selectedIndex);
        setIsOpen(true);
      } else if (options[activeIndex]) {
        choose(options[activeIndex]);
      }
    }
  }

  return (
    <div
      ref={rootRef}
      className={`relative ${className}`}
      onBlur={(event) => {
        if (!rootRef.current?.contains(event.relatedTarget as Node)) {
          setIsOpen(false);
        }
      }}
    >
      <button
        id={id}
        type="button"
        role="combobox"
        aria-label={ariaLabel}
        aria-haspopup="listbox"
        aria-controls={listId}
        aria-expanded={isOpen}
        aria-activedescendant={
          isOpen ? `${listId}-option-${activeIndex}` : undefined
        }
        onClick={() => {
          setActiveIndex(selectedIndex);
          setIsOpen((open) => !open);
        }}
        onKeyDown={handleKeyDown}
        className="flex min-h-11 w-full items-center justify-between gap-3 rounded-xl border border-slate-700 bg-slate-800 px-3.5 py-2.5 text-left text-sm text-slate-100 shadow-sm outline-none transition duration-150 hover:border-slate-500 hover:bg-slate-800/90 focus-visible:border-indigo-400 focus-visible:ring-2 focus-visible:ring-indigo-400/30"
      >
        <span className="truncate">{selected?.label ?? value}</span>
        <svg
          aria-hidden="true"
          viewBox="0 0 20 20"
          fill="none"
          className={`size-4 shrink-0 text-slate-400 transition-transform duration-200 ${isOpen ? "rotate-180" : "rotate-0"}`}
        >
          <path
            d="m5 7.5 5 5 5-5"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>
      <div
        id={listId}
        role="listbox"
        aria-label={ariaLabel}
        aria-hidden={!isOpen}
        inert={!isOpen}
        data-open={isOpen}
        className={`select-menu absolute left-0 right-0 z-50 max-h-64 overflow-y-auto rounded-xl border border-slate-700 bg-slate-900 p-1.5 shadow-xl shadow-black/40 ${placement === "top" ? "bottom-full mb-2" : "top-full mt-2"}`}
      >
        {options.map((option, index) => {
          const isSelected = option.value === value;
          const isActive = index === activeIndex;
          return (
            <div
              id={`${listId}-option-${index}`}
              key={option.value}
              role="option"
              aria-selected={isSelected}
              onMouseEnter={() => setActiveIndex(index)}
              onMouseDown={(event) => event.preventDefault()}
              onClick={() => choose(option)}
              className={`flex cursor-pointer items-center justify-between rounded-lg px-3 py-2.5 text-sm transition-colors ${isActive ? "bg-slate-800" : "hover:bg-slate-800/70"} ${isSelected ? "font-semibold text-indigo-200" : "text-slate-300 hover:text-white"}`}
            >
              <span>{option.label}</span>
              {isSelected && (
                <svg
                  aria-hidden="true"
                  viewBox="0 0 20 20"
                  fill="none"
                  className="size-4 text-indigo-300"
                >
                  <path
                    d="m4.5 10 3.5 3.5 7.5-7.5"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
