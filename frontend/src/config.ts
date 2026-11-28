import type { AIProvider } from "./types/provider";
import type { Theme } from "./types/theme";

// Change this value to choose the provider used for users without a saved preference.
export const DEFAULT_AI_PROVIDER: AIProvider = "gemini";

// Change this value to choose the theme used for users without a saved preference.
export const DEFAULT_THEME: Theme = "dark";
