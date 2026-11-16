# College Hackathon & Project Defense Presentation Script
## AI Interview Preparation & Evaluation System

**Candidate / Presenter:** Rajan Kumar Prajapati  
**Branch:** B.Tech — Computer Science & Engineering (Artificial Intelligence)  
**Institution:** Bansal Institute of Engineering & Technology, Lucknow  
**Session:** 2025–2026  
**Presentation Deck:** `AI_Interview_System_Presentation.pptx` (8 Slides)  
**Total Target Duration:** 7–9 Minutes (approx. 1 minute per slide + demo/Q&A)

---

## 🎯 Executive Presentation Strategy (Hackathon Style)

- **Tone:** Confident, energetic, product-focused, and technically grounded. Speak like a startup founder or lead product engineer pitching an innovative solution, not a student reading textbook definitions.
- **Pacing:** Aim for 130–150 words per minute. Pause for 1–2 seconds after key impact statements.
- **Body Language:** Look directly at the examination panel. Point to the genuine UI screenshots and data flow charts on the screen.
- **Key Message:** *"We built an autonomous, privacy-preserving AI mentor that solves placement anxiety with real engineering—combining Google Gemini, local Whisper speech-to-text, client-side computer vision heuristics, and PostgreSQL."*

---

## Slide 1: Introduction & Title
**Slide Title:** *AI Interview Preparation & Evaluation System*  
**Key Visual:** Project Title Banner, Academic Metadata, and Live Webcam UI Screenshot.

### 🎙️ Spoken Script (45–60 Seconds)
> "Respected external examiner, Head of Department, and faculty members. Good morning. 
> 
> My name is **Rajan Kumar Prajapati**, and I am a final-year B.Tech student in Computer Science & Engineering with specialization in Artificial Intelligence at **Bansal Institute of Engineering & Technology, Lucknow**.
> 
> Today, I am excited to present our college mini-project: the **'AI Interview Preparation & Evaluation System'**.
> 
> Over 80% of engineering graduates face intense anxiety and unexpected rejections during campus placement drives. The issue isn't that students don't know computer science theory—it's that they lack realistic, objective, and judgment-free practice. 
> 
> To solve this, we engineered a full-stack, multi-modal web platform that simulates realistic video mock interviews. It listens to candidate answers with local neural speech recognition, analyzes non-verbal delivery signals in the browser, grades responses across an objective four-pillar rubric using Google Gemini, and tracks performance over time in a persistent PostgreSQL database.
> 
> Let us look at the exact problem we set out to solve."

---

## Slide 2: Problem & Our Solution
**Slide Title:** *Bridging the College-to-Corporate Placement Gap*  
**Key Visual:** Two-Column Comparison Card (Red 'Traditional Preparation' vs. Green 'AI Solution').

### 🎙️ Spoken Script (50–60 Seconds)
> "If you look at the left side of this slide, traditional interview preparation has four critical flaws:
> 
> First, **peer mock interviews are subjective**. Classmates cannot provide deep technical rubrics or consistent scoring.
> 
> Second, **verbal deficiencies go unnoticed**. Candidates are unaware that they speak at an erratic 190 words per minute or repeat filler words like *'um'* and *'basically'* twenty times in a single answer.
> 
> Third, **camera presence is overlooked**. In modern virtual campus drives, candidates frequently look away from the webcam or slouch, resulting in silent rejection.
> 
> And fourth, **commercial platforms are expensive**—charging upwards of ₹10,000 a month.
> 
> On the right side is our solution: an autonomous, always-available platform. It provides **multi-axis AI scoring** across technical accuracy and relevance; **deterministic speech pacing** that benchmarks speaking tempo against corporate standards; **client-side behavioral telemetry** for eye-gaze and posture; and **complete, zero-cost accessibility** on any student laptop."

---

## Slide 3: Key Features
**Slide Title:** *Engineered for Real-World Placement Success*  
**Key Visual:** 6 Feature Cards with vibrant accent icons.

