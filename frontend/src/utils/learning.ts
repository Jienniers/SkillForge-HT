import { emptyProgress, type Progress } from "../types/learning";

export const dayName = (day: string) =>
  day.replace("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
export function levelForXp(xp: number) {
  if (xp >= 1000) return "👑 SkillForge Master";
  if (xp >= 600) return "🚀 Advanced";
  if (xp >= 300) return "🔥 Intermediate";
  if (xp >= 100) return "⚡ Apprentice";
  return "🌱 Beginner";
}
export function readProgress(): Progress {
  try {
    return {
      ...emptyProgress,
      ...JSON.parse(localStorage.getItem("skillforge-progress") || "{}"),
    };
  } catch {
    return emptyProgress;
  }
}
export function saveProgress(progress: Progress) {
  localStorage.setItem("skillforge-progress", JSON.stringify(progress));
}
export function playCompletionSound(achievement: string | null) {
  if (!achievement) return;
  const sound =
    achievement === "first_completion" || achievement === "final_completion"
      ? "AchievementSound.mp3"
      : "DayCompleteSound.mp3";
  void new Audio(`/sounds/${sound}`).play().catch(() => undefined);
}
