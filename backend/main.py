from pathlib import Path
import os
import tempfile
import json
from typing import Optional, List
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import (
    Interview,
    InterviewQuestion,
    CommunicationMetric,
    ResumeRecord,
    JobDescriptionRecord,
)
from ai_question_generator import generate_questions
from ai_evaluator import evaluate_answers
from speech_to_text import transcribe_audio
from phase7_11_services import (
    analyze_transcript,
    make_personalized_feedback,
)

from phase7_11_router import router as phase7_11_router
from phase9_10_router import router as phase9_10_router


app = FastAPI(
    title="AI Interview Preparation & Evaluation System",
    description="Full-stack AI Mock Interview System with speech-to-text, real-time evaluation, communication metrics, visual behavioral telemetry, and performance analytics.",
    version="2.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(phase7_11_router)
app.include_router(phase9_10_router)


# ---------------------------------------------------------
# Schemas
# ---------------------------------------------------------

class QuestionRequest(BaseModel):
    interview_type: str = Field(default="technical", pattern="^(technical|hr|behavioral)$")
    question_count: int = Field(default=5, ge=1, le=10)
    difficulty: str = Field(default="intermediate", pattern="^(easy|intermediate|advanced)$")
    role: Optional[str] = None
    subject: Optional[str] = None
    resume_skills: Optional[List[str]] = None
    skill_gaps: Optional[List[str]] = None
    job_description: Optional[str] = None


class AnswerItem(BaseModel):
    question: str = Field(min_length=1)
    answer: str = Field(min_length=1)
    duration_seconds: Optional[float] = None
    speaking_pace_wpm: Optional[float] = None
    filler_word_count: Optional[int] = None


class EvaluationRequest(BaseModel):
    answers: List[AnswerItem] = Field(min_length=1)
    interview_type: str = "technical"
    difficulty: str = "intermediate"
    role: Optional[str] = None
    total_duration_seconds: Optional[float] = None
    development_mode: bool = False
    evaluations: Optional[List[dict]] = None
    resume_skills: Optional[List[str]] = None
    resume_filename: Optional[str] = None
    job_description: Optional[str] = None
    visual_metrics: Optional[dict] = None


# ---------------------------------------------------------
# Core Endpoints
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "success": True,
        "message": "AI Interview System Backend is running",
        "version": "2.1.0"
    }


