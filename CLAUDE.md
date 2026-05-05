# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyDevMap is a full-stack adaptive online learning platform for Python programming. Key features: AI-powered placement testing (IRT algorithm), sandboxed code execution via Docker, Uzbek payment integrations (Payme, Click), and PDF certificate generation. Backend is Django REST Framework; frontend is React + Vite.

## Commands

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver     # http://localhost:8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev      # http://localhost:3000
npm run build
npm run preview
```

### Docker (required for code sandbox)

```bash
docker pull python:3.11-slim
docker run --rm --network=none python:3.11-slim python -c "print('Hello')"
```

### Environment variables

Backend `.env` needs: `ANTHROPIC_API_KEY`, `PAYME_LOGIN`, `PAYME_KEY`, `CLICK_SERVICE_ID`, `CLICK_SECRET_KEY`, and database credentials.

Frontend `.env.local` needs: `VITE_API_URL=http://localhost:8000/api/v1`

## Architecture

### Backend (`backend/`)

- `config/settings/base.py` — Django settings, JWT config (access: 5 min, refresh: 1 day)
- `src/core/models/` — All models. `base.py` has abstract `BaseModel` with timestamps. Subfolders: `course/`, `compiler/`, `quiz/`
- `src/api/views/` — API views grouped by feature: `auth/`, `compiler/`, `course/`, `lesson/`, `quiz/`, `payment/`
- `src/api/urls/` — URL routing, one file per feature, all registered under `/api/v1/`
- `src/api/serializers/` — DRF serializers

### Frontend (`frontend/src/`)

- `context/AuthContext.jsx` — Global auth state with JWT auto-refresh via Axios interceptors
- `context/ThemeContext.jsx` — Dark/light theme
- `services/api.js` — Axios instance; handles token refresh queue for concurrent requests
- `pages/` — Full-page route components
- `components/` — Reusable UI pieces (`PrivateRoute.jsx` guards authenticated routes)

### Key subsystems

**Code execution** (`src/api/views/compiler/run_code.py`): Before Docker execution, code is validated against a banned-import list (`os`, `sys`, `socket`, etc.) and regex patterns for dangerous builtins (`exec`, `eval`, `open`, `compile`). Docker runs with `--network none`, 128 MB memory limit, read-only FS, 50% CPU quota, and a 5-second timeout.

**Adaptive placement test** (`src/api/views/`): IRT-based algorithm, 10–15 questions across 10 Python topics. Difficulty adjusts per answer; questions weighted by difficulty for scoring.

**AI integration**: Uses `claude-haiku-4-5` (via `anthropic` SDK) for placement analysis, code review, career guidance, and the AI advisor chat.

**Payments**: Payme uses Basic Auth + JSON-RPC callbacks; Click uses MD5 signature verification. Both follow a webhook pattern to flip order status to paid and grant course access.

**Certificates**: Generated as PDFs via ReportLab with a QR code linking to a verification URL. Unique ID: `PDM-{MD5(user_id+course_id+date)}`. Users cannot change their display name after a certificate is issued.

### API documentation

Swagger UI available at `/swagger/` when the backend dev server is running (via `drf-yasg`).
