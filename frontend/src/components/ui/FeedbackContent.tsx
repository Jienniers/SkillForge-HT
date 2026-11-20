import { CodeBlock } from "./CodeBlock";
import { InlineMarkdown } from "./InlineMarkdown";

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
              <InlineMarkdown text={paragraph.trim()} />
            </p>
          ));
      })}
    </div>
  );
}
