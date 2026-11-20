export type Roadmap = Record<string, string[]>;
export type PracticePlan = Record<string, Record<string, string[]>>;
export type Progress = {
  xp: number;
  completed: string[];
  answers: Record<string, string>;
  results: Record<string, string>;
  hints: Record<string, string>;
  charged: string[];
  correct: string[];
};
export type Evaluation = {
  feedback: string;
  correct: boolean;
  xp_awarded: number;
};
export const languages = ["Python", "JavaScript", "Java", "C++", "Go"] as const;
export type Language = (typeof languages)[number];
export const emptyProgress: Progress = {
  xp: 0,
  completed: [],
  answers: {},
  results: {},
  hints: {},
  charged: [],
  correct: [],
};
