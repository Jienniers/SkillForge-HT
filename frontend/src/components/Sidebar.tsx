import { NavLink } from "react-router";
import { Button } from "./ui/Button";
import { Select } from "./ui/Select";
import { languages, type Language, type Progress } from "../types/learning";

export function Sidebar({
  language,
  onLanguageChange,
  onGeneratePlan,
  isGenerating,
  progress,
  completedDays,
  totalPracticeDays,
  level,
}: {
  language: Language;
  onLanguageChange: (language: Language) => void;
  onGeneratePlan: () => void;
  isGenerating: boolean;
  progress: Progress;
  completedDays: number;
  totalPracticeDays: number | null;
  level: string;
}) {
  return (
    <aside className="app-sidebar w-full bg-[#101a31] p-5 text-white md:min-h-screen md:w-72 md:shrink-0 md:p-6">
      <NavLink
        to="/"
        className="mb-7 flex items-center gap-3 text-xl font-bold"
      >
        <span className="grid size-10 place-items-center rounded-xl bg-indigo-500">
          ⚒
        </span>{" "}
        SkillForge
      </NavLink>
      <div className="sidebar-panel mb-5 rounded-2xl bg-white/5 p-4">
        <label
          htmlFor="language"
          className="mb-2 block text-xs font-semibold uppercase tracking-wider text-slate-400"
        >
          Your learning path
        </label>
        <Select
          id="language"
          ariaLabel="Your learning path"
          value={language}
          onChange={(value) => onLanguageChange(value as Language)}
          options={languages.map((item) => ({ value: item, label: item }))}
          className="w-full"
        />
        <Button
          variant="primary"
          onClick={onGeneratePlan}
          disabled={isGenerating}
          className="mt-3 w-full bg-indigo-500 py-3"
        >
          {isGenerating ? "Please wait…" : "Generate plan"}
        </Button>
      </div>
      <nav className="mb-6 flex gap-2 md:block md:space-y-2">
        {[
          ["/", "⌂", "Roadmap"],
          ["/analytics", "▥", "Progress"],
          ["/settings", "⚙", "Settings"],
        ].map(([to, icon, title]) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex flex-1 items-center gap-3 rounded-xl px-4 py-3 text-sm ${isActive ? "bg-indigo-500 text-white" : "text-slate-300 hover:bg-white/5"}`
            }
          >
            <span>{icon}</span>
            {title}
          </NavLink>
        ))}
      </nav>
      <section className="sidebar-panel hidden rounded-2xl border border-white/10 bg-white/5 p-4 md:block">
        <h2 className="mb-4 text-sm font-semibold">📊 Your stats</h2>
        <div className="flex justify-between text-sm">
          <span className="text-slate-400">Experience</span>
          <b>{progress.xp} XP</b>
        </div>
        <p className="mt-2 text-sm text-indigo-200">{level}</p>
        <div className="mt-5 flex justify-between text-sm">
          <span className="text-slate-400">Days completed</span>
          <b>
            {completedDays}/{totalPracticeDays ?? "—"}
          </b>
        </div>
        <div className="mt-2 h-2 rounded-full bg-slate-700">
          <div
            className="h-full rounded-full bg-indigo-400"
            style={{
              width: `${totalPracticeDays ? (completedDays / totalPracticeDays) * 100 : 0}%`,
            }}
          />
        </div>
      </section>
      <p className="mt-6 hidden text-xs leading-5 text-slate-500 md:block">
        Your answers and progress are saved locally in this browser.
      </p>
    </aside>
  );
}
