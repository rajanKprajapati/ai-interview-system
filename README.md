# AI Interview Preparation & Evaluation System

An enterprise-grade, full-stack AI Mock Interview platform designed to help students and candidates practice Technical, HR, and Behavioral interviews with realistic camera and microphone simulations, speech-to-text transcription, Gemini-powered answer evaluation, observable delivery metrics, and an integrated performance dashboard backed by PostgreSQL.

---

## 🌟 Key Features

1. **Adaptive AI Question Generation**:
   - Technical, HR, and Behavioral modes.
   - 3 Difficulty tiers: Easy, Intermediate, Advanced.
   - Role & technology targeting (e.g. Full Stack Developer, Python Backend, Data Scientist).
   - Resume & Job Description integration for personalized questions and skill-gap identification.
2. **Camera & Microphone Simulation**:
   - In-browser WebRTC live camera preview (`getUserMedia`).
   - Browser audio recording via `MediaRecorder` with WebM audio packaging.
   - Visual engagement indicators and mic status badges.
3. **Speech-to-Text Transcription**:
   - High-performance local transcription using `faster-whisper` (`base` model on CPU int8).
   - Automatic speech recognition with transcription editing support.
   - Precise answer duration tracking.
4. **AI-Powered Answer Evaluation**:
   - Evaluates Relevance, Technical Accuracy, Communication Clarity, and Delivery Confidence (0–10 scale).
   - Generates specific verified strengths, growth areas, and actionable improvement recommendations for each answer.
   - Grounded in genuine AI scoring without hardcoded or simulated placeholders.
5. **Observable Delivery & Communication Analytics**:
   - Deterministic speaking pace calculation in Words Per Minute (WPM).
   - Algorithmic filler-word detection (*um*, *uh*, *like*, *basically*, *you know*, etc.) and density percentage.
   - Transparent, observable proxy metrics with explicit student-friendly disclaimers.
6. **Persistent PostgreSQL Database**:
   - SQLAlchemy ORM with additive Alembic migrations.
   - Persistent storage of interview sessions, questions, answers, evaluations, communication metrics, resumes, and job descriptions.
7. **Performance Dashboard & Session History**:
   - KPI metrics: Overall average score, competency averages, total questions attempted.
   - Chronological score trend chart.
   - Session history with filtering, detailed report inspection, and session deletion.
8. **Personalized Action Plans**:
   - Synthesizes session performance into verified strengths and practice recommendations.

---

## 🛠️ Technology Stack

- **Frontend**:
  - React 19
  - Vite 8
  - Modern Responsive CSS (Inter typography, CSS variables, mobile-friendly grid layout)
- **Backend**:
  - Python 3.13
  - FastAPI (REST API & OpenAPI documentation)
  - Uvicorn (ASGI server)
  - Pydantic v2 (Request/Response validation)
- **Database**:
  - PostgreSQL
  - SQLAlchemy 2.0 (ORM)
  - Alembic (Database migrations)
  - Psycopg2-binary
- **AI & Speech Processing**:
  - Google GenAI SDK (`google-genai` with `gemini-3.5-flash-lite`)
  - `faster-whisper` (Local CPU speech-to-text with CTranslate2)
  - `pypdf` (PDF text extraction and skill keyword matching)

---

## 📁 Project Structure

```
ai-interview-system/
├── backend/
│   ├── alembic/                         # Database migration versions & runner
│   │   ├── versions/
│   │   └── env.py
│   ├── database.py                      # SQLAlchemy engine & SessionLocal factory
│   ├── models.py                        # Unified SQLAlchemy database models
│   ├── main.py                          # FastAPI application and REST endpoints
│   ├── ai_question_generator.py         # Adaptive Gemini question engine
│   ├── ai_evaluator.py                  # Structured answer evaluation engine
│   ├── speech_to_text.py                # faster-whisper local transcription service
│   ├── phase7_11_services.py            # WPM, filler regex, resume parsing, feedback
│   ├── phase7_11_router.py              # Confidence, resume, and feedback endpoints
│   ├── phase9_10_router.py              # Persistent metrics & record endpoints
│   ├── phase9_10_schemas.py             # Schema re-exports for backward compatibility
│   ├── test_system.py                   # Automated end-to-end verification test suite
│   ├── requirements.txt                 # Backend Python dependencies
│   ├── alembic.ini                      # Alembic configuration
│   └── .env.example                     # Environment secrets template
├── frontend/
│   ├── src/
│   │   ├── services/
│   │   │   └── api.js                   # Unified frontend API client
│   │   ├── utils/
│   │   │   └── confidencePresentation.js # Delivery indicator formatters
│   │   ├── App.jsx                      # Navigation shell and tab routing
│   │   ├── InterviewSetup.jsx           # Interview configuration, resume & JD upload
│   │   ├── Interview.jsx                # Live camera interview, STT, and results view
│   │   ├── Dashboard.jsx                # Candidate performance analytics & trends
│   │   ├── History.jsx                  # Session log list with filtering
│   │   ├── ReportDetail.jsx             # Comprehensive past interview drilldown
│   │   └── index.css                    # Responsive stylesheet
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── docs/                                # Technical documentation
│   ├── ARCHITECTURE.md
│   ├── DATABASE.md
│   ├── API_AND_WORKFLOWS.md
│   ├── DEPLOYMENT.md
│   └── TESTING.md
├── README.md                            # Main project documentation
├── AGENTS.md                            # Guidelines for future AI agents & developers
├── PROJECT_PROGRESS.md                  # Comprehensive phase verification tracker
└── HELPING_ME.md                        # Student viva preparation & quickstart guide
```

