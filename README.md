# Taptym demo app

This repository contains a small Vue + FastAPI demo app.

## Project structure

- `frontend/` — Vue 3 frontend
- `backend/` — FastAPI backend API

## Requirements

- Node.js 18+
- Python 3.11+
- npm
- pip

## 1) Install frontend

```bash
cd frontend
npm install
cp .env.example .env
```

## 2) Install backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## 3) Run backend

```bash
cd backend
source .venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open API docs:

- http://localhost:8000/docs

## 4) Run frontend

```bash
cd frontend
npm run dev -- --host 0.0.0.0
```

Then open:

- http://localhost:5173

## Notes for demo use

- Do not commit `.env`, `.venv`, `node_modules`, uploaded files, or local SQLite DB.
- The repository already includes a sample SQLite database and seed data for quick demo startup.
- If the frontend shows nothing, check that the backend is running and the API URL in `.env` matches `http://localhost:8000`.

## Common issue

Do not run npm commands from the repository root (`/Users/muha/taptym_app`).
The frontend has its own `package.json` in `frontend/`.

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

## Deployment setup

This project is structured as two separate apps:

- `frontend/` for Vercel deployment
- `backend/` for Render deployment

### Frontend on Vercel

1. Import the repository into Vercel.
2. Set Root Directory to `frontend`.
3. Keep the default Vite preset.
4. Add environment variable:

```bash
VITE_API_URL=https://your-render-backend-url.onrender.com
```

5. Deploy.

### Backend on Render

1. Create a new Web Service in Render.
2. Set Root Directory to `backend`.
3. Build command:

```bash
pip install -r requirements.txt
```

4. Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

5. Add environment variable:

```bash
FRONTEND_ORIGINS=https://your-vercel-app.vercel.app
```

> For a quick demo, SQLite is enough. For real production, use PostgreSQL instead of the local SQLite database.
cd /Users/muha/taptym_app/backend
DATABASE_URL=sqlite:///./taptym.db .venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
> cd /Users/muha/taptym_app/frontend
npm run dev -- --host 0.0.0.0
