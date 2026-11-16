# B.Tech Mini Project Presentation Content
## AI Interview Preparation & Evaluation System

**Candidate:** Rajan Kumar Prajapati  
**Branch:** B.Tech — Computer Science & Engineering (Artificial Intelligence)  
**Institution:** Bansal Institute of Engineering & Technology, Lucknow  
**Session:** 2025–2026  

---

## Slide 1: Title Slide

### Slide Title
**AI Interview Preparation & Evaluation System**  
*An Intelligent Multi-Modal Platform for Automated Mock Interview Simulation, Speech Analysis, and Behavioral Evaluation*

### Main Content
- **Project Type:** B.Tech Mini Project
- **Student Name:** Rajan Kumar Prajapati
- **Branch / Specialization:** Computer Science & Engineering (Artificial Intelligence)
- **Department:** Department of Computer Science & Engineering
- **Institution:** Bansal Institute of Engineering & Technology (BIET), Lucknow
- **Affiliation:** Dr. A.P.J. Abdul Kalam Technical University (AKTU), Uttar Pradesh

### Presenter Notes (Spoken Script)
> "Respected external examiner, department head, and respected faculty members. Good morning. My name is Rajan Kumar Prajapati, a student of B.Tech Computer Science and Engineering with specialization in Artificial Intelligence at Bansal Institute of Engineering & Technology, Lucknow. Today, I am proud to present my B.Tech mini project titled **'AI Interview Preparation & Evaluation System'**.
> 
> In this presentation, I will walk you through the real-world engineering challenge that inspired this work, the multi-modal system architecture combining Large Language Models, local neural speech transcription, and client-side computer vision heuristics, followed by our database design, automated testing, and live system demonstration."

### Suggested Visuals
- High-resolution BIET Lucknow and AKTU logos.
- Professional modern title graphic showing an interviewer AI hologram connecting with a student at a webcam.

---

## Slide 2: Abstract & Executive Summary

### Slide Title
**Project Abstract: Bridging the College-to-Corporate Transition**

### Main Content
- **Core Mission:** Deliver an accessible, automated, and objective mock interview environment for engineering students facing placement rounds.
- **Multi-Modal AI Pipeline:**
  - **Generative AI:** Google Gemini (`gemini-3.5-flash-lite`) for role-adaptive technical and behavioral question generation and rubric-based response evaluation.
  - **Local Neural STT:** `faster-whisper` (`base` model, int8 CPU quantization) for zero-cloud-cost, privacy-preserving audio transcription.
  - **Computer Vision Telemetry:** Real-time client-side HTML5 canvas frame analysis capturing eye-gaze engagement, head pose stability, posture alignment, and environmental lighting.
  - **Resume-JD Skill Gap Analysis:** Automated PDF parsing extracting technical proficiencies and matching against employer job descriptions.
  - **Persistent Relational Analytics:** PostgreSQL backend storing granular evaluation rubrics, temporal session data, and longitudinal skill trends.

### Presenter Notes (Spoken Script)
> "Engineering graduates often face significant hurdles when transitioning to corporate placement drives. While students may understand theoretical computer science, they struggle with articulate verbal delivery, time management, and interview anxiety. 
> 
> Professional human coaching is cost-prohibitive for most college students. Our solution provides an always-available, objective AI mentor that evaluates not just the technical correctness of the student's answer, but also observable delivery indicators—such as speaking pace, filler word frequency, and camera engagement—delivering actionable personalized feedback within seconds."

### Suggested Visuals
- 3-pillar diagram: **Input Modalities** (Speech, Camera, Resume PDF) $\rightarrow$ **AI Processing Core** (Gemini, Whisper, Canvas CV) $\rightarrow$ **Actionable Output** (Granular Scoring, Behavioral Feedback, Longitudinal Dashboard).

---

## Slide 3: Problem Statement & Motivation

### Slide Title
**The Problem: Limitations of Conventional Interview Preparation**

### Main Content
- **1. Subjective & Inconsistent Feedback:** Peer mock interviews lack rigorous technical depth and objective scoring rubrics.
- **2. The 'Confidence vs. Competence' Gap:** Students who know how to solve a coding challenge often struggle to communicate their thought process under pressure.
- **3. Hidden Speech Deficiencies:** Excessive filler words (*"um"*, *"like"*, *"you know"*) and erratic speaking tempos (>180 WPM or <90 WPM) severely degrade interviewer perception.
- **4. Unmonitored Non-Verbal Delivery:** In modern remote video interviews, eye contact, upright posture, and framing make or break candidate selection.
- **5. High Commercial Cost:** Industry coaching platforms charge prohibitive subscription fees, creating an access barrier for collegiate students.

