# Practical Student Guide & Viva Preparation Manual
**AI Interview Preparation & Evaluation System**  
**Student:** Rajan Kumar Prajapati  
**Branch:** B.Tech — Computer Science & Engineering (Artificial Intelligence)  
**Institution:** Bansal Institute of Engineering & Technology, Lucknow  
**Session:** 2025–2026  

---

## 1. Quick Start: How to Run the Project

### Option A: One-Click Launch (Recommended)
Double-click `START_PROJECT.bat` in the project root.  
This automatically validates Python and Node.js, launches the FastAPI backend on `http://127.0.0.1:8000`, and opens the React web app on `http://localhost:5173`.  
To stop services cleanly, run `STOP_PROJECT.bat`.

### Option B: Manual Terminal Execution

#### Terminal 1: Start Backend (FastAPI + PostgreSQL)
```powershell
cd C:\Users\Lenovo\OneDrive\Desktop\ai-interview-system\backend
# Activate your python environment if using venv
# .\venv\Scripts\activate
uvicorn main:app --reload --port 8000
```
- The backend will start on `http://127.0.0.1:8000`.
- Verify by opening `http://127.0.0.1:8000/docs` in your browser.

#### Terminal 2: Start Frontend (React + Vite)
```powershell
cd C:\Users\Lenovo\OneDrive\Desktop\ai-interview-system\frontend
npm run dev
```
- Open `http://localhost:5173` in your browser.

---

## 2. How the Application Works (End-to-End Workflow)

```
[Candidate Opens Web App]
         │
         ▼
[1. Interview Setup]
  - Select Type: Technical / HR / Behavioral
  - Select Difficulty: Easy / Intermediate / Advanced
  - Enter Target Role: e.g. "Software Engineer"
  - Optional: Upload PDF Resume (Skills extracted automatically)
  - Optional: Paste Job Description
         │
         ▼
[2. AI Question Generation]
  - Backend sends role, difficulty, and skills to Gemini AI (`gemini-3.5-flash-lite`)
  - AI generates realistic, tailored questions
         │
         ▼
[3. Camera & Microphone Interview Screen]
  - WebRTC enables live webcam preview and microphone
  - Question 1 displayed with instructions
  - Candidate clicks "Start Voice Answer" and speaks into microphone
  - Candidate clicks "Stop Recording"
         │
         ▼
[4. Speech-to-Text Transcription]
  - Audio chunk (.webm) is uploaded to `/api/transcribe`
  - `faster-whisper` converts speech to text on local CPU
  - Candidate sees transcript and can make corrections if needed
  - Process repeats for all questions
         │
         ▼
[5. AI Evaluation & Delivery Analysis]
  - Candidate submits completed answers
  - Gemini AI evaluates answers across Relevance, Accuracy, Communication, and Confidence
  - Communication algorithm calculates Words Per Minute (WPM) and detects filler words
  - Personalized action plan is synthesized
         │
         ▼
[6. PostgreSQL Persistent Storage]
  - Session record is stored in `interviews` table
  - Individual answers & evaluations stored in `interview_questions`
  - Delivery metrics stored in `communication_metrics`
         │
         ▼
[7. Results & Performance Dashboard]
  - Candidate views instant detailed report
  - Results saved to "Dashboard" and "Session History" for future review
```

---

## 3. Architecture & Main Modules

1. **`backend/main.py`**:
   The primary entrypoint. Configures CORS, mounts routers, and defines endpoints for health checks, question generation, audio transcription, evaluation, session history, and dashboard analytics.
2. **`backend/models.py`**:
   SQLAlchemy database models for `Interview`, `InterviewQuestion`, `CommunicationMetric`, `ResumeRecord`, and `JobDescriptionRecord`.
3. **`backend/ai_question_generator.py`**:
   Integrates with Google GenAI (`gemini-3.5-flash-lite`) using prompt engineering to create mode-specific questions tailored to difficulty and candidate skills.
4. **`backend/ai_evaluator.py`**:
   Sends interview questions and answers to Gemini, validating the returned JSON against a strict scoring rubric.
5. **`backend/speech_to_text.py`**:
   Loads the `faster-whisper` base model on CPU with 8-bit quantization for fast, offline transcription.
6. **`backend/phase7_11_services.py`**:
   Contains business logic for deterministic communication metrics (WPM, filler word detection), PDF text extraction via `pypdf`, skill-matching algorithms, and personalized feedback synthesis.
7. **`frontend/src/InterviewSetup.jsx`**:
   Configuration form with PDF upload and interactive skill preview.
8. **`frontend/src/Interview.jsx`**:
   Live camera interface, recording state management, STT integration, and performance results.
9. **`frontend/src/Dashboard.jsx`**:
   Visual performance analytics with KPI cards, score progress trends, and competency breakdown bars.
10. **`frontend/src/History.jsx` & `ReportDetail.jsx`**:
    Session logs and full historical review of previous interviews.

---

## 4. Database Schema Explained

- **`interviews`**:
  - `id`: Primary key (Integer).
  - `interview_type`: String (technical, hr, behavioral).
  - `question_count`: Integer.
  - `overall_score`: Float (0–10).
  - `created_at`: Timestamp with timezone.
- **`interview_questions`**:
  - `id`: Primary key.
  - `interview_id`: Foreign key to `interviews.id` (Cascading delete).
  - `question_number`: Integer (1, 2, 3...).
  - `question`: Text.
  - `answer`: Text.
  - `relevance`, `technical_accuracy`, `communication`, `confidence`, `overall_score`: Floats (0–10).
  - `strengths`, `weaknesses`: JSON-formatted text.
  - `improvement_feedback`: Text.
