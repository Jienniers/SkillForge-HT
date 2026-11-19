# SkillForge

SkillForge is a React + TypeScript learning application backed by a Python API. It uses Google Gemini to generate a 30-day programming roadmap, create practice questions, evaluate code, and provide hints.

## Run locally

1. Install Python dependencies with `pip install -r requirements.txt`.
2. Install frontend dependencies with `cd frontend && npm ci`.
3. Add `GEMINI_API_KEY` to `.env` at the repository root.
4. Start the API from the repository root: `uvicorn main:app --app-dir src --reload`.
5. Start Vite in another terminal: `cd frontend && npm run dev`.

Vite proxies `/api` requests to `http://localhost:8000`. The production Docker image builds the frontend and serves it from the same FastAPI process on port 8000.

## API

- `POST /api/roadmap` — generate and validate a 30-day language plan.
- `POST /api/practice` — generate coding exercises for a plan.
- `POST /api/evaluate` — evaluate a code submission.
- `POST /api/hint` — generate a level 1 or level 2 hint.
- `POST /api/gamification/completion` and `/api/gamification/level` — apply existing XP and level rules.
- `POST /api/roadmap/pdf` — create a PDF from the displayed plan.

The frontend stores learning progress in browser local storage. Gemini generation requires a valid `GEMINI_API_KEY`.
