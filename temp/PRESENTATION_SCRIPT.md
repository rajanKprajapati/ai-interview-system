# College Presentation Speaking Script
## AI Interview Preparation & Evaluation System

**Project Title:** AI Interview Preparation & Evaluation System  
**Presentation Deck:** `AI_Interview_System_Presentation.pptx` (8 Slides)  
**Total Target Time:** 7 to 9 Minutes (~1 minute per slide + Demo / Q&A)  
**Language:** Simple, clear, and confident English  

---

### Project Team Members:
1. **Rajan Kumar Prajapati**
2. **Dhruv Maurya**
3. **Saloni**
4. **Harsh Gupta**

**Institution:** Bansal Institute of Engineering & Technology, Lucknow (AKTU Code: 422)  
**Department:** Computer Science & Engineering (Artificial Intelligence)  
**Academic Year:** 2025–2026  

---

## 💡 Quick Tips for a Great Presentation

1. **Speak Slowly and Clearly:** Keep your speaking speed around 130 to 140 words per minute. Do not rush.
2. **Look at the Audience:** Make eye contact with your teachers and external examiners.
3. **Point to the Screen:** When discussing Slide 4 (Workflow) and Slide 6 (Demo Screenshots), physically gesture to the screen to show that you built a real working system.
4. **Keep Sentences Short:** Simple English sounds confident, natural, and professional.
5. **Team Coordination:** If presenting as a team, clearly introduce who is speaking for which section.

---

## Slide 1: Introduction

**Slide Title:** *AI Interview Preparation & Evaluation System*  
**Key Visual:** Project Title, College Details, Team Members List, and Live Camera Interview Screenshot.  
**Target Duration:** 50–60 Seconds  

### 🎙️ What You Should Say:

> "Respected external examiner, Head of Department, and teachers. Good morning.
>
> My name is **Rajan Kumar Prajapati**, and along with my team members **Dhruv Maurya**, **Saloni**, and **Harsh Gupta**, we are final year students of Computer Science & Engineering with specialization in Artificial Intelligence at **Bansal Institute of Engineering & Technology, Lucknow**.
>
> Today, we are proud to present our college mini project: the **'AI Interview Preparation & Evaluation System'**.
>
> Getting placed in a good company is the primary goal of every engineering student. However, many students face intense fear, nervousness, and lack of guidance when facing job interviews.
>
> To solve this problem, we developed a complete web application that acts as a personal AI interview coach. It simulates realistic video interviews using your webcam and microphone, transcribes spoken answers into text directly on your laptop, and evaluates your responses using Google Gemini AI.
>
> It provides instant, objective feedback on technical accuracy and communication delivery so that students can practice anytime and enter campus placement drives with complete confidence.
>
> Let us look at the real-world problems that inspired this project."

---

## Slide 2: Problem Statement

**Slide Title:** *Problem Statement*  
**Key Visual:** Left side shows 5 common student problems. Right side shows reliable industry statistics.  
**Target Duration:** 55–65 Seconds  

### 🎙️ What You Should Say:

> "When preparing for campus placements, college students face several major challenges:
>
> 1. **Lack of Regular Practice:** Colleges have hundreds of graduating students. It is practically impossible for teachers to conduct regular one-on-one mock interviews for everyone.
> 2. **Fear of Speaking:** Many students understand programming and core concepts, but freeze up or get nervous when speaking in English before an interviewer.
> 3. **Difficulty Identifying Mistakes:** When practicing alone in front of a mirror, a student cannot tell whether their answer was technically complete, structured, or clear.
> 4. **No Communication Feedback:** Students are unaware of bad speaking habits—such as speaking too fast, taking long awkward pauses, or repeating filler words like *'um'*, *'uh'*, and *'basically'*.
> 5. **High Commercial Costs:** Professional interview coaching services charge between ₹5,000 to ₹15,000 per month, which most college students cannot afford.
>
> These problems are supported by reliable industry reports:
> - According to the **Wheebox India Skills Report 2024**, over **48%** of Indian graduates lack job-ready employability skills—primarily in communication and technical articulation.
> - The **National Employability Study by Aspiring Minds / SHL** reports that only about **20%** of engineers are ready for software roles directly, with spoken English being a top reason for rejection.
> - Furthermore, placement observations show that over **65%** of rejections in first-round interviews occur due to nervous communication delivery rather than a lack of basic subject knowledge.
>
> Our project directly solves these problems."