### Presenter Notes (Spoken Script)
> "When we investigated why candidates fail campus placement interviews, the data revealed a recurring pattern: failure is rarely caused by a complete lack of technical knowledge. Rather, it is caused by disjointed delivery, nervous filler words, poor eye engagement with the camera lens, and an inability to structure complex thoughts in concise English.
> 
> Furthermore, university placement cells cannot conduct five personalized mock interviews for every graduating student each semester due to faculty time constraints. This project directly solves that scalability bottleneck."

### Suggested Visuals
- Infographic showing typical student interview hurdles: anxiety icon, filler word counter, high commercial coaching prices, and placement rejection stats.

---

## Slide 4: Proposed Solution & Key Objectives

### Slide Title
**The Solution: An Autonomous, Multi-Modal Mock Interview Platform**

### Main Content
- **Objective 1 — Intelligent Question Generation:** Dynamically generate technical, behavioral, system design, and soft skill questions tailored to specific roles, experience tiers, and uploaded candidate resumes.
- **Objective 2 — Private Speech Transcription:** Capture verbal responses via browser audio APIs and transcribe them locally using `faster-whisper` without leaking student audio to third-party cloud servers.
- **Objective 3 — Multi-Dimensional Scoring Rubrics:** Assess every answer across four distinct axes: *Relevance*, *Technical Accuracy*, *Communication Clarity*, and *Observable Confidence*.
- **Objective 4 — Privacy-Preserving Behavioral Telemetry:** Sample video frames directly in the browser to quantify camera gaze, posture, and stability without streaming heavy video over the internet.
- **Objective 5 — Continuous Improvement Loop:** Track progress across multiple sessions via a persistent PostgreSQL database and an interactive visual dashboard.

### Presenter Notes (Spoken Script)
> "To address this challenge systematically, we established five strict engineering objectives. First, the questions must be genuinely dynamic—adapting to whether a candidate is interviewing for a Junior Frontend Developer or an Associate Data Engineer role. Second, speech processing must be privacy-compliant and run locally. Third, evaluations must never use arbitrary 'black box' numbers; every score must be backed by a clear rubric. Fourth, visual indicators must be measured client-side to respect bandwidth and privacy. And fifth, all performance data must persist across time so candidates can visibly track their growth."

### Suggested Visuals
- Circular feedback cycle: **Practice** $\rightarrow$ **Evaluation** $\rightarrow$ **Targeted Feedback** $\rightarrow$ **Re-practice**.

---

## Slide 5: Real-World Relevance & Target Audience

### Slide Title
**Target Audience & Societal Impact**

### Main Content
- **Primary Beneficiaries:**
  - **B.Tech / MCA / BCA Students:** Preparing for campus recruitment drives (TCS, Infosys, Wipro, Cognizant, Tech Mahindra, product startups).
  - **Self-Taught Developers & Career Switchers:** Needing realistic interview practice tailored to their non-traditional resumes.
  - **Collegiate Training & Placement Cells (T&P):** Offering continuous, unconstrained mock interview facilities without faculty burnout.
- **Pedagogical Alignment:**
  - Builds verbal fluency in technical English.
  - Cultivates the **STAR methodology** (Situation, Task, Action, Result) for behavioral scenarios.
  - Demystifies automated corporate Applicant Tracking Systems (ATS) and remote video hiring processes.

### Presenter Notes (Spoken Script)
> "This system directly targets pre-final and final-year engineering students. In Tier-2 and Tier-3 institutions like ours, students possess strong technical foundations but often miss out on Tier-1 placement packages because of communication inhibitions. By giving each student a private, judgment-free platform to practise speaking aloud into a camera, their confidence grows exponentially before they ever step into an actual corporate interview."

### Suggested Visuals
- Photos or mockups of students practicing on laptops with the interface, plus company hiring logos.

---

## Slide 6: High-Level System Architecture

### Slide Title
**Full-Stack System Architecture & Data Flow**

### Main Content
```
 ┌────────────────────────────────────────────────────────┐
 │                   BROWSER CLIENT                      │
 │   React 19 SPA • Vite • Web Audio API • MediaStream    │
 │       Canvas Vision Telemetry (Gaze, Posture, Light)   │
 └─────────────┬──────────────────────────▲───────────────┘
               │ JSON / FormData          │ JSON Responses
               ▼                          │
 ┌────────────────────────────────────────┴───────────────┐
 │                  FASTAPI REST BACKEND                  │
 │   CORS Middleware • SQLAlchemy ORM • Alembic Migrations │
 └──────┬────────────────────┬────────────────────┬───────┘
        │                    │                    │
        ▼                    ▼                    ▼
 ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
 │ POSTGRESQL  │      │ GOOGLE AI   │      │ FASTER-     │
 │ DATABASE    │      │ GEMINI SDK  │      │ WHISPER     │
 │ 127.0.0.1   │      │ 3.5 Flash   │      │ Local CPU   │
 └─────────────┘      └─────────────┘      └─────────────┘
```
- **Loose Coupling:** Clean boundary between presentation, business logic, persistence, and AI pipelines.
- **Asynchronous Execution:** Non-blocking FastAPI endpoints ensuring rapid response times.

