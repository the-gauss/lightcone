# Lightcone

Production-style starter for a LangGraph + FastAPI + React stack.

## Structure

- `backend/` FastAPI service with LangGraph workflows
- `frontend/` React (Vite) client
- `main.py` re-exports the FastAPI app for `uvicorn`

## Backend

```bash
uv run uvicorn backend.app.main:app --reload
```

Environment variables live in `.env` (see `.env.example`). The backend auto-loads
`.env` for local development; in production, set real env vars instead.

## Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

The UI posts YouTube URLs to `POST /api/v1/youtube/process`.

## Gemini

Set `GOOGLE_AI_STUDIO_API_KEY` (or `GEMINI_API_KEY`) and optionally `GEMINI_MODEL`
to enable summarization.

The backend downloads the YouTube video and sends it to Gemini for multimodal
summarization. Large videos may fail; adjust `MAX_VIDEO_MB` as needed. Some
videos require `ffmpeg` for stream merging if no progressive MP4 is available.
