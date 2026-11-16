"""Add-on services for phases 7, 8 and 11 of AI Interview System.

Designed to work alongside the existing FastAPI/SQLAlchemy application.
Does not replace main.py, models.py, or the existing interview workflow.
"""
from __future__ import annotations

import io
import re
from collections import Counter
from typing import Any

FILLER_TERMS = {
    "um", "uh", "erm", "hmm", "like", "basically", "actually",
    "literally", "you know", "i mean", "sort of", "kind of",
}

SKILL_TERMS = [
    "python", "java", "c++", "sql", "postgresql", "mysql", "excel",
    "power bi", "tableau", "pandas", "numpy", "matplotlib", "machine learning",
    "deep learning", "fastapi", "react", "javascript", "html", "css",
    "data analysis", "statistics", "aws", "azure", "git", "docker",
]

def analyze_transcript(transcript: str, duration_seconds: float | None = None) -> dict[str, Any]:
    """Compute transparent transcript-based indicators; no psychological diagnosis.

    Speaking pace is only calculated when a valid recording duration is supplied.
    """
    clean = (transcript or "").strip()
    words = re.findall(r"\b[\w+#.']+\b", clean.lower())
    word_count = len(words)

    # Match multi-word fillers first, then single-word fillers.
    lower_text = re.sub(r"\s+", " ", clean.lower())
    filler_counts = {}
    for term in sorted(FILLER_TERMS, key=len, reverse=True):
        pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
        count = len(re.findall(pattern, lower_text))
        if count:
            filler_counts[term] = count

    pace = None
    pace_label = "Not measured"
    if duration_seconds and duration_seconds > 0:
        pace = round(word_count / (duration_seconds / 60), 1)
        if pace < 100:
            pace_label = "Slow"
        elif pace <= 160:
            pace_label = "Typical range"
        else:
            pace_label = "Fast"

    filler_total = sum(filler_counts.values())
    filler_rate = round((filler_total / max(word_count, 1)) * 100, 1)

    if filler_rate <= 1:
        filler_label = "Low"
    elif filler_rate <= 3:
        filler_label = "Moderate"
    else:
        filler_label = "Frequent"

    return {
        "word_count": word_count,
        "duration_seconds": round(duration_seconds, 2) if duration_seconds else None,
        "speaking_pace_wpm": pace,
        "speaking_pace_label": pace_label,
        "filler_word_count": filler_total,
        "filler_word_breakdown": filler_counts,
        "filler_rate_percent": filler_rate,
        "filler_label": filler_label,
        "interpretation": (
            "These are observable communication indicators, not a definitive measure "
            "of confidence, personality, or interview suitability."
        ),
    }


def extract_resume_text(pdf_bytes: bytes, max_chars: int = 100_000) -> str:
    """Extract text from a text-based PDF using pypdf."""
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("Install pypdf: pip install pypdf") from exc

    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")
    if len(pdf_bytes) > 10 * 1024 * 1024:
        raise ValueError("Resume PDF exceeds the 10 MB limit.")

    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        if getattr(reader, "is_encrypted", False):
            raise ValueError("Encrypted PDFs are not supported. Upload an unlocked PDF.")
        pages = []
        for page in reader.pages[:20]:
            pages.append(page.extract_text() or "")
        text = "\n".join(pages).strip()
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("Could not read this PDF. Try exporting the resume as a text-based PDF.") from exc

    if not text:
        raise ValueError("No selectable text was found. This may be a scanned PDF; OCR is not configured.")
    return text[:max_chars]


def extract_known_skills(text: str) -> list[str]:
    lower = (text or "").lower()
    found = []
    for skill in SKILL_TERMS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])"
        if re.search(pattern, lower):
            found.append(skill)
    return sorted(set(found))


def build_resume_jd_profile(resume_text: str, job_description: str) -> dict[str, Any]:
    """Return transparent skill overlap plus source text for AI question generation."""
    if not (resume_text or "").strip():
        raise ValueError("Resume text is required.")
    if not (job_description or "").strip():
        raise ValueError("Job description is required.")

    resume_skills = extract_known_skills(resume_text)
    jd_skills = extract_known_skills(job_description)
    resume_set, jd_set = set(resume_skills), set(jd_skills)

    return {
        "resume_skills": resume_skills,
        "job_required_skills": jd_skills,
        "matched_skills": sorted(resume_set & jd_set),
        "possible_skill_gaps": sorted(jd_set - resume_set),
        "resume_text": resume_text[:20_000],
        "job_description": job_description[:12_000],
        "note": "Skill extraction uses a configurable keyword list; review results before relying on them."
    }


def make_personalized_feedback(evaluations: list[dict[str, Any]], communication_metrics: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build actionable, explainable feedback from stored evaluation values and visual telemetry."""
    evaluations = evaluations or []
    strengths, weaknesses = [], []
    score_fields = [
        ("relevance", "answer relevance"),
        ("technical_accuracy", "technical accuracy"),
        ("communication", "communication clarity"),
    ]

    for field, label in score_fields:
        scores = [float(e[field]) for e in evaluations if isinstance(e.get(field), (int, float))]
        if scores:
            avg = sum(scores) / len(scores)
            if avg >= 7.5:
                strengths.append(f"Strong {label} (average {avg:.1f}/10).")
            elif avg < 6:
                weaknesses.append(f"Improve {label} (average {avg:.1f}/10).")

    recommendations = []
    if any("technical accuracy" in item.lower() for item in weaknesses):
        recommendations.append("Review core concepts and practise explaining each concept with a concrete example.")
    if any("relevance" in item.lower() for item in weaknesses):
        recommendations.append("Answer the exact question first, then add a short explanation and example.")
    if any("communication" in item.lower() for item in weaknesses):
        recommendations.append("Use a structured framework: direct answer, technical explanation, concrete example.")

    if communication_metrics:
        filler_label = communication_metrics.get("filler_label")
        if filler_label == "Frequent":
            recommendations.append("Practise pausing silently for 1–2 seconds instead of using repeated filler words.")
        pace_label = communication_metrics.get("speaking_pace_label")
        if pace_label == "Fast":
            recommendations.append("Try shorter sentences and slow down slightly to achieve optimal conversational pacing (120–160 WPM).")
        elif pace_label == "Slow":
            recommendations.append("Practise concise answers with a clear beginning, middle, and end to improve speaking tempo.")

        # Behavioral & Visual recommendations
        visual = communication_metrics.get("visual_indicators") or {}
        gaze = visual.get("camera_gaze_metric")
        if gaze is not None and gaze < 55:
            recommendations.append("Position your webcam at eye level and aim for consistent gaze towards the lens to enhance audience engagement.")
        posture = visual.get("posture", {}).get("status", "")
        if "slouching" in posture.lower() or "lean" in posture.lower():
            recommendations.append("Maintain an upright, centered sitting posture to project composure throughout longer responses.")

    if not recommendations:
        recommendations.append("Consistent performance observed! Practise explaining advanced architecture trade-offs for competitive placement rounds.")

    return {
        "strengths": strengths or ["Demonstrated solid foundational readiness."],
        "weaknesses": weaknesses or ["No major low-scoring category was identified by the evaluation rubric."],
        "recommended_practice": recommendations,
        "disclaimer": "Feedback is synthesized from recorded answer scores, speech tempo, and observable camera engagement; it is not a psychological or personality assessment."
    }
