import { Select } from "../components/ui/Select";
import type { Theme } from "../types/theme";

export function SettingsPage({
  theme,
  onThemeChange,
}: {
  theme: Theme;
  onThemeChange: (theme: Theme) => void;
}) {
  return (
    <section className="theme-card rounded-2xl border border-slate-700 bg-slate-900 p-6 shadow-sm md:p-7">
      <p className="text-sm font-semibold text-indigo-300">PREFERENCES</p>
      <h2 className="mt-1 text-2xl font-bold">Settings</h2>
      <div className="mt-7 flex flex-col gap-3 sm:max-w-sm">
        <div>
          <h3 className="font-semibold">Theme</h3>
          <p className="mt-1 text-sm text-slate-400">
            Choose the appearance you want to use in SkillForge.
          </p>
        </div>
        <Select
          ariaLabel="Theme"
          value={theme}
          onChange={(value) => onThemeChange(value as Theme)}
          options={[
            { value: "light", label: "Light" },
            { value: "dark", label: "Dark" },
          ]}
          className="w-full"
        />
      </div>
    </section>
  );
}
