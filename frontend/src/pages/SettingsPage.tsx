import { Select } from "../components/ui/Select";
import { aiProviders, type AIProvider } from "../types/provider";
import type { Theme } from "../types/theme";

export function SettingsPage({
  theme,
  onThemeChange,
  provider,
  onProviderChange,
}: {
  theme: Theme;
  onThemeChange: (theme: Theme) => void;
  provider: AIProvider;
  onProviderChange: (provider: AIProvider) => void;
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
      <div className="mt-8 flex flex-col gap-3 border-t border-slate-700 pt-6 sm:max-w-sm">
        <div>
          <h3 className="font-semibold">AI provider</h3>
          <p className="mt-1 text-sm text-slate-400">
            {provider === "local"
              ? "Local generation uses LM Studio at localhost:1234 with qwen2.5-coder-7b-instruct."
              : "Gemini generation uses the API key configured on the Python backend."}
          </p>
        </div>
        <Select
          ariaLabel="AI provider"
          value={provider}
          onChange={(value) => onProviderChange(value as AIProvider)}
          options={aiProviders}
          className="w-full"
        />
      </div>
    </section>
  );
}
