export function InlineMarkdown({ text }: { text: string }) {
  return text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g).map((part, index) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return <strong key={index}>{part.slice(2, -2)}</strong>;
    }
    if (part.startsWith("`") && part.endsWith("`")) {
      return (
        <code
          key={index}
          className="rounded bg-slate-950/60 px-1.5 py-0.5 font-mono text-emerald-100"
        >
          {part.slice(1, -1)}
        </code>
      );
    }
    return part;
  });
}