### 🎙️ Spoken Script (55–65 Seconds)
> "Our system delivers six core, production-verified features:
> 
> 1. **Dynamic AI Questions:** The system generates technical, behavioral STAR-method, and system design questions adapted to Beginner, Intermediate, and Advanced tiers.
> 2. **Resume & Job Description Skill Matching:** Candidates can upload a PDF resume. Our `pypdf` pipeline extracts technical competencies, compares them against the job description, and targets candidate skill gaps during the interview.
> 3. **Local Neural Speech-to-Text:** Using `faster-whisper` quantized to 8-bit integers on standard CPU, audio is transcribed in under 3 seconds with zero cloud audio leakage.
> 4. **Camera Behavioral Telemetry:** Browser-side canvas heuristics quantify eye-gaze engagement, head pose stability, posture, and room lighting.
> 5. **Multi-Pillar Scoring Rubrics:** Responses are graded from 0 to 10 on Relevance, Accuracy, Communication, and Confidence, paired with actionable improvement advice.
> 6. **Performance Dashboard & History:** Every session is permanently stored in PostgreSQL, allowing students to visualize their score progress over time."

---

## Slide 4: How the System Works
**Slide Title:** *End-to-End Candidate Practice Lifecycle*  
**Key Visual:** 5-Step Linear Process Pipeline (01 to 05) with bottom performance pill.

### 🎙️ Spoken Script (55–65 Seconds)
> "This slide illustrates the seamless end-to-end architecture of our application.
> 
> - **In Step 1**, the candidate selects their target role—such as Full Stack Developer or Data Analyst—and uploads their PDF resume.
> - **In Step 2**, Google Gemini receives this context and generates tailored questions designed specifically to probe the candidate's verified skills and missing gaps.
> - **In Step 3**, the candidate enters the live interview room. WebRTC streams the camera feed while the browser canvas samples downscaled frames at 2.5 frames per second to track gaze and posture.
> - **In Step 4**, as the student speaks, `faster-whisper` converts their voice into text on the CPU while our deterministic communication engine measures speaking pace in words per minute.
> - **Finally, in Step 5**, Gemini scores the transcript against our multi-pillar rubric, and the entire session is committed in an atomic PostgreSQL transaction.
> 
> Notice that the total response evaluation latency is under 3.5 seconds, and zero video frames are ever sent over the network."

---

## Slide 5: Technology Stack
**Slide Title:** *Production-Grade, Modular Technology Stack*  
**Key Visual:** 6 Domain Architecture Cards (Frontend, Backend, Database, LLM, Speech, Vision).

### 🎙️ Spoken Script (50–60 Seconds)
> "Every technology on this slide is genuinely implemented and verified in our codebase:
> 
> - **On the Frontend:** We built a high-performance Single Page Application using **React 19** and **Vite 8**, styled with custom CSS variables to avoid heavy third-party UI dependencies.
> - **On the Backend:** We use **FastAPI** running on Python 3.13 with Uvicorn ASGI server and Pydantic v2 for strict type safety.
> - **For the Database:** We chose **PostgreSQL 16** with **SQLAlchemy 2.0** and **Alembic** additive migrations, guaranteeing zero data loss.
> - **For Generative AI:** We integrate Google's latest **`gemini-3.5-flash-lite`** model via the official `google-genai` SDK for low-latency question generation and rubric evaluation.
> - **For Speech Recognition:** We run **`faster-whisper`** locally on the CPU with 8-bit quantization, eliminating cloud transcription costs and protecting student privacy.
> - **And for Vision & Documents:** We use **HTML5 Canvas** pixel differencing for real-time telemetry and **`pypdf`** for in-memory resume parsing."

---

## Slide 6: Actual Project Demonstration
**Slide Title:** *Actual Working Interface in Action*  
**Key Visual:** 4 High-Resolution Screenshots of the running application.

### 🎙️ Spoken Script (60–75 Seconds)
> *(Point directly to the four screenshots on the slide)*
> 
> "Here you can see the actual working application captured directly from our running system:
> 
> - **Top-Left (Screen 1):** Shows our **Interview Setup screen**. Candidates select their role, difficulty, question count, and upload their resume. You can see the extracted skill badges and matched competencies.
> - **Top-Right (Screen 2):** Shows the **Live Mock Interview screen**. On the left is the AI question prompt and voice recording controls; on the right is the active WebRTC camera preview with real-time hardware status indicators.
> - **Bottom-Left (Screen 3):** Shows the **Comprehensive Performance Report**. Notice the overall score of **8.9 out of 10**, the four competency progress bars, verbal delivery metrics showing **140 Words Per Minute**, and our camera telemetry showing **84% eye contact** and **90% upright posture**.
> - **Bottom-Right (Screen 4):** Shows the **Candidate Dashboard**. It tracks overall practice hours, average scores, chronological score trends, and allows one-click drilldowns into past sessions."

