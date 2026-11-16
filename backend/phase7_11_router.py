"""Optional Phase 7/8/11 FastAPI router.

Register with:
    from phase7_11_router import router as phase7_11_router
    app.include_router(phase7_11_router)

This router intentionally does not persist resumes or metrics yet. It provides a safe
working starting point; add persistence after reviewing the existing DB schema.
"""
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from phase7_11_services import (
    analyze_transcript,
    build_resume_jd_profile,
    extract_resume_text,
    make_personalized_feedback,
)

router = APIRouter(prefix="/api", tags=["Phase 7-11 add-ons"])


class ConfidenceRequest(BaseModel):
    transcript: str = Field(min_length=1, max_length=100_000)
    duration_seconds: float | None = Field(default=None, gt=0, le=3600)


class FeedbackRequest(BaseModel):
    evaluations: list[dict] = Field(default_factory=list)
    communication_metrics: dict | None = None


@router.post("/confidence/analyze")
def confidence_analyze(payload: ConfidenceRequest):
    try:
        return {"success": True, "metrics": analyze_transcript(payload.transcript, payload.duration_seconds)}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/resume/profile")
async def resume_profile(
    resume: UploadFile = File(...),
    job_description: str = Form(..., min_length=20, max_length=20_000),
):
    if resume.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(status_code=415, detail="Upload a PDF resume.")
    try:
        data = await resume.read()
        resume_text = extract_resume_text(data)
        profile = build_resume_jd_profile(resume_text, job_description)
        # Do not echo full resume/JD text to the client by default.
        return {
            "success": True,
            "resume_skills": profile["resume_skills"],
            "job_required_skills": profile["job_required_skills"],
            "matched_skills": profile["matched_skills"],
            "possible_skill_gaps": profile["possible_skill_gaps"],
            "note": profile["note"],
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Resume processing failed.") from exc


@router.post("/feedback/personalized")
def personalized_feedback(payload: FeedbackRequest):
    return {
        "success": True,
        "feedback": make_personalized_feedback(
            payload.evaluations,
            payload.communication_metrics
        )
    }
