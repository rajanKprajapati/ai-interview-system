# Complete User & Operator Guide

## AI Interview Preparation & Evaluation System
**Candidate / Student:** Rajan Kumar Prajapati  
**Branch:** B.Tech Computer Science & Engineering (Artificial Intelligence)  
**Institution:** Bansal Institute of Engineering & Technology, Lucknow  

---

## 1. Quick Start (One-Click Launch)

The repository provides automated startup scripts in the root directory:

1. **Start Both Backend and Frontend:**
   Double-click `START_PROJECT.bat` in Windows Explorer, or run in PowerShell:
   ```powershell
   .\START_PROJECT.bat
   ```
   This script:
   - Validates that Python and Node.js are available.
   - Launches the FastAPI backend in a dedicated console window on `http://127.0.0.1:8000`.
   - Launches the React/Vite frontend in a dedicated console window on `http://localhost:5173`.
   - Displays all active endpoints and documentation links.

2. **Access the Application:**
   - **Interactive Web App:** [http://localhost:5173](http://localhost:5173)
   - **Backend API & Swagger Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **API Health Endpoint:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

3. **Stop All Services Safely:**
   Double-click `STOP_PROJECT.bat`, or run:
   ```powershell
   .\STOP_PROJECT.bat
   ```
   This detects and terminates only the processes listening on ports `8000` and `5173` without affecting unrelated background processes.

---

## 2. Manual Startup Commands

If you prefer starting services manually inside your development environment:

### Terminal 1 — Backend (FastAPI + PostgreSQL + Gemini + Whisper)
```powershell
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
*Note:* The Whisper model initializes on first audio capture. The backend will confirm database connection and route registration upon boot.

### Terminal 2 — Frontend (React 19 + Vite)
```powershell
cd frontend
npm install   # (only needed first time)
npm run dev
```

---

## 3. Database Verification (PostgreSQL)

The application requires an active PostgreSQL server.

- **Default Port:** `5432`
- **Database Name:** `ai_interview_db`
- **User:** `postgres`
- **Environment Configuration:** Defined in `backend/.env` as:
  ```env
  DATABASE_URL=postgresql://postgres:<password>@localhost:5432/ai_interview_db
  ```

### Verify PostgreSQL Service Status (Windows)
Open an administrative PowerShell or Services manager:
```powershell
Get-Service postgresql*
```
If stopped, start the service:
```powershell
Start-Service postgresql-x64-16  # (adjust version if applicable)
```

### Apply Migrations
Database schemas are version-controlled via Alembic:
```powershell
cd backend
python -m alembic upgrade head
```

---

## 4. End-to-End Interview Walkthrough

### Step 1: Configuration & Setup
1. Open [http://localhost:5173](http://localhost:5173).
2. Choose your **Interview Type**:
   - `Technical`: In-depth coding, architecture, and language fundamentals.
   - `Behavioral`: STAR-method situational challenges and teamwork scenarios.
   - `System Design`: Scalability, databases, caching, and microservices.
   - `HR & Soft Skills`: Career goals, cultural alignment, and work ethic.
3. Select target **Role** (e.g. *Software Engineer*, *Data Scientist*, *Full Stack Developer*).
4. Select target **Difficulty** (*Beginner*, *Intermediate*, *Advanced*).
5. Choose number of questions (1 to 10; default is 5).
6. *(Optional)* **Upload Resume PDF**:
   - Click "Browse" and upload your resume in `.pdf` format.
   - The system automatically extracts verified technical skills and identifies missing competencies against the target role.
7. Click **"Begin Mock Interview"**.

### Step 2: Camera & Microphone Setup
1. In the interview window, click **"Enable Camera & Mic"**.
2. When prompted by Chrome or Edge, click **"Allow"**.
3. Your live camera feed will appear in the webcam preview pane with status `LIVE`.

### Step 3: Answering Questions
1. Review the AI-generated question displayed in the question card.
2. Click **"🎙 Start Voice Answer"**.
3. Speak clearly into your microphone:
   - Client-side canvas vision heuristics capture non-invasive framing and gaze telemetry.
   - Whisper audio captures speech duration and cadence.
4. When finished speaking, click **"■ Stop Recording"**.
5. Local Whisper Speech-to-Text automatically transcribes your answer into the text area in 1–3 seconds.
6. Edit or refine your text if desired, then click **"Submit & Next Question →"**.

### Step 4: Comprehensive Evaluation Report
Once all questions are submitted, the Gemini AI pipeline synthesizes:
- **Overall Score** (0–10 scale) and verdict (*Excellent*, *Good*, *Passing*, *Needs Practice*).
- **Core Competencies**: Relevance, Technical Accuracy, Communication Clarity, Observable Confidence.
- **Verbal Delivery Indicators**: Speaking tempo in Words Per Minute (WPM), filler word count and density percentage.
- **Visual Delivery Telemetry**: Camera gaze engagement percentage, head pose stability, upright posture consistency, hand gesture presence, and lighting status.
- **Personalized Action Plan**: Concrete strengths, identified weaknesses, and targeted topics for revision.
- **Question-by-Question Rubrics**: Detailed score breakdowns and AI improvement suggestions for each answer.

### Step 5: Dashboard & Historical Analytics
- **Dashboard Tab:** Review your overall performance trends, total practice hours, average competencies, and competency distribution.
- **History Tab:** Search, filter, and inspect past interview reports or delete outdated test sessions.

---

## 5. Troubleshooting & FAQ

| Problem | Cause | Resolution |
| :--- | :--- | :--- |
| **`Database connection failed`** | PostgreSQL is stopped or password in `.env` is invalid | Verify PostgreSQL is running on port 5432. Check `backend/.env` matches your local PostgreSQL credentials. |
| **`Camera/Mic permission denied`** | Browser permissions blocked | Click the lock icon in Chrome/Edge URL address bar -> Set Camera and Microphone to **"Allow"** -> Reload page. |
| **`AI Question generation fails`** | Missing or exhausted Gemini API key | Check `backend/.env` for a valid `GEMINI_API_KEY`. Free API keys can be generated at [Google AI Studio](https://aistudio.google.com/). |
| **`Port 8000 or 5173 already in use`** | Previous instance still running | Run `STOP_PROJECT.bat` or kill the ports via `netstat -ano | findstr :8000`. |
| **`faster-whisper high CPU usage`** | Model running on multi-thread CPU | Normal during speech transcription (typically 2–4 seconds per answer). The model uses `int8` quantization for optimal CPU efficiency. |

---

## 6. Production & Public Deployment Guide

To deploy this project as a publicly accessible web application:

### Database (Managed Cloud PostgreSQL)
1. Provision a free managed PostgreSQL instance on [Supabase](https://supabase.com/) or [Neon](https://neon.tech/).
2. Copy the external connection URI into your production environment variables (`DATABASE_URL`).
3. Run Alembic migrations against the cloud database:
   ```bash
   alembic upgrade head
   ```

### Backend (Render / Railway / AWS EC2)
1. Create a Web Service on Render or Railway connected to your GitHub repository.
2. Root directory: `backend/`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Set environment variables:
   - `DATABASE_URL` = `<your_supabase_postgres_url>`
   - `GEMINI_API_KEY` = `<your_gemini_api_key>`
   - `GEMINI_MODEL` = `gemini-3.5-flash-lite`

### Frontend (Vercel / Netlify)
1. Connect your repository to Vercel or Netlify.
2. Root directory: `frontend/`
3. Build command: `npm run build`
4. Output directory: `dist`
5. Set environment variable:
   - `VITE_API_BASE_URL` = `https://<your-backend-app>.onrender.com`
