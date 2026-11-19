import { useEffect, useMemo, useState } from 'react'
import { BrowserRouter, NavLink, Route, Routes, useNavigate } from 'react-router'

type Roadmap = Record<string, string[]>
type Practice = Record<string, Record<string, string[]>>
type Progress = { xp: number; completed: string[]; answers: Record<string, string>; results: Record<string, string>; hints: Record<string, string>; charged: string[]; correct: string[] }
const languages = ['Python', 'JavaScript', 'Java', 'C++', 'Go']
const emptyProgress: Progress = { xp: 0, completed: [], answers: {}, results: {}, hints: {}, charged: [], correct: [] }
const dayName = (day: string) => day.replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase())
const endpoint = (path: string) => `${import.meta.env.VITE_API_URL ?? ''}/api/${path}`
const request = async <T,>(path: string, body: unknown): Promise<T> => {
  const response = await fetch(endpoint(path), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
  if (!response.ok) throw new Error((await response.text()) || `Request failed (${response.status})`)
  return response.json() as Promise<T>
}

function AppShell() {
  const [language, setLanguage] = useState('Python')
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null)
  const [practice, setPractice] = useState<Practice | null>(null)
  const [selectedDay, setSelectedDay] = useState('day_1')
  const [busy, setBusy] = useState('')
  const [notice, setNotice] = useState('')
  const [progress, setProgress] = useState<Progress>(() => { try { return { ...emptyProgress, ...JSON.parse(localStorage.getItem('skillforge-progress') || '{}') } } catch { return emptyProgress } })
  const navigate = useNavigate()
  useEffect(() => { localStorage.setItem('skillforge-progress', JSON.stringify(progress)) }, [progress])
  const completed = progress.completed.length
  const level = progress.xp >= 1000 ? '👑 SkillForge Master' : progress.xp >= 600 ? '🚀 Advanced' : progress.xp >= 300 ? '🔥 Intermediate' : progress.xp >= 100 ? '⚡ Apprentice' : '🌱 Beginner'
  const update = (fn: (p: Progress) => Progress) => setProgress(p => fn(p))

  async function generatePlan() {
    setBusy('Generating your roadmap…'); setNotice('')
    try {
      const generated = await request<Roadmap>('roadmap', { language: language.toLowerCase() })
      setRoadmap(generated)
    } catch {
      setNotice('AI roadmap generation needs a backend API. You can still use the built-in topic roadmap and practice workflow.')
      const roadmapData = await import('./data/roadmaps.json')
      const topics = roadmapData.default.roadmaps[language.toLowerCase() as keyof typeof roadmapData.default.roadmaps].steps
      setRoadmap(Object.fromEntries(Array.from({ length: 30 }, (_, i) => [`day_${i + 1}`, i < topics.length ? [topics[i]] : ['Review and build a small project using previous topics']])))
    } finally { setBusy('') }
  }
  async function generatePractice() {
    if (!roadmap) return
    setBusy('Generating practice questions…'); setNotice('')
    try {
      const generated = await request<Practice>('practice', { language: language.toLowerCase(), roadmap })
      setPractice(generated)
    } catch {
      setNotice('AI practice generation is unavailable without a connected backend. Starter questions are ready for each roadmap topic.')
      setPractice(Object.fromEntries(Object.entries(roadmap).map(([day, topics]) => [day, Object.fromEntries(topics.filter(t => t.toLowerCase() !== 'rest day').map(topic => [topic, [
        `Explain the core idea behind ${topic} in ${language}.`,
        `Write a small ${language} example that demonstrates ${topic}.`,
        `Describe one common mistake when using ${topic} and how you would avoid it.`,
      ]]))])))
    }
    setBusy('')
  }
  async function evaluate(key: string, question: string, code: string) {
    if (!code.trim()) { setNotice('Add your answer before checking it.'); return }
    setBusy('Checking your answer…')
    try {
      const result = await request<{ feedback: string; correct: boolean }>('evaluate', { language: language.toLowerCase(), question, code })
      update(p => ({ ...p, results: { ...p.results, [key]: result.feedback }, correct: result.correct && !p.correct.includes(key) ? [...p.correct, key] : p.correct, xp: result.correct && !p.correct.includes(key) ? p.xp + 10 : p.xp }))
    } catch {
      setNotice('AI evaluation needs a connected backend. Your answer is saved locally; add VITE_API_URL to connect the API.')
    }
    setBusy('')
  }
  async function getHint(key: string, question: string, level: 1 | 2) {
    const charged = progress.charged.includes(key)
    if (level === 2 && !charged && progress.xp < 5) { setNotice('You need at least 5 XP to use Hint 2.'); return }
    setBusy('Getting a hint…')
    try {
      const result = await request<{ hint: string }>('hint', { language: language.toLowerCase(), question, level })
      update(p => ({ ...p, hints: { ...p.hints, [`${key}-${level}`]: result.hint }, xp: level === 2 && !charged ? p.xp - 5 : p.xp, charged: level === 2 && !charged ? [...p.charged, key] : p.charged }))
    } catch { setNotice('Hint generation needs a connected backend API.') }
    setBusy('')
  }
  const dayData = practice?.[selectedDay] ?? {}
  const questions = useMemo(() => Object.entries(dayData).flatMap(([topic, qs]) => qs.map((question, i) => ({ topic, question, key: `${selectedDay}-${topic}-${i}` }))), [dayData, selectedDay])
  function checkDay() {
    if (questions.length && questions.every(q => progress.correct.includes(q.key))) {
      update(p => {
        if (p.completed.includes(selectedDay)) return p
        const next = [...p.completed, selectedDay]
        const bonus = next.length === 1 ? 10 : selectedDay === 'day_30' && next.length === 30 ? 50 : 0
        return { ...p, completed: next, xp: p.xp + bonus }
      })
    }
  }
  async function checkQuestion(key: string, question: string) { await evaluate(key, question, progress.answers[key] ?? ''); setTimeout(checkDay, 100) }
  function downloadPdf() {
    if (!roadmap) return
    const content = `SkillForge — ${language} 30 Day Learning Plan\n\n` + Object.entries(roadmap).map(([day, topics]) => `${dayName(day)}\n${topics.map(t => `• ${t}`).join('\n')}`).join('\n\n')
    const link = document.createElement('a'); link.href = URL.createObjectURL(new Blob([content], { type: 'text/plain' })); link.download = 'SkillForge_Roadmap.txt'; link.click(); URL.revokeObjectURL(link.href)
  }

  return <div className="min-h-screen bg-[#f6f8fc] text-slate-800 md:flex">
    <aside className="w-full bg-[#101a31] p-5 text-white md:min-h-screen md:w-72 md:shrink-0 md:p-6">
      <NavLink to="/" className="mb-7 flex items-center gap-3 text-xl font-bold"><span className="grid size-10 place-items-center rounded-xl bg-indigo-500">⚒</span> SkillForge</NavLink>
      <div className="mb-5 rounded-2xl bg-white/5 p-4"><label className="mb-2 block text-xs font-semibold uppercase tracking-wider text-slate-400">Your learning path</label><select value={language} onChange={e => setLanguage(e.target.value)} className="w-full rounded-lg border border-white/10 bg-[#1b2944] p-3 text-sm"><option>Python</option>{languages.slice(1).map(l => <option key={l}>{l}</option>)}</select><button onClick={generatePlan} className="mt-3 w-full rounded-lg bg-indigo-500 px-4 py-3 text-sm font-semibold hover:bg-indigo-400">Generate plan</button></div>
      <nav className="mb-6 flex gap-2 md:block md:space-y-2">{[['/', '⌂', 'Roadmap'], ['/analytics', '▥', 'Progress']].map(([to, icon, label]) => <NavLink key={to} to={to} className={({ isActive }) => `flex flex-1 items-center gap-3 rounded-xl px-4 py-3 text-sm ${isActive ? 'bg-indigo-500 text-white' : 'text-slate-300 hover:bg-white/5'}`}><span>{icon}</span>{label}</NavLink>)}</nav>
      <section className="hidden rounded-2xl border border-white/10 bg-white/5 p-4 md:block"><h2 className="mb-4 text-sm font-semibold">📊 Your stats</h2><div className="flex justify-between text-sm"><span className="text-slate-400">Experience</span><b>{progress.xp} XP</b></div><p className="mt-2 text-sm text-indigo-200">{level}</p><div className="mt-5 flex justify-between text-sm"><span className="text-slate-400">Days completed</span><b>{completed}/30</b></div><div className="mt-2 h-2 rounded-full bg-slate-700"><div className="h-full rounded-full bg-indigo-400" style={{ width: `${completed / 30 * 100}%` }} /></div><button className="mt-5 w-full rounded-lg border border-white/10 py-2 text-sm text-slate-300 hover:bg-white/5" onClick={() => { setSelectedDay('day_1'); setNotice('Progress is saved in this browser.'); }}>Refresh</button></section>
      <p className="mt-6 hidden text-xs leading-5 text-slate-500 md:block">Your answers and progress are saved locally in this browser.</p>
    </aside>
    <main className="min-w-0 flex-1 p-5 md:p-10"><header className="mb-8 flex flex-wrap items-center justify-between gap-4"><div><p className="text-sm font-medium text-indigo-600">YOUR PERSONAL LEARNING SPACE</p><h1 className="mt-1 text-3xl font-bold tracking-tight">Build your next skill.</h1></div><span className="rounded-full bg-white px-4 py-2 text-sm shadow-sm">🔥 {progress.xp} XP</span></header>
      {notice && <div role="status" className="mb-5 flex items-start justify-between gap-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900"><span>{notice}</span><button onClick={() => setNotice('')} aria-label="Dismiss">×</button></div>}
      {busy && <div className="mb-5 rounded-xl bg-indigo-50 p-3 text-sm text-indigo-700">{busy}</div>}
      <Routes><Route path="/analytics" element={<section className="rounded-2xl border border-slate-200 bg-white p-7 shadow-sm"><h2 className="text-2xl font-bold">Your progress</h2><p className="mt-1 text-slate-500">A snapshot of your learning journey.</p><div className="mt-7 grid gap-4 sm:grid-cols-3"><Stat label="Experience earned" value={`${progress.xp} XP`} /><Stat label="Current level" value={level} /><Stat label="Days completed" value={`${completed} / 30`} /></div><div className="mt-8"><div className="mb-2 flex justify-between text-sm"><b>Roadmap progress</b><span>{Math.round(completed / 30 * 100)}%</span></div><div className="h-3 rounded-full bg-slate-100"><div className="h-3 rounded-full bg-indigo-500" style={{ width: `${completed / 30 * 100}%` }} /></div></div><button onClick={() => navigate('/')} className="mt-7 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white">Continue learning</button></section>} /><Route path="/" element={<>
        {!roadmap ? <section className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm md:p-12"><div className="mb-6 grid size-14 place-items-center rounded-2xl bg-indigo-50 text-3xl">🚀</div><p className="text-sm font-semibold text-indigo-600">A PLAN BUILT AROUND YOU</p><h2 className="mt-2 max-w-2xl text-3xl font-bold">Turn your goal into a 30-day coding habit.</h2><p className="mt-3 max-w-xl leading-7 text-slate-500">Choose a language and create a structured learning roadmap, then practice with questions, hints, and progress tracking.</p><button onClick={generatePlan} className="mt-6 rounded-xl bg-indigo-600 px-5 py-3 font-semibold text-white hover:bg-indigo-500">Generate my {language} plan →</button></section> : <>
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm md:p-7"><div className="flex flex-wrap items-start justify-between gap-4"><div><p className="text-sm font-semibold text-indigo-600">YOUR 30-DAY ROADMAP</p><h2 className="mt-1 text-2xl font-bold">{language} learning plan</h2><p className="mt-1 text-sm text-slate-500">A day-by-day path from foundations to advanced skills.</p></div><button onClick={downloadPdf} className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-semibold hover:bg-slate-50">📄 Download roadmap</button></div><div className="mt-6 grid gap-3 sm:grid-cols-2 xl:grid-cols-3">{Object.entries(roadmap).map(([day, topics]) => <details key={day} className="group rounded-xl border border-slate-200"><summary className="flex cursor-pointer list-none items-center justify-between p-4 font-semibold">{dayName(day)}<span className="text-slate-400 group-open:rotate-180">⌄</span></summary><div className="space-y-2 border-t border-slate-100 px-4 py-3 text-sm">{topics.map(t => <p key={t} className={t.toLowerCase() === 'rest day' ? 'text-emerald-700' : 'text-slate-600'}>{t.toLowerCase() === 'rest day' ? '😴 Rest Day' : `✓ ${t}`}</p>)}</div></details>)}</div><div className="mt-6 flex flex-wrap gap-3"><button onClick={generatePractice} className="rounded-lg bg-indigo-600 px-4 py-3 text-sm font-semibold text-white hover:bg-indigo-500">🧠 Generate practice questions</button><button onClick={() => setRoadmap(null)} className="rounded-lg border border-slate-200 px-4 py-3 text-sm font-semibold">Choose another language</button></div></section>
          {practice && <section className="mt-7 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm md:p-7"><div className="flex flex-wrap items-center justify-between gap-4"><div><p className="text-sm font-semibold text-indigo-600">LEARN BY DOING</p><h2 className="mt-1 text-2xl font-bold">🧠 Practice zone</h2></div><select value={selectedDay} onChange={e => setSelectedDay(e.target.value)} className="rounded-lg border border-slate-200 bg-white px-3 py-2">{Object.keys(practice).map(day => <option key={day} value={day}>{dayName(day)}{progress.completed.includes(day) ? ' (✅ Passed)' : ''}</option>)}</select></div>{!Object.keys(dayData).length ? <p className="mt-6 rounded-lg bg-slate-50 p-4 text-slate-600">No coding practice for this day (setup/theory day).</p> : <><h3 className="mt-6 text-lg font-semibold">📘 {dayName(selectedDay)}</h3>{Object.entries(dayData).map(([topic, qs]) => <details key={topic} open className="mt-4 rounded-xl border border-slate-200"><summary className="cursor-pointer bg-slate-50 p-4 font-semibold">📌 {topic}</summary><div className="space-y-6 p-4">{qs.map((question, i) => { const key = `${selectedDay}-${topic}-${i}`; return <article key={key} className="border-b border-slate-100 pb-6 last:border-0"><h4 className="font-semibold">❓ Question {i + 1}</h4><p className="mt-2 text-sm leading-6 text-slate-600">{question}</p><textarea aria-label={`Answer ${i + 1}`} value={progress.answers[key] ?? ''} onChange={e => update(p => ({ ...p, answers: { ...p.answers, [key]: e.target.value } }))} placeholder={`Write your ${language} answer here…`} className="mt-3 min-h-40 w-full rounded-xl border border-slate-200 bg-[#111827] p-4 font-mono text-sm text-emerald-100 placeholder:text-slate-500 focus:border-indigo-400 focus:outline-none"/><div className="mt-3 flex flex-wrap gap-2"><button onClick={() => checkQuestion(key, question)} className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white">🧪 Check</button><button onClick={() => getHint(key, question, 1)} className="rounded-lg border border-slate-200 px-3 py-2 text-sm">💡 Hint 1</button><button onClick={() => getHint(key, question, 2)} className="rounded-lg border border-slate-200 px-3 py-2 text-sm">🧠 Hint 2 (-5 XP)</button></div>{[1,2].map(n => progress.hints[`${key}-${n}`] && <p key={n} className="mt-3 rounded-lg bg-indigo-50 p-3 text-sm text-indigo-900">Hint {n}: {progress.hints[`${key}-${n}`]}</p>)}{progress.results[key] && <div className="mt-3 rounded-lg bg-emerald-50 p-4 text-sm text-emerald-900"><b>✅ Feedback</b><p className="mt-1 whitespace-pre-wrap">{progress.results[key]}</p></div>}</article> })}</div></details>)}{questions.length > 0 && questions.every(q => progress.correct.includes(q.key)) && <p className="mt-5 rounded-lg bg-emerald-50 p-4 font-semibold text-emerald-800">🏁 Day Completed! {progress.completed.includes(selectedDay) ? '' : 'Completion bonus added.'}</p>}</>}</section>}
        </>}</>} /></Routes>
      <footer className="mt-8 text-center text-xs text-slate-400">SkillForge · Keep showing up, one day at a time.</footer>
    </main>
  </div>
}
function Stat({ label, value }: { label: string; value: string }) { return <div className="rounded-xl bg-slate-50 p-5"><p className="text-sm text-slate-500">{label}</p><p className="mt-2 text-xl font-bold">{value}</p></div> }
export default function App() { return <BrowserRouter><AppShell /></BrowserRouter> }