- **`communication_metrics`**:
  - `id`: Primary key.
  - `interview_id`: Foreign key to `interviews.id`.
  - `interview_question_id`: Foreign key to `interview_questions.id` (Nullable for session aggregates).
  - `speaking_pace_wpm`: Float (e.g. 135.5).
  - `filler_word_count`: Integer.
  - `filler_word_rate`: Float (percentage).
  - `audio_duration_seconds`: Float.
  - `face_present`: Boolean.
  - `measurement_source`: String.
- **`resumes`** & **`job_descriptions`**:
  - Stores uploaded resume file metadata, extracted skills, and JD text.

---

## 5. Viva Preparation: Questions & Answers for Your Project Defense

### Q1: What problem does your project solve?
**Answer:**  
College graduates and candidates often experience high anxiety and poor preparation for campus placements due to lack of realistic mock interview practice. Our system provides an accessible, AI-powered platform that simulates a real interview environment with webcam preview, voice recording, automatic transcription, objective communication analytics (pace and filler words), and instant, personalized feedback.

### Q2: Why did you choose FastAPI over Flask or Django?
**Answer:**  
FastAPI is an asynchronous, high-performance web framework based on Starlette and Pydantic. It automatically generates interactive OpenAPI/Swagger documentation, enforces strict type validation, and handles async I/O efficiently, which is ideal for streaming audio uploads and external LLM calls.

### Q3: How does speech-to-text work in your system?
**Answer:**  
The candidate's voice is recorded in the browser using the HTML5 `MediaRecorder` API as a WebM audio stream. When recording stops, the audio blob is sent via multipart POST to `/api/transcribe`. The backend utilizes `faster-whisper`, a reimplementation of OpenAI's Whisper model powered by CTranslate2. We use the `base` model with `int8` quantization running on the CPU, achieving fast transcription without requiring an expensive GPU.

### Q4: How is candidate "confidence" measured? Does AI detect emotions?
**Answer:**  
No, we specifically designed our platform **not** to claim psychological emotional detection. Instead, the platform measures quantifiable, observable proxy delivery signals:
1. **Speaking Pace (WPM)**: Words per minute benchmarked against normal conversational pace (120–160 WPM).
2. **Filler Word Density**: Frequency of hesitation markers (*um*, *uh*, *like*, *you know*).
3. **Speech Steadiness & Answer Completeness**: Evaluated based on logical structure and absence of abrupt pauses.
Reports explicitly label these as "Observable Delivery & Communication Indicators".

### Q5: How do you handle database migrations?
**Answer:**  
We use Alembic, SQLAlchemy's migration tool. We follow an additive migration strategy (`alembic upgrade head`), ensuring new tables and columns are introduced without dropping or resetting existing candidate records or reference data.

### Q6: How does the Resume & Job Description personalization work?
**Answer:**  
When a candidate uploads a PDF resume, `pypdf` extracts the raw text in memory. The backend scans the text against technology keywords to build a candidate skill profile. If a Job Description is provided, the system computes skill overlap and identifies skill gaps. These skills and gaps are then injected into the Gemini prompt so the AI generates targeted questions testing both verified competencies and potential gap areas.

### Q7: How does the camera-based behavioral analysis work? Does it stream video to an external server?
**Answer:**  
No video is ever recorded, saved, or streamed to any external cloud server. The camera analysis runs entirely client-side inside the candidate's browser using HTML5 Canvas (`visualAnalysis.js`). At 400 millisecond intervals (2.5 FPS), downscaled frames are sampled to compute:
1. **Camera Gaze & Eye Contact**: Measures upper-center facial skin distribution to detect whether the candidate is looking toward the webcam lens.
2. **Head Pose Stability**: Uses temporal frame differencing in the upper bounding region to quantify head restlessness versus steady posture.
3. **Body Posture & Framing**: Evaluates vertical center-of-mass to detect slouching or leaning.
4. **Lighting Quality**: Calculates average luminance across pixels to alert if lighting is too dim or has glare.
Only aggregated statistical metrics (e.g., 84% gaze engagement, upright posture) are sent with the evaluation payload to be stored in PostgreSQL.

### Q8: What prevents your system from producing 'fake' or hardcoded scores?
**Answer:**  
In production mode, our system strictly enforces real backend API execution:
- Questions are generated dynamically by Google Gemini (`gemini-3.5-flash-lite`).
- Speech is transcribed using the local neural network `faster-whisper`.
- Answer evaluation runs through a multi-dimensional Gemini scoring rubric with Pydantic JSON schema validation.
- All scores, telemetry, and candidate session records are transactionally committed to a live PostgreSQL relational database.
- We have an automated test suite (`backend/test_system.py`) that tests all pathways without dummy placeholders.

---

## 6. Common Errors & Troubleshooting

1. **`ValueError: DATABASE_URL is not set`**:
   - Make sure `backend/.env` exists and contains `DATABASE_URL=postgresql://user:pass@localhost:5432/dbname`.
2. **`psycopg2.OperationalError: connection to server at localhost port 5432 failed`**:
   - PostgreSQL service is not running. Start PostgreSQL via Windows Services or run `net start postgresql-x64-16`.
3. **`Camera or microphone permission was denied`**:
   - Check your browser URL bar: click the lock icon and ensure Camera and Microphone permissions are set to "Allow".
4. **`Whisper model download error`**:
   - On the very first run, `faster-whisper` downloads the base model (~140 MB) from Hugging Face. Ensure internet access is available on first launch.
