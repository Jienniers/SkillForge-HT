import type { Evaluation, PracticePlan, Roadmap } from "../types/learning";
import type { AIProvider } from "../types/provider";

const apiBase = import.meta.env.VITE_API_URL ?? "";
async function post<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${apiBase}/api/${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    const payload = (await response.json().catch(() => null)) as {
      detail?: string;
    } | null;
    throw new Error(payload?.detail || `Request failed (${response.status})`);
  }
  return response.json() as Promise<T>;
}
export const learningApi = {
  roadmap: (language: string, provider: AIProvider) =>
    post<Roadmap>("roadmap", { language: language.toLowerCase(), provider }),
  practice: (language: string, roadmap: Roadmap, provider: AIProvider) =>
    post<PracticePlan>("practice", {
      language: language.toLowerCase(),
      roadmap,
      provider,
    }),
  evaluate: (
    language: string,
    question: string,
    code: string,
    provider: AIProvider,
  ) =>
    post<Evaluation>("evaluate", {
      language: language.toLowerCase(),
      question,
      code,
      provider,
    }),
  hint: (
    language: string,
    question: string,
    level: 1 | 2,
    xp: number,
    alreadyCharged: boolean,
    provider: AIProvider,
  ) =>
    post<{ hint: string; xp_cost: number }>("hint", {
      language: language.toLowerCase(),
      question,
      level,
      xp,
      already_charged: alreadyCharged,
      provider,
    }),
  completion: (
    dayNumber: number,
    completedDayCount: number,
    firstBonusGiven: boolean,
  ) =>
    post<{ xp: number; achievement: string | null }>(
      "gamification/completion",
      {
        day_number: dayNumber,
        completed_day_count: completedDayCount,
        first_bonus_given: firstBonusGiven,
      },
    ),
  level: (xp: number) => post<{ level: string }>("gamification/level", { xp }),
  async downloadPdf(roadmap: Roadmap) {
    const response = await fetch(`${apiBase}/api/roadmap/pdf`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ roadmap }),
    });
    if (!response.ok) throw new Error("Could not create the roadmap PDF.");
    return response.blob();
  },
};
