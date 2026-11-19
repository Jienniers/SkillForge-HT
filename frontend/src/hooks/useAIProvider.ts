import { useEffect, useState } from "react";
import type { AIProvider } from "../types/provider";

const STORAGE_KEY = "skillforge-ai-provider";

function storedProvider(): AIProvider {
  try {
    return localStorage.getItem(STORAGE_KEY) === "gemini" ? "gemini" : "local";
  } catch {
    return "local";
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
