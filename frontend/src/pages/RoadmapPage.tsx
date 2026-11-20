import { Button } from "../components/ui/Button";
import { DropdownCard } from "../components/ui/DropdownCard";
import { PracticePanel } from "../components/PracticePanel";
import type {
  Language,
  PracticePlan,
  Progress,
  Roadmap,
} from "../types/learning";
import { dayName } from "../utils/learning";

export function RoadmapPage({
  language,
  roadmap,
  practice,
  selectedDay,
  onSelectDay,
  progress,
  onGeneratePlan,
  onGeneratePractice,
  isGenerating,
  onDownloadPdf,
  onAnswer,
  onCheck,
  onHint,
}: {
  language: Language;
  roadmap: Roadmap | null;
  practice: PracticePlan | null;
  selectedDay: string;
  onSelectDay: (day: string) => void;
  progress: Progress;
  onGeneratePlan: () => void;
  onGeneratePractice: () => void;
  isGenerating: boolean;
  onDownloadPdf: () => void;
  onAnswer: (key: string, value: string) => void;
  onCheck: (key: string, question: string) => void;
  onHint: (key: string, question: string, level: 1 | 2) => void;
}) {
  if (!roadmap)
    return (
      <section className="rounded-2xl border border-slate-700 bg-slate-900 p-8 shadow-sm md:p-12">
        <div className="mb-6 grid size-14 place-items-center rounded-2xl bg-indigo-500/10 text-3xl">
          🚀
        </div>
        <p className="text-sm font-semibold text-indigo-300">
          A PLAN BUILT AROUND YOU
        </p>
        <h2 className="mt-2 max-w-2xl text-3xl font-bold">
          Turn your goal into a 30-day coding habit.
        </h2>
        <p className="mt-3 max-w-xl leading-7 text-slate-400">
          Choose a language and create a structured learning roadmap, then
          practice with questions, hints, and progress tracking.
        </p>
        <Button
          variant="primary"
          onClick={onGeneratePlan}
          disabled={isGenerating}
          className="mt-6 rounded-xl px-5 py-3"
        >
          {isGenerating ? "Please wait…" : `Generate my ${language} plan →`}
        </Button>
      </section>
    );
  return (
    <>
      <section className="rounded-2xl border border-slate-700 bg-slate-900 p-6 shadow-sm md:p-7">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="text-sm font-semibold text-indigo-300">
              YOUR 30-DAY ROADMAP
            </p>
            <h2 className="mt-1 text-2xl font-bold">
              {language} learning plan
            </h2>
            <p className="mt-1 text-sm text-slate-400">
              A day-by-day path from foundations to advanced skills.
            </p>
          </div>
          <Button onClick={onDownloadPdf}>📄 Download roadmap PDF</Button>
        </div>
        <div className="mt-6 grid items-start gap-3 sm:grid-cols-2 xl:grid-cols-3">
          {Object.entries(roadmap).map(([day, topics]) => (
            <DropdownCard key={day} title={dayName(day)}>
              <div className="space-y-2">
                {topics.map((topic) => (
                  <p
                    key={topic}
                    className={
                      topic.toLowerCase() === "rest day"
                        ? "text-emerald-300"
                        : "text-slate-300"
                    }
                  >
                    {topic.toLowerCase() === "rest day"
                      ? "😴 Rest Day"
                      : `✓ ${topic}`}
                  </p>
                ))}
              </div>
            </DropdownCard>
          ))}
        </div>
        <div className="mt-6 flex flex-wrap gap-3">
          <Button
            variant="primary"
            onClick={onGeneratePractice}
            disabled={isGenerating}
            className="px-4 py-3"
          >
            {isGenerating ? "Generating…" : "🧠 Generate practice questions"}
          </Button>
          <Button onClick={onGeneratePlan} disabled={isGenerating} className="px-4 py-3">
            {isGenerating ? "Please wait…" : "Generate a new plan"}
          </Button>
        </div>
      </section>
      {practice && (
        <PracticePanel
          practice={practice}
          language={language}
          selectedDay={selectedDay}
          onSelectDay={onSelectDay}
          progress={progress}
          onAnswer={onAnswer}
          onCheck={onCheck}
          onHint={onHint}
        />
      )}
    </>
  );
}
