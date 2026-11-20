import { useEffect, useState } from "react";
import { DEFAULT_AI_PROVIDER } from "../config";
import type { AIProvider } from "../types/provider";

const STORAGE_KEY = "skillforge-ai-provider";

function storedProvider(): AIProvider {
  try {
    const savedProvider = localStorage.getItem(STORAGE_KEY);
    return savedProvider === "local" || savedProvider === "gemini"
      ? savedProvider
      : DEFAULT_AI_PROVIDER;
  } catch {
    return DEFAULT_AI_PROVIDER;
  }
}

export function useAIProvider() {
  const [provider, setProvider] = useState<AIProvider>(storedProvider);

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, provider);
    } catch {
      // Keep the selected provider for this session when storage is unavailable.
    }
  }, [provider]);

  return { provider, setProvider };
}