---

## 🚀 Getting Started

### Prerequisites

1. **Python 3.10+** (Python 3.13 recommended)
2. **Node.js 18+** and **npm**
3. **PostgreSQL** running locally on port 5432
4. **Google Gemini API Key** (Free tier available at [Google AI Studio](https://aistudio.google.com/))

---

### Step 1: Backend Setup

1. Open a terminal in `backend/`:
   ```powershell
   cd backend
   ```

2. Create and activate a virtual environment (or use Conda):
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Copy `.env.example` to `.env`:
   ```powershell
   copy .env.example .env
   ```
   Edit `backend/.env` with your actual secrets:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/your_database_name
   ```

5. Run Alembic migrations:
   ```powershell
   alembic upgrade head
   ```

6. Start the FastAPI server:
   ```powershell
   uvicorn main:app --reload --port 8000
   ```
   The backend API will be available at `http://127.0.0.1:8000`.  
   Interactive API docs (Swagger): `http://127.0.0.1:8000/docs`.

---

### Step 2: Frontend Setup

1. Open a new terminal in `frontend/`:
   ```powershell
   cd frontend
   ```

2. Install npm packages:
   ```powershell
   npm install
   ```

3. Configure environment variables (optional for local dev; defaults to port 8000):
   ```powershell
   copy .env.example .env
   ```
   Contents of `frontend/.env`:
   ```env
   VITE_API_BASE_URL=http://127.0.0.1:8000
   ```

4. Start the Vite development server:
   ```powershell
   npm run dev
   ```
   Open `http://localhost:5173` in your browser.

---

## 🧪 Running Automated Tests

Run the full end-to-end verification suite:
```powershell
python backend/test_system.py
```
This automatically verifies:
- Database connectivity & health checks
- Question generation across Technical, HR, and Behavioral modes
- Speech transcription pipeline
- Communication metrics (WPM, filler word density)
- PDF resume skill extraction
- Atomic PostgreSQL persistence of interview sessions, questions, and metrics
- Dashboard aggregation calculations
- Negative edge cases (empty audio, 404s, invalid request payloads)

---

## 🌐 API Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Service health status & database connectivity check |
| `POST` | `/api/questions` | Generates tailored questions based on role, difficulty, and resume skills |
| `POST` | `/api/transcribe` | Transcribes WebM audio recording via faster-whisper |
| `POST` | `/api/evaluate` | Evaluates answers, calculates delivery metrics, and persists to PostgreSQL |
| `GET` | `/api/interviews` | Retrieves list of historical interview sessions |
| `GET` | `/api/interviews/{id}` | Retrieves full question-by-question report for a session |
| `DELETE` | `/api/interviews/{id}` | Deletes a past interview session and associated records |
| `GET` | `/api/dashboard/stats` | Aggregated candidate performance KPIs, trends, and breakdown |
| `POST` | `/api/resume/profile` | Parses PDF resume, extracts skills, and highlights skill gaps vs JD |
| `POST` | `/api/confidence/analyze` | Calculates speaking pace (WPM), filler word counts, and pauses |
| `POST` | `/api/feedback/personalized` | Synthesizes scores into verified strengths and practice advice |

---

## 🔒 Security & Privacy

- All API keys and database credentials reside strictly in `backend/.env` (excluded from git).
- Uploaded audio files are stored in temporary files and immediately deleted after transcription.
- Resume text is parsed in memory; raw resume text is not stored in the database without candidate consent.
- Communication indicators are explicitly labeled as observable delivery signals rather than psychological diagnosis.