---

## Slide 7: Results, Impact & Future Scope
**Slide Title:** *Measurable Value & Future Enhancements*  
**Key Visual:** Two High-Impact Columns (Verified Impact vs. Future Roadmap).

### 🎙️ Spoken Script (50–60 Seconds)
> "What are the tangible outcomes of this system?
> 
> First, it provides **immediate delivery diagnostics**—alerting students if they speak too fast, too slow, or use excessive filler words.
> Second, it provides **targeted technical revision** by probing exact resume skill gaps rather than generic trivia.
> Third, it **eliminates interview anxiety** through unlimited private practice.
> And fourth, it offers **privacy by design**—voice is processed locally, and video never leaves browser memory.
> 
> Looking to the future, we have a clear engineering roadmap:
> 1. Integrating the **Gemini Live Audio API** for natural conversational interruptions and live interviewer follow-ups.
> 2. Embedding an in-browser **Monaco coding sandbox** for live algorithm execution.
> 3. Building an **Institutional Training & Placement Portal** so college placement officers can assign interview batches and export readiness reports.
> 4. And adding **Client WebAssembly FaceMesh** for micro-expression feedback."

---

## Slide 8: Conclusion & Thank You
**Slide Title:** *Empowering Every Candidate with Objective AI Mentorship*  
**Key Visual:** 3 Takeaway Cards, Presenter & Institution Banner, Call-to-Action.

### 🎙️ Spoken Script (45–60 Seconds)
> "To conclude, our AI Interview Preparation & Evaluation System accomplishes three key milestones:
> 
> 1. It is a **fully functional, verified multi-modal platform** combining Generative AI, local speech recognition, and computer vision with zero simulated or fake data.
> 2. It is **privacy-first and zero-cost**, ensuring every engineering student can prepare effectively without financial barriers.
> 3. It is **production and viva ready**, verified by automated test suites and one-click execution scripts.
> 
> I extend my sincere gratitude to the Department of Computer Science & Engineering at **Bansal Institute of Engineering & Technology, Lucknow**, and to our project guides and faculty for their continuous support.
> 
> Thank you for your time and attention. I am now open to your questions and eager to demonstrate the live application."

---

## 💡 Anticipated Viva Questions & Bulletproof Answers

### Q1: Why did you run speech-to-text locally with faster-whisper instead of using Google Cloud Speech API?
> **Answer:**  
> *"Two reasons: cost and privacy. Cloud speech APIs charge per audio minute, which creates an ongoing expense for college students. By using `faster-whisper` with 8-bit integer quantization on the CPU, transcription runs completely free in under 3 seconds. Furthermore, student audio stays strictly on the local machine and is unlinked immediately after transcription, ensuring 100% data privacy."*

### Q2: How does your camera-based behavioral analysis work without heavy server GPU processing?
> **Answer:**  
> *"We offload video processing entirely to the client's browser using the HTML5 Canvas API (`willReadFrequently: true`). Every 400 milliseconds, downscaled 160x120 frames are analyzed for upper-third facial skin distribution to estimate camera gaze, and temporal frame differencing to quantify head and posture movement. Only lightweight statistical aggregates (e.g., 84% gaze engagement) are sent to the backend. This gives us zero server GPU load and zero video streaming bandwidth."*

### Q3: How do you prevent the AI from hallucinating or giving generic scores?
> **Answer:**  
> *"We use structured prompt engineering backed by Pydantic JSON schemas. The Gemini prompt requires the model to score four explicit dimensions (Relevance, Technical Accuracy, Communication, Confidence) from 0 to 10 and cite specific evidence from the student's transcribed answer. If the answer is vague or inaccurate, the model must explicitly list the omission under 'weaknesses' and provide an improved technical explanation."*

### Q4: How is candidate performance stored and tracked over time?
> **Answer:**  
> *"We use PostgreSQL with an additive schema managed by Alembic. Every completed interview commits a parent `interviews` record, child `interview_questions` records, and `communication_metrics` in a single atomic transaction. The `/api/dashboard/stats` endpoint runs aggregate SQL queries across past sessions to compute overall averages and historical score trajectories."*