### Presenter Notes (Spoken Script)
> "Here we see the complete architectural diagram of the system. The frontend is built with React 19 and bundled using Vite, communicating over high-speed RESTful JSON APIs with a FastAPI backend.
> 
> When the candidate begins an interview, FastAPI coordinates three specialized worker engines: the Google Gemini SDK for intelligent prompt generation and answer evaluation; the faster-whisper local neural engine for speech transcription; and the PostgreSQL relational database with connection pooling for transactional persistence.
> 
> Notice that the computer vision analysis runs directly on the candidate's browser via an HTML5 canvas worker, meaning no continuous video stream is transmitted over the network."

### Suggested Visuals
- High-contrast block diagram using the Mermaid flow shown above with color-coded component blocks.

---

## Slide 7: Frontend Architecture & User Experience

### Slide Title
**Frontend Design: Intuitive, Accessible, and Responsive**

### Main Content
- **Modern Technology Stack:** React 19, Vite build tool, modular vanilla CSS custom properties (design system without bloated external UI libraries).
- **Four Core State-Based Views (Single-Page Navigation):**
  1. `interview`: Setup wizard $\rightarrow$ Live question prompt $\rightarrow$ Dual camera/mic capture $\rightarrow$ Instant rubric report.
  2. `dashboard`: Aggregate metrics, score trends, competency bars, and recent sessions.
  3. `history`: Chronological interview list with status filters, delete controls, and deep-dive links.
  4. `report`: Granular inspection of historical interview sessions.
- **Hardware Lifecycle Management:** Automatic MediaStream track shutdown (`stream.getTracks().forEach(t => t.stop())`) upon navigation or interview completion to prevent webcam resource lockups.

### Presenter Notes (Spoken Script)
> "For the frontend, we deliberately chose React 19 paired with Vite. Vite gives us sub-second hot-module reloading and a production bundle size under 280 kilobytes.
> 
> Rather than relying on heavy third-party UI libraries like Material-UI or Bootstrap, we engineered a dedicated CSS design system based on modern CSS variables. This ensures full responsiveness from 4K desktop screens down to mobile viewports.
> 
> Crucially, we implemented strict hardware lifecycle management. Whenever an interview concludes or the user navigates away, all video and microphone tracks are explicitly terminated, guaranteeing the user's camera hardware indicator light turns off immediately."

### Suggested Visuals
- UI screenshot collage: Setup view, Live interview view, and Performance Dashboard.

---

## Slide 8: Backend Architecture & REST API Design

### Slide Title
**FastAPI Backend: High-Throughput, Modular, and Type-Safe**

### Main Content
- **Framework:** FastAPI running on Uvicorn ASGI server with automatic OpenAPI/Swagger documentation generation.
- **RESTful Endpoints Summary:**
  - `POST /api/questions`: Generate dynamic questions with role, difficulty, and resume skills.
  - `POST /api/transcribe`: Ingest multi-part WebM audio and return Whisper transcript and duration.
  - `POST /api/evaluate`: Comprehensive rubric evaluation, verbal metrics, and database persistence.
  - `POST /api/resume-job/profile`: Parse resume PDF and extract skill match/gap profile.
  - `GET /api/interviews` & `GET /api/interviews/{id}`: Paginated history and detailed reports.
  - `GET /api/dashboard/stats`: Aggregated analytics and competency distributions.
- **Enterprise Patterns:**
  - Dependency-injected database sessions (`Depends(get_db)`).
  - Explicit database rollbacks inside `try...except` blocks.
  - Cross-Origin Resource Sharing (CORS) configured for port `5173`.

### Presenter Notes (Spoken Script)
> "The backend is engineered with FastAPI. FastAPI offers Python 3 type hinting via Pydantic schemas, high-throughput asynchronous execution, and automatic Swagger documentation at `/docs`.
> 
> We organized our endpoints into modular routers. Every request follows strict transaction isolation: if an evaluation fails mid-way, `db.rollback()` executes automatically, preventing orphaned database records.
> 
> In addition, we enforce connection pre-pinging in SQLAlchemy, which eliminates stale socket disconnections with PostgreSQL."

