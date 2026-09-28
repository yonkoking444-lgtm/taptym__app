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
