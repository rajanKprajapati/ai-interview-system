import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import get_db
from models import Interview, InterviewQuestion
from phase9_10_schemas import (
    CommunicationMetric,
    ResumeRecord,
    JobDescriptionRecord,
)

router = APIRouter(
    prefix="/api/phase9-10",
    tags=["Phase 9/10 - Persistent Records"],
)


# ----------------------------
# Request schemas
# ----------------------------

class CommunicationMetricCreate(BaseModel):
    interview_id: int = Field(gt=0)
    interview_question_id: Optional[int] = Field(default=None, gt=0)

    speaking_pace_wpm: Optional[float] = Field(default=None, ge=0)
    filler_word_count: Optional[int] = Field(default=None, ge=0)
    filler_word_rate: Optional[float] = Field(default=None, ge=0, le=1)
    audio_duration_seconds: Optional[float] = Field(default=None, ge=0)
    pause_count: Optional[int] = Field(default=None, ge=0)
    pause_duration_seconds: Optional[float] = Field(default=None, ge=0)

    face_present: Optional[bool] = None
    camera_gaze_metric: Optional[float] = None
    posture_metric: Optional[float] = None
    measurement_source: Optional[str] = Field(default=None, max_length=40)


class ResumeCreate(BaseModel):
    interview_id: Optional[int] = Field(default=None, gt=0)
    original_filename: str = Field(min_length=1, max_length=255)
    extracted_text: Optional[str] = None
    extracted_skills: Optional[list[str]] = None


class JobDescriptionCreate(BaseModel):
    interview_id: Optional[int] = Field(default=None, gt=0)
    title: Optional[str] = Field(default=None, max_length=255)
    company_name: Optional[str] = Field(default=None, max_length=255)
    description_text: str = Field(min_length=1)
    required_skills: Optional[list[str]] = None


# ----------------------------
# Validation helpers
# ----------------------------

def validate_interview(db: Session, interview_id: int) -> None:
    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if interview is None:
        raise HTTPException(
            status_code=404,
            detail=f"Interview {interview_id} was not found.",
        )


def validate_question(
    db: Session,
    interview_id: int,
    question_id: int,
) -> None:
    question = db.query(InterviewQuestion).filter(
        InterviewQuestion.id == question_id,
        InterviewQuestion.interview_id == interview_id,
    ).first()

    if question is None:
        raise HTTPException(
            status_code=404,
            detail="Question was not found in the specified interview.",
        )


def metric_to_dict(metric: CommunicationMetric) -> dict:
    return {
        "id": metric.id,
        "interview_id": metric.interview_id,
        "interview_question_id": metric.interview_question_id,
        "speaking_pace_wpm": metric.speaking_pace_wpm,
        "filler_word_count": metric.filler_word_count,
        "filler_word_rate": metric.filler_word_rate,
        "audio_duration_seconds": metric.audio_duration_seconds,
        "pause_count": metric.pause_count,
        "pause_duration_seconds": metric.pause_duration_seconds,
        "face_present": metric.face_present,
        "camera_gaze_metric": metric.camera_gaze_metric,
        "posture_metric": metric.posture_metric,
        "measurement_source": metric.measurement_source,
        "created_at": metric.created_at,
    }


def resume_to_dict(resume: ResumeRecord) -> dict:
    return {
        "id": resume.id,
        "interview_id": resume.interview_id,
        "original_filename": resume.original_filename,
        "extracted_skills": (
            json.loads(resume.extracted_skills)
            if resume.extracted_skills else None
        ),
        "created_at": resume.created_at,
    }


def job_description_to_dict(job: JobDescriptionRecord) -> dict:
    return {
        "id": job.id,
        "interview_id": job.interview_id,
        "title": job.title,
        "company_name": job.company_name,
        "description_text": job.description_text,
        "required_skills": (
            json.loads(job.required_skills)
            if job.required_skills else None
        ),
        "created_at": job.created_at,
    }


