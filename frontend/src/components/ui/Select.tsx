import type { SelectHTMLAttributes } from "react";

export function Select(props: SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select
      {...props}
      className={`rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-100 ${props.className ?? ""}`}
    />
  );
}
