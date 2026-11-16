# Project Overview: AI Interview Preparation & Evaluation System

## Executive Summary
The **AI Interview Preparation & Evaluation System** is an end-to-end web application that prepares college students and job seekers for placement interviews. It blends generative artificial intelligence, local speech recognition, computer vision indicators, and relational database persistence into a unified platform.

---

## Target Audience & Problem Statement
Campus placement interviews and technical job screenings are high-stress milestones. Students frequently lack:
- Objective, immediate feedback on technical accuracy.
- Realistic simulations incorporating real-time speech and camera engagement.
- Awareness of communication habits (e.g. speaking too rapidly or using excessive filler words).
- Targeted practice tailored to their specific resume and target job descriptions.

This application provides an automated, on-demand interview coach that simulates live interviews, scores candidate performance transparently, tracks improvement trends, and generates structured action plans.

---

## Core Capabilities
1. **Interactive Interview Simulator**:
   - WebRTC live camera preview.
   - Microphone recording with local `faster-whisper` transcription.
   - Question stepper with real-time audio duration tracking.
2. **Multi-Mode AI Question Generation**:
   - Technical, HR, and Behavioral question categories.
   - Easy, Intermediate, and Advanced difficulty tiers.
   - Personalization via resume skill extraction and job description matching.
3. **Multi-Dimensional AI Evaluation**:
   - Relevance, Technical Accuracy, Communication Clarity, and Confidence (0–10 score).
   - Concrete strengths and weaknesses per response.
4. **Communication & Delivery Analytics**:
   - Words Per Minute (WPM) calculation.
   - Filler word frequency and percentage density.
5. **Progress Tracking**:
   - PostgreSQL persistence of all attempts.
   - Performance Dashboard with score trends, competency averages, and session drilldowns.
