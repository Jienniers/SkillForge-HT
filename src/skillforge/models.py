"""Type aliases for the JSON-shaped curriculum data."""

type Roadmap = dict[str, list[str]]
type PracticeDay = dict[str, list[str]]
type PracticePlan = dict[str, PracticeDay]