---

## Slide 3: Our Proposed Solution

**Slide Title:** *Our Proposed Solution*  
**Key Visual:** 6 Clean Feature Cards showing the core capabilities.  
**Target Duration:** 50–60 Seconds  

### 🎙️ What You Should Say:

> "Our proposed solution is an automated, accessible, and private AI mock interview system. It gives every student a 24/7 personal interview coach at zero cost.
>
> Here are the six main features of our system:
>
> 1. **AI-Generated Questions:** Google Gemini generates dynamic, role-tailored questions for Technical, HR, and Behavioral rounds, matching the student's chosen difficulty level.
> 2. **Camera-Based Mock Interviews:** The in-browser camera preview simulates a real corporate video call, encouraging professional posture and eye contact.
> 3. **Local Speech Recognition:** Spoken answers are converted to text locally on the laptop using `faster-whisper`. Student audio never leaves the computer, ensuring 100% privacy and zero cloud fees.
> 4. **AI-Based Answer Evaluation:** Gemini evaluates every answer across four key dimensions: Relevance, Technical Accuracy, Communication Clarity, and Delivery Confidence on a 0 to 10 scale.
> 5. **Communication Analysis:** The system automatically calculates speaking speed in Words Per Minute and counts nervous filler words.
> 6. **Personalized Feedback Reports:** Immediately after the interview, the student receives a detailed report showing strengths, weaknesses, and clear tips to improve."

---

## Slide 4: How Our System Works

**Slide Title:** *How Our System Works*  
**Key Visual:** 7-Step sequential user journey flow diagram.  
**Target Duration:** 60–70 Seconds  

### 🎙️ What You Should Say:

> *(Point to the seven steps on the slide as you speak)*
>
> "This slide illustrates the complete, step-by-step user journey in our system:
>
> - **In Step 1:** The student selects their interview type—Technical or HR—chooses their target job role, like Full Stack Developer or Data Analyst, and picks a difficulty level. They can also upload their resume PDF for skill matching.
> - **In Step 2:** Google Gemini AI reads these parameters and generates customized interview questions targeting the candidate's exact role and skill gaps.
> - **In Step 3:** The candidate enters the live interview room. The webcam and microphone turn on, creating a realistic interview environment.
> - **In Step 4:** The student clicks record and speaks their answer. As soon as they stop, `faster-whisper` transcribes the voice into clean text in under 3 seconds.
> - **In Step 5:** The text answer is evaluated by Google Gemini against our four-pillar rubric, checking technical depth and correctness.
> - **In Step 6:** The communication engine measures speaking speed in Words Per Minute, counts filler words, and checks camera engagement.
> - **Finally, in Step 7:** The student receives an instant performance report with detailed advice, and all data is permanently saved in our PostgreSQL database for future review.
>
> The entire evaluation pipeline takes under 3.5 seconds, providing an effortless practice experience."

---

## Slide 5: Key Features & Technology

**Slide Title:** *Key Features & Technology*  
**Key Visual:** 6 Technology Cards explaining Frontend, Backend, Database, Speech, AI, and Vision.  
**Target Duration:** 50–60 Seconds  

### 🎙️ What You Should Say:

