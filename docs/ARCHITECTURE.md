# System Architecture

```mermaid
graph TD
    User["Candidate / Web Browser"]

    subgraph Frontend["React 19 + Vite Frontend"]
        Nav["Navigation & State Shell (App.jsx)"]
        Setup["Interview Setup & PDF Upload (InterviewSetup.jsx)"]
        InterviewComp["Live Camera & Speech Interface (Interview.jsx)"]
        DashComp["Analytics Dashboard (Dashboard.jsx)"]
        HistComp["Session History (History.jsx)"]
        ReportComp["Report Inspector (ReportDetail.jsx)"]
        APIClient["API Client (services/api.js)"]
    end

    subgraph Backend["FastAPI Python Backend"]
        FastAPIApp["FastAPI Main Application (main.py)"]
        QGen["AI Question Engine (ai_question_generator.py)"]
        Eval["AI Evaluation Engine (ai_evaluator.py)"]
        STT["Whisper Speech-to-Text (speech_to_text.py)"]
        CommServices["Delivery & Feedback Engine (phase7_11_services.py)"]
        Routers["Add-on Routers (phase7_11_router, phase9_10_router)"]
    end

    subgraph AI["AI Services"]
        GeminiAPI["Google Gemini API (gemini-3.5-flash-lite)"]
        WhisperModel["faster-whisper CPU (int8 Base Model)"]
    end

    subgraph Storage["PostgreSQL Database"]
        InterviewsTable["interviews"]
        QuestionsTable["interview_questions"]
        MetricsTable["communication_metrics"]
        ResumesTable["resumes"]
        JDTable["job_descriptions"]
    end

    User --> Nav
    Nav --> Setup
    Nav --> InterviewComp
    Nav --> DashComp
    Nav --> HistComp
    Nav --> ReportComp

    Setup --> APIClient
    InterviewComp --> APIClient
    DashComp --> APIClient
    HistComp --> APIClient
    ReportComp --> APIClient

    APIClient -->|REST JSON / Multipart| FastAPIApp

    FastAPIApp --> QGen
    FastAPIApp --> Eval
    FastAPIApp --> STT
    FastAPIApp --> CommServices
    FastAPIApp --> Routers

    QGen -->|Prompt Execution| GeminiAPI
    Eval -->|Rubric Evaluation| GeminiAPI
    STT -->|Audio Transcription| WhisperModel

    FastAPIApp -->|SQLAlchemy ORM| Storage
```

---

## Architectural Highlights
- **Decoupled Architecture**: The React SPA frontend communicates with the FastAPI backend solely via clean RESTful APIs.
- **Local Speech Processing**: Audio transcription runs locally using `faster-whisper` on CPU int8, eliminating cloud STT fees and ensuring zero third-party audio transmission.
- **Single-Transaction Persistence**: Each interview evaluation, along with its questions, metrics, and metadata, is committed in an atomic database transaction.
- **Additive Migrations**: Alembic manages all database migrations additively to guarantee existing candidate records and reference dimensions are preserved.
