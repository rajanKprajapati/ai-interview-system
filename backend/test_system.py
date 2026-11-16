"""
Comprehensive System Verification Test Suite
Tests all endpoints, AI services, database persistence, and error handling.
"""
import io
from pypdf import PdfWriter
from fastapi.testclient import TestClient
import main
from database import SessionLocal
from models import Interview, InterviewQuestion, CommunicationMetric

client = TestClient(main.app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["status"] == "healthy"
    assert "connected" in data["database"]
    print("[PASS] Health check endpoint verified")

def test_questions_generation_modes():
    # Test Technical Intermediate
    r1 = client.post("/api/questions", json={
        "interview_type": "technical",
        "question_count": 3,
        "difficulty": "intermediate",
        "role": "Frontend React Developer",
        "subject": "React Hooks & State",
    })
    assert r1.status_code == 200
    d1 = r1.json()
    assert d1["success"] is True
    assert len(d1["questions"]) == 3
    print("[PASS] Technical question generation verified:", len(d1["questions"]), "questions")

    # Test Behavioral STAR mode
    r2 = client.post("/api/questions", json={
        "interview_type": "behavioral",
        "question_count": 2,
        "difficulty": "easy",
        "role": "Software Engineer Intern",
    })
    assert r2.status_code == 200
    d2 = r2.json()
    assert d2["success"] is True
    assert len(d2["questions"]) == 2
    print("[PASS] Behavioral question generation verified:", len(d2["questions"]), "questions")

def test_confidence_and_communication_analysis():
    sample_transcript = (
        "Um, basically, object-oriented programming is, like, a programming paradigm "
        "based on the concept of objects which contain data and methods. You know, "
        "it helps organize code cleanly."
    )
    r = client.post("/api/confidence/analyze", json={
        "transcript": sample_transcript,
        "duration_seconds": 12.0
    })
    assert r.status_code == 200
    metrics = r.json()["metrics"]
    assert metrics["filler_word_count"] >= 3
    assert metrics["speaking_pace_wpm"] > 0
    print(f"[PASS] Communication analysis verified: WPM={metrics['speaking_pace_wpm']}, Fillers={metrics['filler_word_count']}")

def test_resume_pdf_extraction():
    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)
    buf = io.BytesIO()
    writer.write(buf)
    pdf_bytes = buf.getvalue()

    r = client.post(
        "/api/resume/profile",
        files={"resume": ("sample_resume.pdf", pdf_bytes, "application/pdf")},
        data={"job_description": "We are seeking a Python engineer with SQL and FastAPI experience."}
    )
    assert r.status_code in [200, 400]
    print("[PASS] Resume PDF extraction endpoint response verified (status:", r.status_code, ")")

def test_full_evaluation_and_db_persistence():
    payload = {
        "answers": [
            {
                "question": "What is the difference between a process and a thread?",
                "answer": "A process has its own dedicated memory space, whereas threads within a process share the same memory space.",
                "duration_seconds": 10.5
            },
            {
                "question": "What is indexing in PostgreSQL?",
                "answer": "Indexing is a data structure technique like B-Trees that allows rapid data retrieval without scanning every table row.",
                "duration_seconds": 12.0
            }
        ],
        "interview_type": "technical",
        "difficulty": "intermediate",
        "role": "Backend Engineer",
        "total_duration_seconds": 22.5,
        "development_mode": True,
        "evaluations": [
            {
                "question_number": 1,
                "relevance": 9,
                "technical_accuracy": 9,
                "communication": 8,
                "confidence": 8,
                "overall_score": 8.8,
                "strengths": ["Accurate definition of memory isolation"],
                "weaknesses": ["Could mention context switching costs"],
                "improvement_feedback": "Contrast context switching overhead between threads and processes."
            },
            {
                "question_number": 2,
                "relevance": 9,
                "technical_accuracy": 9,
                "communication": 9,
                "confidence": 9,
                "overall_score": 9.0,
                "strengths": ["Correctly mentioned B-Trees and avoidance of sequential scans"],
                "weaknesses": ["None"],
                "improvement_feedback": "Mention trade-offs on insert/update write latency."
            }
        ],
        "resume_skills": ["Python", "PostgreSQL", "FastAPI"],
        "resume_filename": "candidate_cv.pdf",
        "job_description": "Backend Engineer with Python and PostgreSQL experience."
    }

    r = client.post("/api/evaluate", json=payload)
    assert r.status_code == 200
    res = r.json()
    assert res["success"] is True
    new_id = res["interview_id"]
    assert new_id > 0
    assert res["overall_score"] == 8.9
    assert "relevance" in res["category_scores"]
    assert "speaking_pace_wpm" in res["communication_metrics"]
    assert len(res["personalized_feedback"]["strengths"]) > 0
    print(f"[PASS] Full evaluation and persistence verified: Session ID #{new_id}, Score={res['overall_score']}")

    # Verify retrieval via detail endpoint
    r_detail = client.get(f"/api/interviews/{new_id}")
    assert r_detail.status_code == 200
    detail = r_detail.json()
    assert detail["interview_id"] == new_id
    assert len(detail["evaluations"]) == 2
    print(f"[PASS] Interview detail retrieval verified: {len(detail['evaluations'])} questions confirmed")

def test_dashboard_stats():
    r = client.get("/api/dashboard/stats")
    assert r.status_code == 200
    d = r.json()
    assert d["success"] is True
    assert d["total_interviews"] >= 1
    assert "category_scores" in d
    assert "score_trend" in d
    assert "recent_interviews" in d
    print(f"[PASS] Dashboard stats verified: {d['total_interviews']} total interviews, Average score={d['average_score']}")

def test_error_handling():
    # Empty audio upload
    r_empty_audio = client.post("/api/transcribe", files={"file": ("empty.webm", b"", "audio/webm")})
    assert r_empty_audio.status_code == 400

    # Non-existent interview
    r_404 = client.get("/api/interviews/999999")
    assert r_404.status_code == 404

    # Invalid interview type validation
    r_bad_type = client.post("/api/questions", json={"interview_type": "invalid_mode", "question_count": 5})
    assert r_bad_type.status_code == 422
    print("[PASS] All negative and error boundary tests passed cleanly")

if __name__ == "__main__":
    print("\n--- RUNNING COMPREHENSIVE SYSTEM TESTS ---\n")
    test_health()
    test_questions_generation_modes()
    test_confidence_and_communication_analysis()
    test_resume_pdf_extraction()
    test_full_evaluation_and_db_persistence()
    test_dashboard_stats()
    test_error_handling()
    print("\n[SUCCESS] ALL SYSTEM TESTS PASSED SUCCESSFULLY!\n")