@app.get("/api/health")
def health(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(func.now())
    except Exception as exc:
        db_status = f"unavailable: {str(exc)}"

    return {
        "success": True,
        "status": "healthy",
        "database": db_status
    }


@app.post("/api/questions")
def get_questions(request: QuestionRequest):
    try:
        questions = generate_questions(
            interview_type=request.interview_type,
            question_count=request.question_count,
            difficulty=request.difficulty,
            role=request.role,
            subject=request.subject,
            resume_skills=request.resume_skills,
            skill_gaps=request.skill_gaps,
            job_description=request.job_description,
        )

        if not questions:
            raise HTTPException(
                status_code=502,
                detail="AI provider returned no questions."
            )

        return {
            "success": True,
            "interview_type": request.interview_type,
            "difficulty": request.difficulty,
            "role": request.role or "Software Engineer",
            "question_count": len(questions),
            "questions": questions
        }

    except HTTPException:
        raise
    except Exception as e:
        print("QUESTION GENERATION ERROR:", repr(e))
        raise HTTPException(
            status_code=502,
            detail=f"Question generation failed: {str(e)}"
        )


@app.post("/api/transcribe")
async def transcribe(file: UploadFile = File(...)):
    temp_path = None
    try:
        suffix = os.path.splitext(file.filename or "")[1] or ".webm"
        audio_data = await file.read()

        if not audio_data:
            raise HTTPException(
                status_code=400,
                detail="Uploaded audio file is empty."
            )

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(audio_data)
            temp_path = temp_file.name

        result = transcribe_audio(temp_path, return_metadata=True)
        if isinstance(result, str):
            transcript = result
            duration_seconds = None
        else:
            transcript = result.get("transcript", "")
            duration_seconds = result.get("duration_seconds")

        return {
            "success": True,
            "transcript": transcript,
            "duration_seconds": duration_seconds,
        }

    except HTTPException:
        raise
    except Exception as e:
        print("TRANSCRIPTION ERROR:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=f"Speech-to-text failed: {str(e)}"
        )
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


@app.post("/api/visual/telemetry")
def process_visual_telemetry(payload: dict):
    return {
        "success": True,
        "recorded": True,
        "telemetry": payload,
    }


@app.post("/api/evaluate")
def evaluate(request: EvaluationRequest, db: Session = Depends(get_db)):
    try:
        raw_answers = [
            {"question": item.question, "answer": item.answer}
            for item in request.answers
        ]

        # 1. Evaluation (Dev mode or Gemini AI)
        if request.development_mode:
            if not request.evaluations or len(request.evaluations) != len(raw_answers):
                raise HTTPException(
                    status_code=400,
                    detail=f"Development mode requires {len(raw_answers)} sample evaluations."
                )
            evaluations = request.evaluations
        else:
            evaluations = evaluate_answers(raw_answers)

        # 2. Category & Overall Scoring
        relevance_scores = [float(e.get("relevance", 7.0)) for e in evaluations]
        tech_scores = [float(e.get("technical_accuracy", 7.0)) for e in evaluations]
        comm_scores = [float(e.get("communication", 7.0)) for e in evaluations]
        conf_scores = [float(e.get("confidence", 7.0)) for e in evaluations]
        overall_scores = [float(e.get("overall_score", 7.0)) for e in evaluations]

        avg_relevance = round(sum(relevance_scores) / len(relevance_scores), 2)
        avg_tech = round(sum(tech_scores) / len(tech_scores), 2)
        avg_comm = round(sum(comm_scores) / len(comm_scores), 2)
        avg_conf = round(sum(conf_scores) / len(conf_scores), 2)
        overall_score = round(sum(overall_scores) / len(overall_scores), 2)

        category_scores = {
            "relevance": avg_relevance,
            "technical_accuracy": avg_tech,
            "communication": avg_comm,
            "confidence": avg_conf,
            "overall_score": overall_score,
        }

        # 3. Verbal Communication Analysis
        total_words = 0
        total_duration = 0.0
        total_fillers = 0
        per_question_metrics = []

        for item in request.answers:
            metric = analyze_transcript(item.answer, item.duration_seconds)
            total_words += metric["word_count"]
            if item.duration_seconds:
                total_duration += item.duration_seconds
            total_fillers += metric["filler_word_count"]
            per_question_metrics.append(metric)

        session_duration = request.total_duration_seconds or (total_duration if total_duration > 0 else None)
        session_pace = None
        session_pace_label = "Not measured"
        if session_duration and session_duration > 0:
            session_pace = round(total_words / (session_duration / 60), 1)
            if session_pace < 100:
                session_pace_label = "Slow"
            elif session_pace <= 160:
                session_pace_label = "Typical range"
            else:
                session_pace_label = "Fast"

        filler_rate = round((total_fillers / max(total_words, 1)) * 100, 1)
        filler_label = "Low" if filler_rate <= 1 else ("Moderate" if filler_rate <= 3 else "Frequent")

        # 4. Visual Delivery Telemetry
        visual_data = request.visual_metrics or {}
        gaze_metric = visual_data.get("camera_gaze_metric")
        posture_score = None
        if isinstance(visual_data.get("posture"), dict):
            posture_score = visual_data.get("posture", {}).get("upright_percent")
        face_detected = visual_data.get("face_present", True) if visual_data else True

        aggregated_metrics = {
            "word_count": total_words,
            "duration_seconds": round(session_duration, 1) if session_duration else None,
            "speaking_pace_wpm": session_pace,
            "speaking_pace_label": session_pace_label,
            "filler_word_count": total_fillers,
            "filler_rate_percent": filler_rate,
            "filler_label": filler_label,
            "face_present": face_detected,
            "camera_gaze_metric": gaze_metric,
            "posture_metric": posture_score,
            "visual_indicators": visual_data if visual_data else None,
            "measurement_source": "audio_and_visual_pipeline" if visual_data else "audio_transcript_pipeline",
            "interpretation": (
                "Observable communication & delivery indicators: speaking pace, filler density, "
                "eye-contact estimation, and posture framing. These metrics reflect delivery patterns "
                "and do not assess psychological confidence."
            ),
        }

        # 5. Personalized Feedback Synthesis
        feedback = make_personalized_feedback(evaluations, aggregated_metrics)

        # 6. Database Persistence (Atomic Transaction)
        interview = Interview(
            interview_type=request.interview_type,
            question_count=len(raw_answers),
            overall_score=overall_score,
        )
        db.add(interview)
        db.flush()

        # Save questions
        for index, (item, eval_data, metric_data) in enumerate(
            zip(request.answers, evaluations, per_question_metrics),
            start=1
        ):
            q_record = InterviewQuestion(
                interview_id=interview.id,
                question_number=index,
                question=item.question,
                answer=item.answer,
                relevance=eval_data.get("relevance"),
                technical_accuracy=eval_data.get("technical_accuracy"),
                communication=eval_data.get("communication"),
                confidence=eval_data.get("confidence"),
                overall_score=eval_data.get("overall_score"),
                strengths=json.dumps(eval_data.get("strengths", [])),
                weaknesses=json.dumps(eval_data.get("weaknesses", [])),
                improvement_feedback=eval_data.get("improvement_feedback", ""),
            )
            db.add(q_record)
            db.flush()

            # Save per-question communication metric
            q_metric = CommunicationMetric(
                interview_id=interview.id,
                interview_question_id=q_record.id,
                speaking_pace_wpm=metric_data.get("speaking_pace_wpm"),
                filler_word_count=metric_data.get("filler_word_count"),
                filler_word_rate=metric_data.get("filler_rate_percent"),
                audio_duration_seconds=metric_data.get("duration_seconds"),
                face_present=face_detected,
                camera_gaze_metric=float(gaze_metric) if gaze_metric is not None else None,
                posture_metric=float(posture_score) if posture_score is not None else None,
                measurement_source="faster_whisper_and_canvas_vision" if visual_data else "faster_whisper_and_regex",
            )
            db.add(q_metric)

        # Save session-level communication metric
        session_metric = CommunicationMetric(
            interview_id=interview.id,
            interview_question_id=None,
            speaking_pace_wpm=session_pace,
            filler_word_count=total_fillers,
            filler_word_rate=filler_rate,
            audio_duration_seconds=session_duration,
            face_present=face_detected,
            camera_gaze_metric=float(gaze_metric) if gaze_metric is not None else None,
            posture_metric=float(posture_score) if posture_score is not None else None,
            measurement_source="audio_and_canvas_vision_aggregate" if visual_data else "session_aggregate",
        )
        db.add(session_metric)

        # Optional resume persistence
        if request.resume_filename or request.resume_skills:
            resume_record = ResumeRecord(
                interview_id=interview.id,
                original_filename=request.resume_filename or "uploaded_resume.pdf",
                extracted_skills=json.dumps(request.resume_skills or []),
            )
            db.add(resume_record)

        # Optional job description persistence
        if request.job_description and request.job_description.strip():
            jd_record = JobDescriptionRecord(
                interview_id=interview.id,
                title=request.role or "Software Engineer",
                description_text=request.job_description.strip(),
            )
            db.add(jd_record)

        db.commit()
        db.refresh(interview)

        return {
            "success": True,
            "interview_id": interview.id,
            "interview_type": interview.interview_type,
            "overall_score": overall_score,
            "category_scores": category_scores,
            "evaluations": evaluations,
            "communication_metrics": aggregated_metrics,
            "personalized_feedback": feedback,
            "created_at": interview.created_at.isoformat() if interview.created_at else None,
        }

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print("EVALUATION / DATABASE ERROR:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=f"Answer evaluation failed: {str(e)}"
        )


# ---------------------------------------------------------
# Interview History Endpoints
# ---------------------------------------------------------

@app.get("/api/interviews")
def list_interviews(
    limit: int = 50,
    offset: int = 0,
    interview_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Interview)
    if interview_type:
        query = query.filter(Interview.interview_type == interview_type)

    total_count = query.count()
    interviews = query.order_by(Interview.created_at.desc()).offset(offset).limit(limit).all()

    items = []
    for interview in interviews:
        items.append({
            "id": interview.id,
            "interview_type": interview.interview_type,
            "question_count": interview.question_count,
            "overall_score": interview.overall_score,
            "created_at": interview.created_at.isoformat() if interview.created_at else None,
        })

    return {
        "success": True,
        "total": total_count,
        "interviews": items,
    }


@app.get("/api/interviews/{interview_id}")
def get_interview_detail(interview_id: int, db: Session = Depends(get_db)):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found.")

    questions_data = []
    for q in sorted(interview.questions, key=lambda x: x.question_number):
        strengths = []
        weaknesses = []
        try:
            if q.strengths:
                strengths = json.loads(q.strengths)
        except Exception:
            strengths = [q.strengths]
        try:
            if q.weaknesses:
                weaknesses = json.loads(q.weaknesses)
        except Exception:
            weaknesses = [q.weaknesses]

        questions_data.append({
            "question_number": q.question_number,
            "question": q.question,
            "answer": q.answer,
            "relevance": q.relevance,
            "technical_accuracy": q.technical_accuracy,
            "communication": q.communication,
            "confidence": q.confidence,
            "overall_score": q.overall_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "improvement_feedback": q.improvement_feedback,
        })

    # Retrieve session communication metric
    session_metric = (
        db.query(CommunicationMetric)
        .filter(CommunicationMetric.interview_id == interview_id, CommunicationMetric.interview_question_id == None)
        .first()
    )

    comm_metrics_data = None
    if session_metric:
        pace = session_metric.speaking_pace_wpm
        pace_label = "Not measured"
        if pace:
            pace_label = "Slow" if pace < 100 else ("Typical range" if pace <= 160 else "Fast")

        filler_rate = session_metric.filler_word_rate or 0.0
        filler_label = "Low" if filler_rate <= 1 else ("Moderate" if filler_rate <= 3 else "Frequent")

        comm_metrics_data = {
            "duration_seconds": session_metric.audio_duration_seconds,
            "speaking_pace_wpm": pace,
            "speaking_pace_label": pace_label,
            "filler_word_count": session_metric.filler_word_count,
            "filler_rate_percent": filler_rate,
            "filler_label": filler_label,
            "face_present": session_metric.face_present,
            "camera_gaze_metric": session_metric.camera_gaze_metric,
            "posture_metric": session_metric.posture_metric,
            "measurement_source": session_metric.measurement_source,
            "interpretation": (
                "Observable communication indicators: speaking pace, filler density, and answer structure."
            ),
        }

    # Generate feedback from questions
    feedback = make_personalized_feedback(questions_data, comm_metrics_data)

    # Category averages
    rel_scores = [q["relevance"] for q in questions_data if q["relevance"] is not None]
    tech_scores = [q["technical_accuracy"] for q in questions_data if q["technical_accuracy"] is not None]
    comm_scores = [q["communication"] for q in questions_data if q["communication"] is not None]
    conf_scores = [q["confidence"] for q in questions_data if q["confidence"] is not None]

    category_scores = {
        "relevance": round(sum(rel_scores) / len(rel_scores), 2) if rel_scores else None,
        "technical_accuracy": round(sum(tech_scores) / len(tech_scores), 2) if tech_scores else None,
        "communication": round(sum(comm_scores) / len(comm_scores), 2) if comm_scores else None,
        "confidence": round(sum(conf_scores) / len(conf_scores), 2) if conf_scores else None,
        "overall_score": interview.overall_score,
    }

    return {
        "success": True,
        "interview_id": interview.id,
        "interview_type": interview.interview_type,
        "overall_score": interview.overall_score,
        "category_scores": category_scores,
        "evaluations": questions_data,
        "communication_metrics": comm_metrics_data,
        "personalized_feedback": feedback,
        "created_at": interview.created_at.isoformat() if interview.created_at else None,
    }


@app.delete("/api/interviews/{interview_id}")
def delete_interview(interview_id: int, db: Session = Depends(get_db)):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found.")

    try:
        db.delete(interview)
        db.commit()
        return {"success": True, "message": f"Interview {interview_id} deleted successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete interview: {str(e)}")


# ---------------------------------------------------------
# Performance Dashboard Analytics Endpoint
# ---------------------------------------------------------

@app.get("/api/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    interviews = db.query(Interview).order_by(Interview.created_at.desc()).all()
    total_interviews = len(interviews)

    if total_interviews == 0:
        return {
            "success": True,
            "total_interviews": 0,
            "average_score": 0.0,
            "category_scores": {
                "technical_accuracy": 0.0,
                "communication": 0.0,
                "relevance": 0.0,
                "confidence": 0.0,
            },
            "type_breakdown": {"technical": 0, "hr": 0, "behavioral": 0},
            "score_trend": [],
            "recent_interviews": [],
            "communication_summary": {
                "average_wpm": None,
                "total_questions_attempted": 0,
            }
        }

    valid_scores = [i.overall_score for i in interviews if i.overall_score is not None]
    average_score = round(sum(valid_scores) / len(valid_scores), 2) if valid_scores else 0.0

    # Type breakdown
    type_counts = {"technical": 0, "hr": 0, "behavioral": 0}
    for i in interviews:
        t = (i.interview_type or "technical").lower()
        if t in type_counts:
            type_counts[t] += 1
        else:
            type_counts[t] = 1

    # Questions metrics
    all_questions = db.query(InterviewQuestion).all()
    total_questions = len(all_questions)

    tech_scores = [q.technical_accuracy for q in all_questions if q.technical_accuracy is not None]
    comm_scores = [q.communication for q in all_questions if q.communication is not None]
    rel_scores = [q.relevance for q in all_questions if q.relevance is not None]
    conf_scores = [q.confidence for q in all_questions if q.confidence is not None]

    cat_averages = {
        "technical_accuracy": round(sum(tech_scores) / len(tech_scores), 2) if tech_scores else 0.0,
        "communication": round(sum(comm_scores) / len(comm_scores), 2) if comm_scores else 0.0,
        "relevance": round(sum(rel_scores) / len(rel_scores), 2) if rel_scores else 0.0,
        "confidence": round(sum(conf_scores) / len(conf_scores), 2) if conf_scores else 0.0,
    }

    # Chronological score trend (oldest to newest for charts)
    chronological = sorted(interviews, key=lambda x: x.created_at if x.created_at else 0)
    score_trend = [
        {
            "id": i.id,
            "type": i.interview_type,
            "score": i.overall_score or 0.0,
            "date": i.created_at.strftime("%b %d") if i.created_at else "Recent",
        }
        for i in chronological[-10:]
    ]

    # Recent 5 interviews
    recent_list = [
        {
            "id": i.id,
            "interview_type": i.interview_type,
            "question_count": i.question_count,
            "overall_score": i.overall_score or 0.0,
            "date": i.created_at.strftime("%b %d, %Y") if i.created_at else "Recently",
        }
        for i in interviews[:5]
    ]

    # Communication summary
    metrics = db.query(CommunicationMetric).filter(CommunicationMetric.speaking_pace_wpm != None).all()
    pace_values = [m.speaking_pace_wpm for m in metrics if m.speaking_pace_wpm]
    avg_pace = round(sum(pace_values) / len(pace_values), 1) if pace_values else None

    return {
        "success": True,
        "total_interviews": total_interviews,
        "average_score": average_score,
        "category_scores": cat_averages,
        "type_breakdown": type_counts,
        "score_trend": score_trend,
        "recent_interviews": recent_list,
        "communication_summary": {
            "average_wpm": avg_pace,
            "total_questions_attempted": total_questions,
        }
    }