### Suggested Visuals
- Screenshot of the Swagger interactive UI at `http://127.0.0.1:8000/docs` showing all active routes.

---

## Slide 9: Database Schema & Relational Design

### Slide Title
**PostgreSQL Relational Schema & Data Integrity**

### Main Content
- **Primary Tables:**
  1. `interviews`: Master session record (`id`, `interview_type`, `question_count`, `overall_score`, `created_at`).
  2. `interview_questions`: Granular question-answer records (`question_number`, `question`, `answer`, `relevance`, `technical_accuracy`, `communication`, `confidence`, `overall_score`, `strengths`, `weaknesses`, `improvement_feedback`).
  3. `communication_metrics`: Delivery telemetry (`speaking_pace_wpm`, `filler_word_count`, `filler_word_rate`, `audio_duration_seconds`, `camera_gaze_metric`, `posture_metric`, `face_present`).
  4. `resumes`: Uploaded resume tracking and extracted JSON skills list.
  5. `job_descriptions`: Target job role descriptions and competency criteria.
- **Migration Engine:** Version-controlled via Alembic (`phase9_10_additive_001`). Strict zero-drop database protection.

### Presenter Notes (Spoken Script)
> "Data integrity is fundamental to any enterprise software application. Our PostgreSQL relational database uses a normalized schema with strict foreign key constraints and cascade rules.
> 
> The `interviews` table serves as the parent record. Each session links one-to-many with `interview_questions`, capturing individualized sub-scores and feedback for every question answered. 
> 
> The `communication_metrics` table records speech pacing and visual metrics. Furthermore, all schema modifications are managed through additive Alembic migrations, ensuring that our reference datasets and live candidate history are never dropped or corrupted."

### Suggested Visuals
- Entity-Relationship (ER) diagram showing `interviews` linked to `interview_questions`, `communication_metrics`, `resumes`, and `job_descriptions`.

---

## Slide 10: AI Question Generation Engine

### Slide Title
**Dynamic AI Question Generation via Google Gemini**

### Main Content
- **Model:** `gemini-3.5-flash-lite` through the official `google-genai` Python SDK.
- **Context Injection Pipeline:**
  - Role (`Software Engineer`, `Data Analyst`, etc.)
  - Interview Type (`technical`, `behavioral`, `system_design`, `hr`)
  - Difficulty Tier (`beginner`, `intermediate`, `advanced`)
  - Optional Subject Focus (e.g. *Operating Systems, Computer Networks*)
  - Candidate Resume Skills & Missing Competency Gaps
