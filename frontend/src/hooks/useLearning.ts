import { useEffect, useMemo, useState } from "react";
import { learningApi } from "../services/learningApi";
import type { AIProvider } from "../types/provider";
import {
  emptyProgress,
  type Language,
  type PracticePlan,
  type Progress,
  type Roadmap,
} from "../types/learning";
import {
  playCompletionSound,
  readProgress,
  saveProgress,
} from "../utils/learning";

export function useLearning(language: Language, provider: AIProvider) {
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [practice, setPractice] = useState<PracticePlan | null>(null);
  const [selectedDay, setSelectedDay] = useState("day_1");
  const [progress, setProgress] = useState<Progress>(readProgress);
  const [level, setLevel] = useState("");
  const [busy, setBusy] = useState("");
  const [notice, setNotice] = useState("");
  useEffect(() => saveProgress(progress), [progress]);
  useEffect(() => {
    let current = true;
    learningApi
      .level(progress.xp)
      .then((result) => {
        if (current) setLevel(result.level);
      })
      .catch(() => {
        if (current) setLevel("");
      });
    return () => {
      current = false;
    };
  }, [progress.xp]);
  const currentQuestions = useMemo(
    () =>
      Object.entries(practice?.[selectedDay] ?? {}).flatMap(
        ([topic, questions]) =>
          questions.map((_, index) => ({
            key: `${selectedDay}-${topic}-${index}`,
          })),
      ),
    [practice, selectedDay],
  );
  const updateProgress = (transform: (current: Progress) => Progress) =>
    setProgress((current) => transform(current));

  async function generatePlan() {
    setBusy("Generating your roadmap…");
    setNotice("");
    try {
      setRoadmap(await learningApi.roadmap(language, provider));
      setPractice(null);
      setSelectedDay("day_1");
      setProgress(emptyProgress);
    } catch (error) {
      setNotice(
        error instanceof Error
          ? error.message
          : "Could not generate your roadmap.",
      );
    } finally {
      setBusy("");
    }
  }
  async function generatePractice() {
    if (!roadmap) return;
    setBusy("Generating practice questions…");
    setNotice("");
    try {
      setPractice(await learningApi.practice(language, roadmap, provider));
    } catch (error) {
      setNotice(
        error instanceof Error
          ? error.message
          : "Could not generate practice questions.",
      );
    } finally {
      setBusy("");
    }
  }
  async function checkAnswer(key: string, question: string) {
    const code = progress.answers[key] ?? "";
    if (!code.trim()) {
      setNotice("Add your answer before checking it.");
      return;
    }
    setBusy("Checking your answer…");
    setNotice("");
    try {
      const result = await learningApi.evaluate(
        language,
        question,
        code,
        provider,
      );
      const alreadyCorrect = progress.correct.includes(key);
      const newlyCorrect = result.correct && !alreadyCorrect;
      const dayComplete =
        currentQuestions.length > 0 &&
        currentQuestions.every((item) =>
          item.key === key
            ? result.correct
            : progress.correct.includes(item.key),
        );
      const newlyCompleted =
        dayComplete && !progress.completed.includes(selectedDay);
      const completion = newlyCompleted
        ? await learningApi.completion(
            Number(selectedDay.replace("day_", "")),
            progress.completed.length + 1,
            progress.completed.length > 0,
          )
        : null;
      if (completion) playCompletionSound(completion.achievement);
      updateProgress((current) => {
        const correct =
          result.correct && !alreadyCorrect
            ? [...current.correct, key]
            : current.correct;
        const completed = completion
          ? [...current.completed, selectedDay]
          : current.completed;
        const xp =
          current.xp +
          (newlyCorrect ? result.xp_awarded : 0) +
          (completion?.xp ?? 0);
        return {
          ...current,
          results: { ...current.results, [key]: result.feedback },
          correct,
          completed,
          xp,
        };
      });
    } catch (error) {
      setNotice(
        error instanceof Error ? error.message : "Could not check your answer.",
      );
    } finally {
      setBusy("");
    }
  }
  async function getHint(key: string, question: string, level: 1 | 2) {
    const charged = progress.charged.includes(key);
    setBusy("Getting a hint…");
    setNotice("");
    try {
      const { hint, xp_cost } = await learningApi.hint(
        language,
        question,
        level,
        progress.xp,
        charged,
        provider,
      );
      updateProgress((current) => ({
        ...current,
        hints: { ...current.hints, [`${key}-${level}`]: hint },
        xp: current.xp - xp_cost,
        charged:
          level === 2 && xp_cost > 0
            ? [...current.charged, key]
            : current.charged,
      }));
    } catch (error) {
      setNotice(
        error instanceof Error ? error.message : "Could not generate a hint.",
      );
    } finally {
      setBusy("");
    }
  }
  async function downloadPdf() {
    setBusy("Preparing your PDF…");
    setNotice("");
    try {
      if (!roadmap)
        throw new Error("Generate a roadmap before downloading the PDF.");
      const blob = await learningApi.downloadPdf(roadmap);
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "SkillForge_Roadmap.pdf";
      link.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      setNotice(
        error instanceof Error ? error.message : "Could not create your PDF.",
      );
    } finally {
      setBusy("");
    }
  }
  function updateAnswer(key: string, value: string) {
    updateProgress((current) => ({
      ...current,
      answers: { ...current.answers, [key]: value },
    }));
  }
  return {
    roadmap,
    practice,
    selectedDay,
    setSelectedDay,
    progress,
    level,
    busy,
    notice,
    setNotice,
    currentQuestions,
    generatePlan,
    generatePractice,
    checkAnswer,
    getHint,
    downloadPdf,
    updateAnswer,
  };
}
