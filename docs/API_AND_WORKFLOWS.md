# API Endpoints & Operational Workflows

The backend exposes RESTful HTTP endpoints with automatic JSON request validation via Pydantic.

---

## 1. Endpoints Reference

### Health & Status
- **`GET /api/health`**
  - **Response**: `{ "success": true, "status": "healthy", "database": "connected" }`

### Question Generation
- **`POST /api/questions`**
  - **Request**:
    ```json
    {
      "interview_type": "technical",
      "question_count": 5,
      "difficulty": "intermediate",
      "role": "Full Stack Engineer",
      "subject": "React & Node.js",
      "resume_skills": ["JavaScript", "React", "PostgreSQL"],
      "skill_gaps": ["Docker"],
      "job_description": "Seeking a developer skilled in React and cloud architecture."
    }
    ```
  - **Response**:
    ```json
    {
      "success": true,
      "interview_type": "technical",
      "difficulty": "intermediate",
      "role": "Full Stack Engineer",
      "question_count": 5,
      "questions": [
        "Explain the virtual DOM diffing algorithm in React...",
        "..."
      ]
    }
    ```

### Speech-to-Text Transcription
- **`POST /api/transcribe`**
  - **Content-Type**: `multipart/form-data`
  - **Payload**: `file` (WebM audio file)
  - **Response**:
    ```json
    {
      "success": true,
      "transcript": "Object-oriented programming is structured around objects...",
      "duration_seconds": 14.8
    }
    ```

### Answer Evaluation & Persistence
- **`POST /api/evaluate`**
  - **Request**:
    ```json
    {
      "answers": [
        {
          "question": "What is an index in PostgreSQL?",
          "answer": "An index accelerates lookup queries by building a B-Tree structure...",
          "duration_seconds": 15.2
        }
      ],
      "interview_type": "technical",
      "difficulty": "intermediate",
      "role": "Backend Developer",
      "development_mode": false
    }
    ```
  - **Response**:
    ```json
    {
      "success": true,
      "interview_id": 6,
      "overall_score": 8.5,
      "category_scores": {
        "relevance": 9.0,
        "technical_accuracy": 8.5,
        "communication": 8.0,
        "confidence": 8.5,
        "overall_score": 8.5
      },
      "evaluations": [
        {
          "question_number": 1,
          "relevance": 9,
          "technical_accuracy": 8.5,
          "communication": 8,
          "confidence": 8.5,
          "overall_score": 8.5,
          "strengths": ["Accurately identified B-Tree indexing mechanism"],
          "weaknesses": ["Could mention write overhead during insert/update"],
          "improvement_feedback": "Explain trade-offs on insert write latency."
        }
      ],
      "communication_metrics": {
        "word_count": 48,
        "speaking_pace_wpm": 138.2,
        "speaking_pace_label": "Typical range",
        "filler_word_count": 1,
        "filler_rate_percent": 2.1,
        "filler_label": "Moderate"
      },
      "personalized_feedback": {
        "strengths": ["Good answer relevance (average 9.0/10)."],
        "weaknesses": ["No major low-scoring category was identified."],
        "recommended_practice": ["Practice explaining trade-offs concisely."]
      }
    }
    ```

### Session History
- **`GET /api/interviews`**: List historical sessions with pagination.
- **`GET /api/interviews/{id}`**: Retrieve full details, questions, transcripts, and evaluation breakdown for a session.
- **`DELETE /api/interviews/{id}`**: Remove a session and its associated questions and metrics.

### Dashboard Analytics
- **`GET /api/dashboard/stats`**
  - Aggregates total completed sessions, overall average score, competency breakdowns, score trends, and recent session logs.

### Resume & Job Description Profiling
- **`POST /api/resume/profile`**
  - **Content-Type**: `multipart/form-data`
  - **Payload**: `resume` (PDF) and `job_description` (string).
  - Returns extracted resume skills, required job skills, matched skills, and detected skill gaps.