- **Prompt Engineering & Output Sanitization:**
  - System prompts enforce output of strictly one plain question per line.
  - Automated regex cleans Markdown fences (` ``` `), asterisks, and numbering prefix artifacts.
  - Fallback domain questions maintain zero-downtime reliability if external API quotas are encountered.

### Presenter Notes (Spoken Script)
> "Let us look at how questions are generated. We utilize Google's newest `gemini-3.5-flash-lite` model.
> 
> Rather than asking generic trivia, our prompt engineering injects specific contextual parameters: the candidate's chosen role, the requested difficulty tier, and most importantly, any skills identified from their uploaded resume.
> 
> If a candidate's resume lists Python and SQL but lacks System Design, the model intelligently formulates questions that test their core knowledge while probing potential skill gaps. The output is thoroughly sanitized through automated text filters to ensure clean rendering."

### Suggested Visuals
- Before-and-after prompt engineering comparison: Raw candidate input $\rightarrow$ Structured Gemini prompt $\rightarrow$ Generated questions.

---

## Slide 11: Resume & Job Description Skill Gap Analysis

### Slide Title
**Resume Parsing & Target Role Alignment**

### Main Content
- **PDF Extraction Engine:** Native binary stream extraction using `pypdf` (v7.1.0) with multi-page safety limits (up to 20 pages, 10 MB maximum).
- **Intelligent Keyword Matching:**
  - Regular-expression word-boundary scanning across 60+ industry tech skills (*Python, Java, React, Docker, Kubernetes, AWS, PyTorch, SQL, REST APIs, etc.*).
  - Case-insensitive normalization preventing false sub-word matches.
- **Gap Identification Algorithm:**
  $$\text{Matched Skills} = \text{Resume Skills} \cap \text{Job Skills}$$
  $$\text{Skill Gaps} = \text{Job Skills} \setminus \text{Resume Skills}$$
- **Direct Impact:** Identified skill gaps are fed directly into the interview generator to simulate targeted corporate placement questions.

### Presenter Notes (Spoken Script)
> "A major highlight of this project is our Resume and Job Description analysis module. 
> 
> Candidates can upload their resume in PDF format. Using `pypdf`, we extract the textual content and apply boundary-aware regular expression scanning across comprehensive technical vocabularies.
> 
> We compute the set intersection and set difference between the candidate's extracted proficiencies and the job requirements. The resulting skill gaps are displayed to the student and automatically passed into Gemini to generate tailored questions that challenge those exact areas."

### Suggested Visuals
- Screenshot of the Resume Upload interface in `InterviewSetup.jsx` showing extracted skills badges and matched skill gap cards.

---

## Slide 12: Speech-to-Text Pipeline (faster-whisper)

### Slide Title
**Local Speech-to-Text via faster-whisper**

### Main Content
- **Architecture:** Local neural speech recognition using OpenAI's Whisper model reimplemented in CTranslate2 (`faster-whisper`).
- **Optimization Strategy:**
  - Model variant: `base` (~73M parameters).
  - Quantization: `int8` on multi-core CPU.
  - Latency: 1.5 to 3.5 seconds for a standard 30-second spoken answer.
- **Privacy & Security Advantages:**
  - Zero candidate voice data is transmitted across public cloud networks.
  - Audio files are processed as temporary WebM files on the local filesystem and immediately unlinked in a `finally:` block.
- **Fault-Tolerant Fallback:** Full manual text editing support in case of ambient noise or hardware limitations.

### Presenter Notes (Spoken Script)
> "Speech recognition is handled using `faster-whisper`. Unlike standard Whisper, `faster-whisper` uses CTranslate2, which delivers up to four times faster inference with memory-efficient 8-bit quantization on standard desktop CPUs.
> 
> There are two major reasons we chose local STT over cloud APIs: first, cost—it costs zero dollars per API call; second, candidate privacy. The student's voice recording is saved in a temporary buffer, transcribed, and deleted immediately from disk. Candidates can also review and polish their transcribed text before submission."

### Suggested Visuals
- Benchmark chart comparing cloud speech API latency/cost vs. local `faster-whisper` CPU execution.

---

## Slide 13: Verbal Communication & Delivery Metrics

### Slide Title
**Verbal Delivery Metrics: Quantifying Speaking Tempo & Fluency**

### Main Content
- **1. Speaking Pace (Words Per Minute — WPM):**
  $$\text{WPM} = \frac{\text{Total Spoken Words}}{\text{Audio Duration in Seconds}} \times 60$$
  - **Optimal Range:** 120–160 WPM (*Typical conversational pacing*).
  - **Pacing Alerts:** Flagged as *Fast* (>160 WPM) or *Slow* (<100 WPM).
- **2. Filler Word Detection:**
  - Lexical token matching for high-frequency filler phrases: *"um"*, *"uh"*, *"like"*, *"you know"*, *"basically"*, *"sort of"*, *"actually"*, *"literally"*.
  - **Filler Rate Percentage:**
    $$\text{Filler Rate} = \frac{\text{Filler Word Count}}{\text{Total Spoken Words}} \times 100\%$$
  - Evaluated as *Low* ($\le 1\%$), *Moderate* ($1–3\%$), or *Frequent* ($>3\%$).

### Presenter Notes (Spoken Script)
> "How do we measure delivery? We quantify two core verbal attributes: Speaking Pace and Filler Word Density.
> 
> In professional communication, the target conversational rate is 120 to 160 words per minute. If a candidate rushes through their answer at 190 WPM, interviewers struggle to follow; if they speak at 85 WPM, they appear hesitant.
> 
> Simultaneously, our algorithm detects verbal crutches such as 'um', 'basically', and 'you know'. The system calculates exact filler density and provides actionable advice, such as encouraging the student to take silent one-second pauses instead of vocalized fillers."

### Suggested Visuals
- Gauges showing WPM speedometer (Red: Slow, Green: 120-160 WPM, Red: Fast) and a filler words breakdown chart.

---

## Slide 14: Computer Vision & Behavioral Telemetry

### Slide Title
**Advanced Client-Side Camera Behavioral Telemetry**

### Main Content
- **Privacy-Preserving Mechanism:** HTML5 Canvas frame sampling at 2.5 FPS (400 ms intervals); zero raw video is recorded or streamed to servers.
- **Telemetry Indicators:**
  - **Camera Gaze & Eye Engagement:** Upper-third facial skin distribution heuristic measuring sustained attention toward the webcam lens.
  - **Head Pose Stability:** Temporal frame differencing in the upper bounding region to detect excessive nodding, tilting, or restlessness.
  - **Body Posture & Framing:** Center-of-mass vertical tracking detecting slouching, leaning, or leaving the camera frame.
  - **Gestures & Motion:** Lower-third motion tracking capturing natural versus excessive hand gestures.
  - **Lighting Quality:** Luminance histogram analysis alerting candidates to poor lighting or severe glare.
- **Strict Educational Disclaimer:** Explicitly labeled as observable delivery signals; never claims to assess internal psychological states or emotional mind-reading.

### Presenter Notes (Spoken Script)
> "In virtual hiring, camera presence is essential. We implemented a lightweight, non-blocking computer vision module in JavaScript using HTML5 Canvas.
> 
> Every 400 milliseconds, the client-side analyzer samples a downscaled frame to compute luminance, facial centering, vertical posture, and movement deltas. It assesses whether the candidate is maintaining eye contact with the camera lens, whether they are slouching, and whether their room lighting is sufficient.
> 
> We adhere strictly to ethical AI guidelines: we label these metrics as 'Observable Delivery Indicators'. We make it clear that the AI is evaluating delivery habits for practice, not attempting psychological mind-reading."

### Suggested Visuals
- Canvas sampling diagram showing face bounding box, eye level zone, and lower-third gesture zone.

---

## Slide 15: AI Evaluation & Scoring Rubrics

### Slide Title
**Multi-Dimensional Evaluation & Scoring Rubrics**

### Main Content
- **Comprehensive Evaluation Axes (0 to 10 Scale):**
  - **Relevance:** Does the response directly address the core prompt?
  - **Technical Accuracy:** Are engineering principles, algorithms, and concepts correctly explained?
  - **Communication Clarity:** Is the answer logically structured with concise, professional vocabulary?
  - **Observable Confidence:** Is the delivery structured, decisive, and free from excessive uncertainty?
- **Weighted Overall Score:**
  $$\text{Overall Score} = 0.35 \times \text{Tech} + 0.30 \times \text{Rel} + 0.20 \times \text{Comm} + 0.15 \times \text{Conf}$$
- **Anti-Hallucination Guarantees:** Strict JSON schemas enforce verifiable reasoning and prevent generic praise.

### Presenter Notes (Spoken Script)
> "When evaluating responses, our prompt engineering enforces an objective four-pillar rubric: Relevance, Technical Accuracy, Communication Clarity, and Observable Confidence.
> 
> Technical accuracy receives the highest weighting at 35%, followed by relevance at 30%, communication at 20%, and observable confidence at 15%. 
> 
> The AI must cite specific evidence from the student's transcript to justify its score. It cannot simply say 'Good job'—it must state what was correct, what was missing, and provide an improved sample answer."

### Suggested Visuals
- 4-bar competency visualization alongside the mathematical weighting formula.

---

## Slide 16: Personalized Feedback Synthesis

### Slide Title
**Actionable Personalized Feedback & Improvement Roadmaps**

### Main Content
- **Synthesized Action Plan:**
  - **✓ Verified Strengths:** Identifies demonstrated competencies (e.g. *"Strong explanation of ACID properties and database indexing"*).
  - **! Areas for Growth:** Pinpoints specific omissions or inaccuracies (e.g. *"Failed to discuss edge cases when handling binary tree null nodes"*).
  - **🎯 Recommended Practice Topics:** Prescribes 2–3 concrete technical and delivery exercises for the candidate's next session.
- **Cross-Modal Telemetry Integration:**
  - If filler rate exceeds 3% $\rightarrow$ *"Practise pausing silently for 1–2 seconds."*
  - If camera gaze is under 55% $\rightarrow$ *"Position webcam at eye level to enhance audience connection."*
  - If posture slouching is detected $\rightarrow$ *"Maintain upright posture to project composure."*

### Presenter Notes (Spoken Script)
> "Feedback is only valuable if it is actionable. Our feedback engine synthesizes data across both evaluation dimensions: technical content and behavioral delivery.
> 
> As you can see on this slide, if a candidate demonstrated great technical knowledge but looked away from the camera and used frequent filler words, the personalized roadmap addresses both: recommending advanced architecture practice while suggesting eye-level webcam alignment and silent pauses. This creates a complete coaching experience."

### Suggested Visuals
- Screenshot of the Personalized Feedback section from a live interview report showing strengths, weaknesses, and practice recommendations.

---

## Slide 17: Candidate Dashboard & Historical Analytics

### Slide Title
**Longitudinal Analytics & Performance Tracking**

### Main Content
- **Interactive Dashboard Capabilities:**
  - **Key Performance Indicators (KPIs):** Total interviews completed, total practice duration, average score across all sessions, and latest performance verdict.
  - **Score Progression Chart:** Visual line graph tracing score trajectories across successive sessions.
  - **Competency Distribution Breakdown:** Average scores across Relevance, Technical Accuracy, Communication, and Confidence.
  - **Recent Sessions Quick-List:** One-click navigation to past session reports.
- **History Management:**
  - Filter by interview type (*Technical, Behavioral, System Design*).
  - Search and deep-dive into full question-by-question historical reports.
  - Delete past practice sessions with safe cascade database cleanup.

### Presenter Notes (Spoken Script)
> "To provide long-term value, we built a comprehensive Candidate Dashboard and History view.
> 
> Every session is permanently recorded in PostgreSQL. When candidates open the dashboard, they see high-level KPIs: their total practice count, average score, and a chronological progression chart showing whether their performance is improving over time.
> 
> In the History tab, candidates can search past sessions, compare technical versus behavioral performances, or review past answers before a real interview."

### Suggested Visuals
- Full dashboard screenshot showing KPI cards, score trend line chart, and competency progress bars.

---

## Slide 18: Security, Privacy & Database Protection

### Slide Title
**Software Security, Data Protection & Ethical AI**

### Main Content
- **1. Zero Audio/Video Cloud Leakage:** Audio is transcribed locally; camera frames are processed exclusively inside browser memory.
- **2. Strict Credential Isolation:** API keys and PostgreSQL credentials reside in `.env` files with sample templates provided; never committed to git.
- **3. Transactional Integrity:** All database operations use scoped sessions and rollback on failure.
- **4. Strict Schema Safety (Rule 3):**
  - Zero database or table drops.
  - Zero migration resets.
  - Additive migrations only (`phase9_10_additive_001`).
- **5. Ethical Transparency:** Transparent explanations, student-centric disclaimers, and zero automated hiring discrimination.

### Presenter Notes (Spoken Script)
> "Security and engineering ethics were central to our implementation. 
> 
> First, student privacy is protected by design: video frames never leave client RAM, and voice audio is transcribed locally on CPU and deleted immediately.
> 
> Second, our backend implements strict credential isolation and SQL transaction rollbacks. 
> 
> Third, from a database perspective, we enforce additive migrations—never dropping tables or resetting migration history.
> 
> Finally, we provide explicit educational disclaimers so candidates understand that this tool is an educational coach, not a discriminatory automated hiring filter."

### Suggested Visuals
- Security shield graphic displaying: Local STT, Ephemeral Video, Scoped SQL Transactions, and Zero Data Leaks.

---

## Slide 19: System Testing, Verification & QA Results

### Slide Title
**Verification & Automated Quality Assurance**

### Main Content
- **Automated End-to-End Test Suite (`backend/test_system.py`):**
  - **Test 1:** Server Health Check (`GET /health`) $\rightarrow$ **PASS**
  - **Test 2:** AI Question Generation (`POST /api/questions`) $\rightarrow$ **PASS**
  - **Test 3:** Verbal Metric Computation (Pace & Fillers) $\rightarrow$ **PASS**
  - **Test 4:** Gemini Rubric Evaluation & Persistence (`POST /api/evaluate`) $\rightarrow$ **PASS**
  - **Test 5:** Visual Telemetry Storage & Schema Check $\rightarrow$ **PASS**
  - **Test 6:** Dashboard Aggregation Endpoint (`GET /api/dashboard/stats`) $\rightarrow$ **PASS**
- **Frontend Production Build Verification:**
  - Build command: `npm --prefix frontend run build`
  - Output: 23 modules compiled in **362ms** with **0 build errors**.
- **No Mock Data in Production (Rule 6):** 100% verified real database transactions and genuine Gemini AI responses.

### Presenter Notes (Spoken Script)
> "To guarantee software reliability, we developed a comprehensive automated test script: `test_system.py`.
> 
> This test verifies every critical pathway: server health, dynamic question generation, verbal metric calculation, evaluation storage in PostgreSQL, visual telemetry persistence, and dashboard aggregation. All tests pass with zero errors.
> 
> On the frontend, Vite compiles all 23 JSX and CSS modules into optimized static bundles in just 362 milliseconds. Most importantly, per Rule 6 of our engineering guidelines, zero simulated timeouts or hardcoded dummy scores are used in production flows."

### Suggested Visuals
- Terminal screenshot showing the green `[PASS]` output from `python backend/test_system.py` and the successful `npm run build` output.

---

## Slide 20: Engineering Challenges & Implemented Solutions

### Slide Title
**Engineering Challenges & Technical Solutions**

### Main Content
| Challenge | Root Cause | Engineering Solution Implemented |
| :--- | :--- | :--- |
| **Windows Sandbox Socket Restrictions** | Windows sandbox isolating port 5432 and 8000 | Implemented `pool_pre_ping=True` and environment-aware execution patterns. |
| **Heavy Computer Vision Overhead** | Python MediaPipe packages failing on Python 3.13 | Developed client-side HTML5 Canvas pixel differencing and luminance heuristics (zero pip bloat). |
| **Scattered Environment Variables** | `load_dotenv()` failing when scripts executed from different directories | Standardized `Path(__file__).resolve().parent / ".env"` across all backend modules. |
| **Camera Hardware Lockups** | Lingering browser media tracks after session completion | Enforced explicit MediaStream track termination in React cleanup hooks. |
| **Model Deprecation Drift** | Legacy Gemini model names deprecated by Google | Upgraded to the high-speed, cost-effective `gemini-3.5-flash-lite` model. |

### Presenter Notes (Spoken Script)
> "During the development lifecycle, we tackled several non-trivial engineering challenges.
> 
> For example, when exploring computer vision libraries like MediaPipe, we found they experienced binary dependency conflicts on the latest Python 3.13 runtime. Rather than downgrading our Python environment or adding hundreds of megabytes of heavy wheel files, we architected a lightweight, browser-native canvas solution that computes gaze and posture in JavaScript with zero backend latency.
> 
> We also resolved directory-sensitive environment loading by anchoring all `.env` lookups to absolute module paths."

### Suggested Visuals
- Comparison diagram: Heavy server-side video streaming vs. Lightweight browser canvas telemetry.

---

## Slide 21: Future Scope & Roadmap

### Slide Title
**Future Enhancements & Scalability Roadmap**

### Main Content
- **1. Real-Time Interactive Voice Streaming:** Integrating the Gemini Live Audio API for natural conversational back-and-forth interruptions.
- **2. Live In-Browser Code Execution Sandbox:** Adding Monaco Editor (VS Code core) and WebAssembly Python/JavaScript execution for live coding rounds.
- **3. Advanced Computer Vision via WebAssembly:** Integrating lightweight FaceMesh landmarks running entirely on client GPU via WebGL.
- **4. Enterprise College LMS / Placement Portal Integration:** Role-based access control (RBAC) allowing college placement officers to assign mock interview batches and export student readiness spreadsheets.
- **5. Automated Video Recording Playback:** Optional encrypted video replay with timestamped AI critique markers.

### Presenter Notes (Spoken Script)
> "Looking ahead, this project has immense potential for expansion. 
> 
> Our immediate next step is integrating the Gemini Live Audio API to enable real-time conversational interruptions, replicating an interviewer who asks follow-up questions when a candidate hesitates.
> 
> We also plan to integrate an in-browser coding sandbox using Monaco Editor and WebAssembly, allowing candidates to code data structure algorithms while explaining their logic out loud.
> 
> Finally, we envision integrating with our college placement portal so training coordinators can monitor cohort readiness metrics at scale."

### Suggested Visuals
- Product roadmap timeline showing Phase 1 (Current Core), Phase 2 (Live Coding & Wasm), and Phase 3 (Institutional T&P Portal).

---

## Slide 22: Conclusion & Acknowledgements

### Slide Title
**Conclusion & Acknowledgements**

### Main Content
- **Summary of Achievements:**
  - Successfully designed, developed, integrated, and verified a multi-modal AI Interview Preparation & Evaluation System.
  - Seamlessly fused Generative AI (Gemini), Neural Speech-to-Text (`faster-whisper`), Client-Side Computer Vision, and PostgreSQL persistence into a unified React 19 application.
  - Created standalone one-click execution scripts (`START_PROJECT.bat`) ensuring 100% independent operation.
- **Acknowledgements:**
  - Department of Computer Science & Engineering, Bansal Institute of Engineering & Technology, Lucknow.
  - Project guides, faculty mentors, and collegiate peers for feedback and domain guidance.
- **Contact:**
  - **Student:** Rajan Kumar Prajapati
  - **Email:** Student Portal / Institutional Registry

### Presenter Notes (Spoken Script)
> "In conclusion, the AI Interview Preparation & Evaluation System successfully demonstrates how modern artificial intelligence, speech processing, and web engineering can be combined to solve a tangible problem faced by thousands of graduating engineers.
> 
> I extend my heartfelt gratitude to my project guide, the Head of Department, and the faculty members of the Computer Science & Engineering department at Bansal Institute of Engineering & Technology for their continuous encouragement and guidance throughout this project.
> 
> Thank you for your time and attention. I am now open to your questions, feedback, and ready to demonstrate the live application."

### Suggested Visuals
- Thank You graphic, BIET Lucknow emblem, and invitation banner for Live Demonstration & Q&A.
