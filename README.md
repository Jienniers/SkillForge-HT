# SkillForge

SkillForge is a React + TypeScript learning application backed by a Python API. It uses a local OpenAI-compatible model through LM Studio by default, and can also use Google Gemini. Either provider generates roadmaps, practice questions, answer feedback, and hints.

## Run locally

1. Install Python dependencies with `pip install -r requirements.txt`.
2. Install frontend dependencies with `cd frontend && npm ci`.
3. In LM Studio, load `qwen2.5-coder-7b-instruct` and start the local server on `http://localhost:1234`.
4. Add `GEMINI_API_KEY` to the root `.env` only if you want to use Gemini.
5. Start the API from the repository root: `uvicorn main:app --app-dir src --reload`.
6. Start Vite in another terminal: `cd frontend && npm run dev`.

Vite proxies `/api` requests to `http://localhost:8000`. Use **Settings → AI provider** to switch between Local (LM Studio) and Gemini. The choice is saved in browser local storage. The production Docker image builds the frontend and serves it from the same FastAPI process on port 8000. For Docker, set `LOCAL_AI_BASE_URL` to an address reachable from the container if LM Studio is running on the host.

## API

- `POST /api/roadmap` — generate and validate a 30-day language plan.
- `POST /api/practice` — generate coding exercises for a plan.
- `POST /api/evaluate` — evaluate a code submission.
- `POST /api/hint` — generate a level 1 or level 2 hint.
- `POST /api/gamification/completion` and `/api/gamification/level` — apply existing XP and level rules.
- `POST /api/roadmap/pdf` — create a PDF from the displayed plan.

The frontend stores learning progress, theme, and AI-provider preference in browser local storage. Gemini generation requires a valid `GEMINI_API_KEY`. Local generation uses `LOCAL_AI_BASE_URL` and `LOCAL_AI_MODEL`, which default to the LM Studio URL and model above.
