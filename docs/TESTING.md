# Testing & Quality Assurance Guide

Comprehensive verification strategy covering functional, integration, regression, and error-boundary testing.

---

## 1. Automated Test Suite (`backend/test_system.py`)

The automated suite tests the end-to-end backend functionality using FastAPI's `TestClient`.

### Running the Suite
```powershell
python backend/test_system.py
```

### Covered Test Cases
1. **Health & Connectivity**:
   - `test_health()`: Asserts that `/api/health` returns `200 OK` and reports active PostgreSQL database connection.
2. **AI Question Generation Modes**:
   - `test_questions_generation_modes()`:
     - Technical mode with specific role ("Frontend React Developer") and subject ("React Hooks").
     - Behavioral STAR mode with difficulty ("easy").
     - Asserts correct question counts, absence of numbering artifacts, and structured response schema.
3. **Communication Analysis & Heuristics**:
   - `test_confidence_and_communication_analysis()`:
     - Verifies WPM calculation based on word count and recording duration.
     - Tests regex detection of multi-word and single-word filler terms (*um*, *basically*, *like*, *you know*).
4. **Resume PDF Parsing**:
   - `test_resume_pdf_extraction()`:
     - Tests `/api/resume/profile` endpoint handling of PDF uploads.
5. **Full Evaluation & Database Persistence**:
   - `test_full_evaluation_and_db_persistence()`:
     - Simulates multi-question interview submission.
     - Verifies atomic insertion into `interviews`, `interview_questions`, and `communication_metrics`.
     - Validates category scoring (Relevance, Technical, Communication, Confidence).
     - Confirms synthesized personalized strengths and practice topics.
     - Asserts retrieval via `GET /api/interviews/{id}`.
6. **Performance Dashboard Analytics**:
   - `test_dashboard_stats()`:
     - Computes candidate-wide KPIs: total sessions, average score, competency breakdowns, and chronological score trend data points.
7. **Negative Boundaries & Error Handling**:
   - `test_error_handling()`:
     - Submitting empty audio file to `/api/transcribe` -> `400 Bad Request`.
     - Requesting non-existent session `/api/interviews/999999` -> `404 Not Found`.
     - Requesting invalid interview mode -> `422 Unprocessable Entity`.

---

## 2. Frontend Build Verification

To verify that the frontend bundles without React syntax errors or broken imports:
```powershell
cd frontend
npm run build
```
Expected output:
```
✓ 22 modules transformed.
dist/index.html                   0.45 kB
dist/assets/index-....css        23.28 kB
dist/assets/index-....js        269.85 kB
✓ built in <500ms
```

---

## 3. Manual Testing Checklist

| Test Item | Steps | Expected Result | Verified |
| :--- | :--- | :--- | :---: |
| **Microphone Permission** | Click "Start Voice Answer" without mic enabled | Prompts user to enable media permissions | [x] |
| **Webcam Stream** | Click "Enable Camera & Mic" | Shows mirrored live video preview | [x] |
| **Live Transcription** | Speak for 10 seconds and stop | Real-time transcript appears in textarea | [x] |
| **Question Progression** | Click "Submit & Next Question" | Moves to next question; progress bar updates | [x] |
| **Real Evaluation** | Complete all questions and click "Finish" | Computes genuine scores via Gemini; saves to PostgreSQL | [x] |
| **Dashboard KPIs** | Open "Dashboard" tab | Shows updated total sessions and score trend | [x] |
| **History Drilldown** | Click "View Report" on past session | Renders full question-by-question breakdown | [x] |
| **Session Deletion** | Click trash icon on history item | Cascades deletion from database cleanly | [x] |
| **Resume Extraction** | Upload PDF on setup screen | Displays detected skills badges | [x] |
| **Responsive UI** | Resize viewport to mobile screen | Navigation stacks, columns collapse to 1-column | [x] |
