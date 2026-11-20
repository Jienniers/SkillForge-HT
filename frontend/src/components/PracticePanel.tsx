import { Button } from "./ui/Button";
import { Select } from "./ui/Select";
import { DropdownCard } from "./ui/DropdownCard";
import type { Language, PracticePlan, Progress } from "../types/learning";
import { dayName } from "../utils/learning";
import { FeedbackContent } from "./ui/FeedbackContent";

export function PracticePanel({
  practice,
  language,
  selectedDay,
  onSelectDay,
  progress,
  onAnswer,
  onCheck,
  onHint,
}: {
  practice: PracticePlan;
  language: Language;
  selectedDay: string;
  onSelectDay: (day: string) => void;
  progress: Progress;
  onAnswer: (key: string, answer: string) => void;
  onCheck: (key: string, question: string) => void;
  onHint: (key: string, question: string, level: 1 | 2) => void;
}) {
  const topics = practice[selectedDay] ?? {};
  const questions = Object.entries(topics).flatMap(([topic, list]) =>
    list.map((question, i) => ({
      topic,
      question,
      index: i,
      key: `${selectedDay}-${topic}-${i}`,
    })),
  );
  const passed =
    questions.length > 0 &&
    questions.every((item) => progress.correct.includes(item.key));
  return (
    <section className="mt-7 rounded-2xl border border-slate-700 bg-slate-900 p-6 shadow-sm md:p-7">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-sm font-semibold text-indigo-300">
            LEARN BY DOING
          </p>
          <h2 className="mt-1 text-2xl font-bold">🧠 Practice zone</h2>
        </div>
        <Select
          ariaLabel="Select a practice day"
          value={selectedDay}
          onChange={onSelectDay}
          options={Object.keys(practice).map((day) => ({
            value: day,
            label: `${dayName(day)}${progress.completed.includes(day) ? " (✅ Passed)" : ""}`,
          }))}
          placement="top"
          className="w-full sm:w-56"
        />
      </div>
      {questions.length === 0 ? (
        <p className="mt-6 rounded-lg bg-slate-800 p-4 text-slate-300">
          No coding practice for this day (setup/theory day).
        </p>
      ) : (
        <>
          <h3 className="mt-6 text-lg font-semibold">
            📘 {dayName(selectedDay)}
          </h3>
          {Object.entries(topics).map(([topic, list]) => (
            <DropdownCard key={topic} title={`📌 ${topic}`} className="mt-4">
              <div className="space-y-6">
                {list.map((question, index) => {
                  const key = `${selectedDay}-${topic}-${index}`;
                  const isCorrect = progress.correct.includes(key);
                  const feedback = (progress.results[key] ?? "")
                    .replace(/^\s*(?:\*\*)?✅\s*Correct(?:\*\*)?\s*/u, "")
                    .trim();
                  return (
                    <article
                      key={key}
                      className="border-b border-slate-700 pb-6 last:border-0"
                    >
                      <h4 className="font-semibold">❓ Question {index + 1}</h4>
                      <p className="mt-2 text-sm leading-6 text-slate-300">
                        {question}
                      </p>
                      <textarea
                        aria-label={`Answer ${index + 1}`}
                        value={progress.answers[key] ?? ""}
                        onChange={(event) => onAnswer(key, event.target.value)}
                        placeholder={`Write your ${language} answer here…`}
                        className="mt-3 min-h-40 w-full rounded-xl border border-slate-700 bg-[#111827] p-4 font-mono text-sm text-emerald-100 placeholder:text-slate-400 focus:border-indigo-400 focus:outline-none"
                      />
                      <div className="mt-3 flex flex-wrap gap-2">
                        <Button
                          variant="primary"
                          onClick={() => onCheck(key, question)}
                        >
                          🧪 Check
                        </Button>
                        <Button onClick={() => onHint(key, question, 1)}>
                          💡 Hint 1
                        </Button>
                        <Button onClick={() => onHint(key, question, 2)}>
                          🧠 Hint 2 (-5 XP)
                        </Button>
                      </div>
                      {[1, 2].map(
                        (level) =>
                          progress.hints[`${key}-${level}`] && (
                            <p
                              key={level}
                              className="mt-3 rounded-lg bg-indigo-500/10 p-3 text-sm text-indigo-200"
                            >
                              Hint {level}: {progress.hints[`${key}-${level}`]}
                            </p>
                          ),
                      )}
                      {progress.results[key] && (
                        <div
                          className={`mt-3 rounded-lg p-4 text-sm ${isCorrect ? "bg-emerald-500/10 text-emerald-200" : "bg-amber-500/10 text-amber-200"}`}
                        >
                          <b>
                            {isCorrect ? "✅ Correct" : "📝 Feedback"}
                          </b>
                          {feedback && <FeedbackContent content={feedback} />}
                        </div>
                      )}
                    </article>
                  );
                })}
              </div>
            </DropdownCard>
          ))}
          {passed && (
            <p className="mt-5 rounded-lg bg-emerald-500/10 p-4 font-semibold text-emerald-200">
              🏁 Day Completed!
            </p>
          )}
        </>
      )}
    </section>
  );
}