# ----------------------------
# Communication metrics
# ----------------------------

@router.post("/communication-metrics", status_code=201)
def create_communication_metric(
    payload: CommunicationMetricCreate,
    db: Session = Depends(get_db),
):
    validate_interview(db, payload.interview_id)

    if payload.interview_question_id is not None:
        validate_question(
            db,
            payload.interview_id,
            payload.interview_question_id,
        )

    metric = CommunicationMetric(
        interview_id=payload.interview_id,
        interview_question_id=payload.interview_question_id,
        speaking_pace_wpm=payload.speaking_pace_wpm,
        filler_word_count=payload.filler_word_count,
        filler_word_rate=payload.filler_word_rate,
        audio_duration_seconds=payload.audio_duration_seconds,
        pause_count=payload.pause_count,
        pause_duration_seconds=payload.pause_duration_seconds,
        face_present=payload.face_present,
        camera_gaze_metric=payload.camera_gaze_metric,
        posture_metric=payload.posture_metric,
        measurement_source=payload.measurement_source,
    )

    try:
        db.add(metric)
        db.commit()
        db.refresh(metric)
        return {"success": True, "metric": metric_to_dict(metric)}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save communication metrics.",
        )


@router.get("/interviews/{interview_id}/communication-metrics")
def get_communication_metrics(
    interview_id: int,
    db: Session = Depends(get_db),
):
    validate_interview(db, interview_id)

    metrics = (
        db.query(CommunicationMetric)
        .filter(CommunicationMetric.interview_id == interview_id)
        .order_by(CommunicationMetric.created_at.desc())
        .all()
    )

    return {
        "success": True,
        "count": len(metrics),
        "metrics": [metric_to_dict(item) for item in metrics],
    }


# ----------------------------
# Resume records
# ----------------------------

@router.post("/resumes", status_code=201)
def create_resume_record(
    payload: ResumeCreate,
    db: Session = Depends(get_db),
):
    if payload.interview_id is not None:
        validate_interview(db, payload.interview_id)

    resume = ResumeRecord(
        interview_id=payload.interview_id,
        original_filename=payload.original_filename,
        extracted_text=payload.extracted_text,
        extracted_skills=(
            json.dumps(payload.extracted_skills)
            if payload.extracted_skills is not None else None
        ),
    )

    try:
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return {"success": True, "resume": resume_to_dict(resume)}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save resume record.",
        )


@router.get("/resumes/{resume_id}")
def get_resume_record(
    resume_id: int,
    db: Session = Depends(get_db),
):
    resume = db.query(ResumeRecord).filter(
        ResumeRecord.id == resume_id
    ).first()

    if resume is None:
        raise HTTPException(status_code=404, detail="Resume record not found.")

    # Intentionally do not return the full extracted resume text.
    return {"success": True, "resume": resume_to_dict(resume)}


# ----------------------------
# Job-description records
# ----------------------------

@router.post("/job-descriptions", status_code=201)
def create_job_description(
    payload: JobDescriptionCreate,
    db: Session = Depends(get_db),
):
    if payload.interview_id is not None:
        validate_interview(db, payload.interview_id)

    job = JobDescriptionRecord(
        interview_id=payload.interview_id,
        title=payload.title,
        company_name=payload.company_name,
        description_text=payload.description_text,
        required_skills=(
            json.dumps(payload.required_skills)
            if payload.required_skills is not None else None
        ),
    )

    try:
        db.add(job)
        db.commit()
        db.refresh(job)
        return {
            "success": True,
            "job_description": job_description_to_dict(job),
        }
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save job-description record.",
        )


@router.get("/job-descriptions/{job_description_id}")
def get_job_description(
    job_description_id: int,
    db: Session = Depends(get_db),
):
    job = db.query(JobDescriptionRecord).filter(
        JobDescriptionRecord.id == job_description_id
    ).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job-description record not found.",
        )

    return {
        "success": True,
        "job_description": job_description_to_dict(job),
    }

