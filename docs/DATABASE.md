# Database Architecture & Schema Reference

The system uses **PostgreSQL** managed through **SQLAlchemy 2.0** ORM and **Alembic** migrations.

---

## 1. Entity-Relationship Diagram

```mermaid
erDiagram
    interviews ||--o{ interview_questions : "contains"
    interviews ||--o{ communication_metrics : "measures"
    interviews ||--o{ resumes : "references"
    interviews ||--o{ job_descriptions : "targets"
    interview_questions ||--o{ communication_metrics : "evaluates"

    interviews {
        int id PK
        varchar interview_type
        int question_count
        float overall_score
        timestamp created_at
    }

    interview_questions {
        int id PK
        int interview_id FK
        int question_number
        text question
        text answer
        float relevance
        float technical_accuracy
        float communication
        float confidence
        float overall_score
        text strengths
        text weaknesses
        text improvement_feedback
    }

    communication_metrics {
        int id PK
        int interview_id FK
        int interview_question_id FK
        float speaking_pace_wpm
        int filler_word_count
        float filler_word_rate
        float audio_duration_seconds
        int pause_count
        float pause_duration_seconds
        boolean face_present
        float camera_gaze_metric
        float posture_metric
        varchar measurement_source
        timestamp created_at
    }

    resumes {
        int id PK
        int interview_id FK
        varchar original_filename
        text extracted_text
        text extracted_skills
        timestamp created_at
    }

    job_descriptions {
        int id PK
        int interview_id FK
        varchar title
        varchar company_name
        text description_text
        text required_skills
        timestamp created_at
    }
```

---

## 2. Table Specifications

### `interviews`
Primary table tracking each completed or ongoing interview session.
- `id`: Auto-incrementing primary key.
- `interview_type`: `'technical'`, `'hr'`, or `'behavioral'`.
- `question_count`: Total number of questions assigned.
- `overall_score`: Aggregate mean score (0.0 to 10.0).
- `created_at`: Time of session completion.

### `interview_questions`
Stores individual question prompts, candidate transcripts, and AI-evaluated scores.
- `interview_id`: Foreign key with `ON DELETE CASCADE` to `interviews.id`.
- `strengths` & `weaknesses`: JSON-serialized string array for flexible reporting.
- `improvement_feedback`: Actionable guidance for the specific question.

### `communication_metrics`
Logs objective delivery signals computed from speech duration and regex transcript analysis.
- `speaking_pace_wpm`: Words per minute.
- `filler_word_count`: Number of detected hesitation words.
- `filler_word_rate`: Density percentage relative to total words spoken.
- `face_present`: Indicator of webcam engagement during answer.

### `resumes` & `job_descriptions`
Stores parsed metadata and skill sets extracted from user uploads.

---

## 3. Migration Strategy
All migrations reside in `backend/alembic/versions/`.
- Revision `9a664f23c784`: Initial tables (`interviews`, `interview_questions`).
- Revision `phase9_10_additive_001`: Additive migration (`communication_metrics`, `resumes`, `job_descriptions`).

To verify current database head:
```powershell
cd backend
alembic current
```
To apply pending additive migrations:
```powershell
alembic upgrade head
```
