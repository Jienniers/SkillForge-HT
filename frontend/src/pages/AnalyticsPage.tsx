import { Button } from '../components/ui/Button'
import type { Progress } from '../types/learning'

function Stat({ label, value }: { label: string; value: string }) { return <div className="rounded-xl bg-slate-50 p-5"><p className="text-sm text-slate-500">{label}</p><p className="mt-2 text-xl font-bold">{value}</p></div> }
export function AnalyticsPage({ progress, level, onContinue }: { progress: Progress; level: string; onContinue: () => void }) {
  const percent = Math.round(progress.completed.length / 30 * 100)
  return <section className="rounded-2xl border border-slate-200 bg-white p-7 shadow-sm"><h2 className="text-2xl font-bold">Your progress</h2><p className="mt-1 text-slate-500">A snapshot of your learning journey.</p><div className="mt-7 grid gap-4 sm:grid-cols-3"><Stat label="Experience earned" value={`${progress.xp} XP`} /><Stat label="Current level" value={level} /><Stat label="Days completed" value={`${progress.completed.length} / 30`} /></div><div className="mt-8"><div className="mb-2 flex justify-between text-sm"><b>Roadmap progress</b><span>{percent}%</span></div><div className="h-3 rounded-full bg-slate-100"><div className="h-3 rounded-full bg-indigo-500" style={{ width: `${percent}%` }} /></div></div><Button variant="primary" onClick={onContinue} className="mt-7">Continue learning</Button></section>
}
