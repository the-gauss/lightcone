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

Environment variables live in `.env` (see `.env.example`).

## Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

The UI posts YouTube URLs to `POST /api/v1/youtube/process`.
