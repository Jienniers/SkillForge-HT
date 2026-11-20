import { useState } from "react";
import {
  BrowserRouter,
  Route,
  Routes,
  useLocation,
  useNavigate,
} from "react-router";
import { Sidebar } from "./components/Sidebar";
import { Notice } from "./components/ui/Notice";
import { BusyToast } from "./components/ui/BusyToast";
import { AnalyticsPage } from "./pages/AnalyticsPage";
import { RoadmapPage } from "./pages/RoadmapPage";
import { useLearning } from "./hooks/useLearning";
import { useTheme } from "./hooks/useTheme";
import { useAIProvider } from "./hooks/useAIProvider";
import { type Language, languages } from "./types/learning";
import { SettingsPage } from "./pages/SettingsPage";

function Application() {
  const [language, setLanguage] = useState<Language>(languages[0]);
  const { provider, setProvider } = useAIProvider();
  const learning = useLearning(language, provider);
  const { theme, setTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div
      data-theme={theme}
      className="app-shell min-h-screen bg-slate-950 text-slate-100 md:flex"
    >
      <Sidebar
        language={language}
        onLanguageChange={setLanguage}
        onGeneratePlan={learning.generatePlan}
        isGenerating={learning.isGenerating}
        progress={learning.progress}
        level={learning.level}
      />

      <main className="app-main min-w-0 flex-1 p-5 md:p-10">
        <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm font-medium text-indigo-400">
              YOUR PERSONAL LEARNING SPACE
            </p>
            <h1 className="mt-1 text-3xl font-bold tracking-tight text-white">
              Build your next skill.
            </h1>
          </div>

          <span className="rounded-full border border-slate-700 bg-slate-900 px-4 py-2 text-sm text-slate-200 shadow-sm">
            🔥 {learning.progress.xp} XP · {learning.level}
          </span>
        </header>

        {learning.notice && (
          <Notice onDismiss={() => learning.setNotice("")}>
            {learning.notice}
          </Notice>
        )}

        <BusyToast message={learning.busy} />

        <div key={location.pathname} className="page-transition">
          <Routes>
            <Route
              path="/"
              element={
                <RoadmapPage
                  language={language}
                  roadmap={learning.roadmap}
                  practice={learning.practice}
                  selectedDay={learning.selectedDay}
                  onSelectDay={learning.setSelectedDay}
                  progress={learning.progress}
                  onGeneratePlan={learning.generatePlan}
                  onGeneratePractice={learning.generatePractice}
                  isGenerating={learning.isGenerating}
                  onDownloadPdf={learning.downloadPdf}
                  onAnswer={learning.updateAnswer}
                  onCheck={learning.checkAnswer}
                  onHint={learning.getHint}
                />
              }
            />

            <Route
              path="/analytics"
              element={
                <AnalyticsPage
                  progress={learning.progress}
                  level={learning.level}
                  onContinue={() => navigate("/")}
                />
              }
            />

            <Route
              path="/settings"
              element={
                <SettingsPage
                  theme={theme}
                  onThemeChange={setTheme}
                  provider={provider}
                  onProviderChange={setProvider}
                />
              }
            />
          </Routes>
        </div>

        <footer className="mt-8 text-center text-xs text-slate-500">
          SkillForge · Keep showing up, one day at a time.
        </footer>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Application />
    </BrowserRouter>
  );
}
