# Guidelines for AI Coding Agents & Engineers

This document outlines architectural patterns, database safety rules, coding conventions, and operational workflows for any developer or AI coding agent working in the **AI Interview Preparation & Evaluation System** codebase.

---

## 1. Core Architectural Principles

1. **Monorepo Structure**:
   - `backend/`: FastAPI REST API, SQLAlchemy models, Alembic migrations, Gemini AI prompt pipelines, faster-whisper local STT.
   - `frontend/`: React 19 single-page application bundled with Vite. State-based tab routing (`interview`, `dashboard`, `history`, `report`).
   - `docs/`: Technical reference documentation for architecture, database, APIs, testing, and deployment.
2. **Preserve Existing Work**:
   - Always inspect files before editing.
   - Never replace or rewrite existing working components unless technically required.
   - Keep additive changes modular; do not break backwards compatibility with existing endpoints or database schemas.
3. **Never Fake Functionality (Rule 6)**:
   - In production mode, always invoke actual backend endpoints, genuine AI models (Gemini), faster-whisper STT, and persistent PostgreSQL storage.
   - Never use hardcoded response strings, simulated success timeouts, or dummy scores in production flows.
   - Always gracefully handle network outages or API quota limits with descriptive error messages.

---

## 2. Database Protection Rules

The PostgreSQL database contains live candidate interviews and reference tables (`company_dim`, `job_postings_fact`, `skills_job_dim`, `skills_dim`).

1. **NEVER drop the database or existing tables.**
2. **NEVER reset or delete the migration history table (`alembic_version`).**
3. **Always use Additive Migrations**:
   - When modifying or adding schema elements, create an additive Alembic migration.
   - Ensure new columns are nullable or have default values so existing records remain intact.
4. **Use Transactions & Safe Rollbacks**:
   - All multi-table inserts (e.g. `Interview` + `InterviewQuestion` + `CommunicationMetric`) must run inside a single transaction.
   - Wrap operations in `try...except` and call `db.rollback()` on error.
5. **Always test database queries with pre-ping enabled**:
   - `create_engine(..., pool_pre_ping=True)` to prevent stale socket errors.

---

## 3. Backend Conventions

- **Path Resolution for Environment Variables**:
  Always use `Path(__file__).resolve().parent / ".env"` when loading `.env` in backend scripts to ensure scripts function regardless of the working directory.
- **Model Organization**:
  All SQLAlchemy models reside in `backend/models.py`.
  If additional schemas or models are introduced, import and export them through `models.py` to maintain a single source of truth for `alembic/env.py`.
- **AI Integration (Gemini)**:
  - Model: `gemini-3.5-flash-lite` via `google-genai` SDK.
  - Temperature: `0.7` for question generation, minimal thinking level for fast interactive latency.
  - Always sanitize model output: strip leading numbering, bullet points, and markdown code fences before returning structured results.
- **Speech-to-Text (`faster-whisper`)**:
  - Model: `base` loaded globally in `speech_to_text.py` on CPU with `int8` quantization.
  - Always clean up temporary audio files inside a `finally:` block.

---

## 4. Frontend Conventions

- **API Base URL**:
  Always reference `import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"` in API calls. Never hardcode `localhost:8000` inside JSX components.
- **State-Based Navigation**:
  Views are managed through top-level states in `App.jsx` (`currentTab`: `'interview' | 'dashboard' | 'history' | 'report'`).
- **Media Stream Lifecycles**:
  Always stop all media tracks (`stream.getTracks().forEach(t => t.stop())`) when unmounting camera/microphone views or finishing an interview session to prevent hardware lockups.
- **Observable Delivery Indicators**:
  Never claim AI measures internal emotional states or definitive confidence. Always use the term **"Observable Delivery & Communication Indicators"** and provide the educational disclaimer.

---

## 5. Verification & Testing Instructions

Before committing changes or concluding a development turn:
1. Run the automated test suite:
   ```powershell
   python backend/test_system.py
   ```
2. Run the frontend production build:
   ```powershell
   npm --prefix frontend run build
   ```
3. Check `git status` to ensure temporary files, cache directories, or untracked test artifacts are not accidentally staged.
