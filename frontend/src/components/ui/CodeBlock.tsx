export function CodeBlock({
  code,
  language,
}: {
  code: string;
  language: string;
}) {
  return (
    <div className="my-3 overflow-hidden rounded-xl border border-slate-700 bg-slate-950/80">
      {language && (
        <div className="border-b border-slate-700 px-4 py-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
          {language}
        </div>
      )}
      <pre className="overflow-x-auto p-4 text-sm leading-6 text-emerald-100">
        <code>{code}</code>
      </pre>
    </div>
  );
}
