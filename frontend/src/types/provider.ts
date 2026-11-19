export type AIProvider = "local" | "gemini";
export const aiProviders: { value: AIProvider; label: string }[] = [
  { value: "local", label: "Local (LM Studio)" },
  { value: "gemini", label: "Gemini" },
];