> "Every technology listed on this slide is actively implemented and verified in our project codebase:
>
> - **React 19 on Frontend:** We used the latest React 19 with Vite to build a fast, single-page application. Students can seamlessly navigate between setup, the live interview, and the analytics dashboard without page reloads.
> - **FastAPI on Backend:** We chose FastAPI in Python for its high performance, automatic API documentation, and strict data validation using Pydantic.
> - **PostgreSQL Database:** All sessions, questions, transcripts, and evaluation metrics are permanently stored in a relational PostgreSQL database with Alembic migrations to ensure data safety.
> - **faster-whisper for Speech-to-Text:** We run the OpenAI Whisper base model locally on the laptop CPU using 8-bit quantization. This gives sub-3-second transcription speed without sending voice data to any external server.
> - **Google Gemini AI:** We utilize the official `google-genai` SDK with `gemini-3.5-flash-lite` for role-adaptive questions and structured answer scoring.
> - **Browser-Based Camera Analysis:** Using lightweight HTML5 canvas frame differencing, the system checks eye contact, head stability, and posture in the browser without sending heavy video over the internet.
>
> This architecture is modern, modular, and 100% functional."

---

## Slide 6: Working Application Demo

**Slide Title:** *Working Application Demo*  
**Key Visual:** 4 Authentic High-Resolution Screenshots of the actual working system.  
**Target Duration:** 60–75 Seconds  

### 🎙️ What You Should Say:

> *(Point to each of the four screenshots on the slide)*
>
> "Here are actual screenshots captured directly from our running project and database:
>
> - **Top-Left (Screen 1):** This is the **Interview Setup screen**. Students choose their job role, difficulty tier, and question count. When a resume PDF is uploaded, our `pypdf` parser automatically extracts technical skills and matches them against job requirements.
> - **Top-Right (Screen 2):** This is the **Live Mock Interview screen**. On the left, you can see the active interview question with STAR-technique answering tips. On the right is the live webcam preview with active microphone controls.
> - **Bottom-Left (Screen 3):** This is the **Detailed Performance Report**. Notice the real evaluation scores: an overall score of **8.9 out of 10**, an ideal speaking pace of **140 Words Per Minute**, a low filler density of **1.8%**, and visual indicators showing **84% camera gaze** and **90% posture alignment**.
> - **Bottom-Right (Screen 4):** This is the **Candidate Dashboard**. It tracks practice hours, average scores across past sessions, and displays a chronological trendline so students can see their skills improve over time."

---

## Slide 7: Results, Benefits & Future Scope

**Slide Title:** *Results, Benefits & Future Scope*  
**Key Visual:** 3 Clear Vertical Columns: Actual Results, Practical Benefits, and Future Scope.  
**Target Duration:** 55–65 Seconds  

### 🎙️ What You Should Say:

> "This slide summarizes our verified results, practical benefits, and future engineering roadmap:
>
> **First, Actual Results:**
> In our verified test runs, our system achieved an overall score of **8.9 out of 10** for technical answers. The speaking pace was measured at **140 Words Per Minute**, which fits perfectly in the standard conversational range of 120 to 160 WPM. The filler word rate was low at **1.8%**, and camera engagement was **84%**. The AI accurately identified technical strengths, such as explaining database B-Tree index lookups, while suggesting improvements on write overhead.
>
> **Second, Practical Benefits:**
> Students can practice unlimited mock interviews anytime at home. They receive immediate, structured feedback to correct technical gaps and speaking habits before real campus drives. Most importantly, it builds genuine speaking confidence at zero financial cost.
>
> **Third, Future Scope & Limitations:**
> In future updates, we plan to:
> 1. Integrate the **Gemini Live Audio API** for real-time voice conversations and live interviewer interruptions.
> 2. Embed an in-browser **Monaco code editor** for live coding interviews.
> 3. Build a **College Placement Portal** where placement coordinators can assign interview batches to students.
>
> To be completely honest about current limitations: our camera metrics measure observable physical delivery patterns rather than internal psychological emotions, and the current workflow takes one answer per question."

---

## Slide 8: Conclusion & Thank You

**Slide Title:** *Conclusion & Thank You*  
**Key Visual:** 3 Takeaway Cards, Team Names Banner, College Affiliation, and Q&A prompt.  
**Target Duration:** 45–55 Seconds  

### 🎙️ What You Should Say:

> "To conclude our presentation:
>
> Our AI Interview Preparation & Evaluation System is a fully working, verified multi-modal platform. It combines modern web engineering, Google Gemini AI, and local speech recognition to solve a genuine problem faced by thousands of college students every year.
>
> It protects student data privacy, requires zero paid cloud subscriptions, and transforms interview anxiety into corporate placement readiness.
>
> On behalf of our team members—**Rajan Kumar Prajapati**, **Dhruv Maurya**, **Saloni**, and **Harsh Gupta**—we express our heartfelt gratitude to our project guide, our respected Head of Department, and the faculty members of **Bansal Institute of Engineering & Technology, Lucknow** for their guidance and encouragement.
>
> Thank you very much for your time and attention. We are now open for your questions and would love to answer them!"

---

## 🎯 Top 8 Viva & Defense Questions (With Confident Answers)

Prepare these questions before your presentation. External examiners and teachers frequently ask them:

### Q1: Why did you run speech recognition locally instead of using Google Cloud Speech API?
> **Answer:**  
> *"We chose `faster-whisper` locally for two reasons: **Cost and Privacy**. Cloud speech APIs charge money per minute of audio, which creates an ongoing cost for students. By running `faster-whisper` on the CPU with 8-bit quantization, transcription runs completely free in under 3 seconds. In addition, student audio stays strictly on the local computer and is never sent to third-party cloud servers, ensuring 100% student privacy."*

### Q2: How does the camera analysis work without an expensive server GPU?
> **Answer:**  
> *"Video processing runs entirely on the client's laptop browser using the HTML5 Canvas API. The browser samples small video frames at 2.5 frames per second and uses pixel differencing to track upper-body stability and camera eye engagement. Only small statistical numbers—like 84% eye contact—are sent to the backend. This means zero GPU load on the server and zero video bandwidth consumption."*

### Q3: How do you ensure the AI grades answers fairly and does not give random scores?
> **Answer:**  
> *"We use structured prompt engineering backed by strict Pydantic schemas. Gemini is instructed to evaluate four specific criteria: Relevance, Technical Accuracy, Communication Clarity, and Confidence, scoring each from 0 to 10. The AI is required to cite specific technical facts from the student's transcript to justify the score, and must provide concrete improvement advice."*

### Q4: How is candidate progress tracked over multiple interviews?
> **Answer:**  
> *"We use a PostgreSQL database. Every completed interview session is saved in an atomic database transaction across our `interviews`, `interview_questions`, and `communication_metrics` tables. Our candidate dashboard runs SQL queries across past sessions to show average scores, total questions answered, and chronological score trendlines."*

### Q5: How does the system extract skills from a candidate's resume?
> **Answer:**  
> *"We use the `pypdf` library to extract raw text from uploaded PDF resumes in memory. Our skill extraction service searches for over 60 industry-standard technical keywords (such as Python, React, Docker, PostgreSQL) and compares them against the job description to find matched competencies and detect missing skill gaps."*

### Q6: What happens if a student speaks too fast or uses too many filler words?
> **Answer:**  
> *"Our communication engine measures speaking pace in Words Per Minute by dividing word count by speaking duration. A healthy conversational rate is 120 to 160 WPM. If the student speaks above 170 WPM or uses words like 'um', 'uh', and 'basically' repeatedly, the report alerts them with exact counts and offers advice on pacing and structured pauses."*

### Q7: Why do you call camera metrics 'Observable Delivery Indicators' instead of confidence?
> **Answer:**  
> *"Because computer vision can only observe physical behaviors like eye direction, head stability, and posture. It cannot read internal human thoughts or emotions. Calling them 'Observable Delivery Indicators' with a clear student disclaimer is scientifically honest, ethical, and follows AI safety best practices."*

### Q8: What was each team member's role in this project?
> **Answer:**  
> - **Rajan Kumar Prajapati:** Backend API architecture, FastAPI integration, Google Gemini prompt pipelines, and database modeling.  
> - **Dhruv Maurya:** Speech-to-text pipeline with faster-whisper, audio recording, and communication pace analytics.  
> - **Saloni:** Frontend UI development in React 19, responsive layout, and candidate performance dashboard.  
> - **Harsh Gupta:** Browser-based camera analysis, resume PDF parsing, and end-to-end system testing.  
