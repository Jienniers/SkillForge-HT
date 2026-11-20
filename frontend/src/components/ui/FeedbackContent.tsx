import { CodeBlock } from "./CodeBlock";

function renderInline(text: string) {
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

export function FeedbackContent({ content }: { content: string }) {
  const blocks = content
    .trim()
    .split(/```([^\n]*)\r?\n([\s\S]*?)```/g);

  return (
    <div className="mt-2 space-y-3 leading-6">
      {blocks.map((block, index) => {
        if (index % 3 === 1) {
          const code = blocks[index + 1] ?? "";
          return (
            <CodeBlock
              key={`code-${index}`}
              language={block.trim()}
              code={code.replace(/^\r?\n|\r?\n$/g, "")}
            />
          );
        }
        if (index % 3 === 2) return null;
        return block
          .split(/\n{2,}/)
          .filter((paragraph) => paragraph.trim())
          .map((paragraph, paragraphIndex) => (
            <p key={`text-${index}-${paragraphIndex}`} className="whitespace-pre-wrap">
              {renderInline(paragraph.trim())}
            </p>
          ));
      })}
    </div>
  );
}
