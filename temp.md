```
                    AI INTERVIEW WEBSITE
                           │
              ┌────────────┴────────────┐
              │                         │
          Candidate                  Interview
           Profile                     Setup
              │                         │
       Resume / JD upload       Technical / HR / Behavioral
              │                         │
              └────────────┬────────────┘
                           ↓
                    QUESTION ENGINE
                           ↓
                    CAMERA INTERVIEW
                           │
                ┌──────────┴──────────┐
                ↓                     ↓
             Camera                Microphone
                │                     │
                │               Audio Recording
                │                     ↓
                │               Speech-to-Text
                │                     ↓
                └─────────────→ Candidate Answer
                                      │
                                      ↓
                                AI EVALUATION
                                      │
                 ┌────────────────────┼─────────────────┐
                 ↓                    ↓                 ↓
             Answer Quality       Communication     Confidence
                 │                    │                 │
                 └────────────────────┼─────────────────┘
                                      ↓
                              PERFORMANCE REPORT
                                      │
                         ┌────────────┴────────────┐
                         ↓                         ↓
                  Score / Weaknesses        Personalized Feedback
                         │
                         ↓
                  Performance History
```


# AI Mock Interview Platform: Requirements & Implementation Matrix

| Requirement (Your Proposal) | Implementation (What We Will Actually Build) |
| :--- | :--- |
| **AI mock interview** | Adaptive Question Engine orchestrated with an LLM |
| **Speech-to-text** | Browser audio capture (`MediaRecorder API`) → Backend stream → Whisper / STT model |
| **Answer quality** | LLM transcript evaluation against rubric (relevance, depth, STAR method) |
| **Confidence analysis** | Measurable delivery indicators (speech steadiness, pause patterns, completion rate) |
| **Communication analysis** | Deterministic metrics: Speaking rate (WPM), pause durations, filler word density, answer structure |
| **Resume-based questions** | Resume text extraction (PDF/DOCX parser) → LLM profile-targeted question generation |
| **JD-based questions** | Job description parsing → LLM role-specific competency question generation |
| **Technical mode** | Domain-specific technical prompt templates & scenario challenges |
| **HR mode** | Standard organizational fit, policy, and background prompt pipelines |
| **Behavioral mode** | Situational prompts mapped to behavioral frameworks (e.g., STAR technique) |
| **Performance tracking** | Relational/Document database schema logging sessions, transcripts, audio metadata, and trend scores |
| **Personalized feedback** | LLM post-session synthesis producing clear strengths, growth areas, and sample strong answers |
| **Camera interview** | HTML5 `getUserMedia` browser webcam preview with client-side frame processing |
| **Overall performance** | Aggregated analytics dashboard tracking progress, score distributions, and communication trends |

---

### Clarification on Assessment Methodology

> **Note on "Confidence Indicators":**  
> The system will not infer internal psychological states or make subjective claims about a candidate's confidence based on raw facial expressions. Instead, evaluations rely on quantifiable, observable proxy metrics:
>
> - **Speech Steadiness & Pace:** Words per minute (WPM) benchmarked against conversational targets (120–160 WPM).
> - **Hesitation & Fluency:** Frequency and duration of unnatural pauses and filler words (*um*, *uh*, *like*, *you know*).
> - **Answer Completeness:** Logical structure, point-to-point coherence, and conclusion clarity.
> - **Visual Engagement (Optional):** Gaze direction and head pose stability, evaluated solely as delivery indicators.
>
> Reports will explicitly label these findings as **"Observable Delivery & Confidence Indicators"** rather than definitive emotional assessments.confidence indicators rather than pretending the AI can know someone's internal confidence.
```