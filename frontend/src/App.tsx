import { useState } from 'react'
import { BrowserRouter, Route, Routes, useNavigate } from 'react-router'
import { Sidebar } from './components/Sidebar'
import { Notice } from './components/ui/Notice'
import { AnalyticsPage } from './pages/AnalyticsPage'
import { RoadmapPage } from './pages/RoadmapPage'
import { useLearning } from './hooks/useLearning'
import { type Language, languages } from './types/learning'

function Application() {
  const [language, setLanguage] = useState<Language>(languages[0])
  const learning = useLearning(language)
  const navigate = useNavigate()
  return <div className="min-h-screen bg-[#f6f8fc] text-slate-800 md:flex">
    <Sidebar language={language} onLanguageChange={setLanguage} onGeneratePlan={learning.generatePlan} progress={learning.progress} level={learning.level} onRefresh={learning.resetSelection} />
    <main className="min-w-0 flex-1 p-5 md:p-10">
      <header className="mb-8 flex flex-wrap items-center justify-between gap-4"><div><p className="text-sm font-medium text-indigo-600">YOUR PERSONAL LEARNING SPACE</p><h1 className="mt-1 text-3xl font-bold tracking-tight">Build your next skill.</h1></div><span className="rounded-full bg-white px-4 py-2 text-sm shadow-sm">🔥 {learning.progress.xp} XP · {learning.level}</span></header>
      {learning.notice && <Notice onDismiss={() => learning.setNotice('')}>{learning.notice}</Notice>}
      {learning.busy && <div role="status" className="mb-5 rounded-xl bg-indigo-50 p-3 text-sm text-indigo-700">{learning.busy}</div>}
      <Routes>
        <Route path="/" element={<RoadmapPage language={language} roadmap={learning.roadmap} practice={learning.practice} selectedDay={learning.selectedDay} onSelectDay={learning.setSelectedDay} progress={learning.progress} onGeneratePlan={learning.generatePlan} onGeneratePractice={learning.generatePractice} onDownloadPdf={learning.downloadPdf} onAnswer={learning.updateAnswer} onCheck={learning.checkAnswer} onHint={learning.getHint} />} />
        <Route path="/analytics" element={<AnalyticsPage progress={learning.progress} level={learning.level} onContinue={() => navigate('/')} />} />
      </Routes>
      <footer className="mt-8 text-center text-xs text-slate-400">SkillForge · Keep showing up, one day at a time.</footer>
    </main>
  </div>
}
export default function App() { return <BrowserRouter><Application /></BrowserRouter> }
