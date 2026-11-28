import { useLayoutEffect, useState } from "react";
import { DEFAULT_THEME } from "../config";
import type { Theme } from "../types/theme";

const STORAGE_KEY = "skillforge-theme";

function storedTheme(): Theme {
  try {
    const savedTheme = localStorage.getItem(STORAGE_KEY);
    return savedTheme === "light" || savedTheme === "dark"
      ? savedTheme
      : DEFAULT_THEME;
  } catch {
    return DEFAULT_THEME;
  }
}

export function useTheme() {
  const [theme, setTheme] = useState<Theme>(storedTheme);

  useLayoutEffect(() => {
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.colorScheme = theme;
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch {
      // Keep the selected theme for this session when storage is unavailable.
    }
  }, [theme]);

  return { theme, setTheme };
}
