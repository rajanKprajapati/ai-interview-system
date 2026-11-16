# Production Deployment Guide
**AI Interview Preparation & Evaluation System**

This guide covers preparing, configuring, and deploying the application as a secure, publicly accessible web application.

---

## 1. Production Architecture Overview

```
[Candidate Browser (HTTPS)]
            │
            ├──────────────────────────┐
            ▼                          ▼
[Frontend Hosting (Vercel / Netlify)]   [Backend Hosting (Render / Railway / VPS)]
  - React 19 / Vite Static Build          - FastAPI ASGI Server (Uvicorn / Gunicorn)
  - Public HTTPS Domain                   - Python 3.13 Runtime
  - Environment: VITE_API_BASE_URL        - faster-whisper (CPU int8)
                                          - Environment: GEMINI_API_KEY, DATABASE_URL
                                                      │
                                                      ▼
                                         [Managed Cloud PostgreSQL]
                                           - Neon / Supabase / Railway
                                           - Persistent storage & SSL connection
```

---

## 2. Recommended Hosting Stack (Practical & Affordable)

1. **Frontend**: **Vercel** or **Netlify** (Free tier with automatic HTTPS and global CDN).
2. **Backend**: **Render** or **Railway** (Linux container with Python 3.13 support).
3. **Database**: **Neon.tech** or **Supabase** (Serverless PostgreSQL with SSL and automated backups).

---

## 3. Step-by-Step Deployment Walkthrough

### Step A: Setup Managed PostgreSQL
1. Create a free PostgreSQL database on [Neon.tech](https://neon.tech/) or [Supabase](https://supabase.com/).
2. Copy the production connection string. It will look like:
   ```
   postgresql://user:password@ep-cool-sample.region.neon.tech/neondb?sslmode=require
   ```

### Step B: Deploy the Backend (FastAPI on Render or Railway)
1. **Repository**: Push this repository to GitHub or GitLab.
2. **Create New Web Service**:
   - Root directory: `backend`
   - Runtime: `Python 3`
   - Build Command:
     ```bash
     pip install -r requirements.txt
     ```
   - Start Command:
     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT --workers 2
     ```
3. **Configure Environment Variables**:
   In the hosting dashboard, add:
   - `GEMINI_API_KEY`: Your Google GenAI API key.
   - `DATABASE_URL`: Your managed PostgreSQL connection string.
4. **Apply Migrations**:
   Run the migration command via SSH console or as a pre-deploy release command:
   ```bash
   alembic upgrade head
   ```
5. **Verify Backend**:
   Open `https://your-backend-url.onrender.com/api/health`.  
   You should see:
   ```json
   { "success": true, "status": "healthy", "database": "connected" }
   ```

### Step C: Deploy the Frontend (React / Vite on Vercel)
1. **Create New Project on Vercel**:
   - Root directory: `frontend`
   - Framework preset: `Vite`
   - Build command: `npm run build`
   - Output directory: `dist`
2. **Configure Environment Variables**:
   Add the backend URL:
   - `VITE_API_BASE_URL`: `https://your-backend-url.onrender.com`
3. **Deploy**:
   Click **Deploy**. Vercel will build the frontend and provide a public HTTPS URL (e.g. `https://ai-interview-system.vercel.app`).

### Step D: Update CORS Configuration
In `backend/main.py`, confirm your public frontend domain is allowed in CORS:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-interview-system.vercel.app",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 4. Production Checklist

- [x] **No hardcoded secrets**: All keys sourced from environment variables.
- [x] **No mock evaluation**: Production mode uses live Gemini API scoring.
- [x] **Clean temporary file handling**: Audio files unlinked after transcription.
- [x] **Additive database schema**: Zero destructive migration commands.
- [x] **HTTPS Enabled**: Encrypted WebRTC audio streams and client-server communication.
- [x] **Health check route active**: `/api/health` monitors DB and ASGI responsiveness.
