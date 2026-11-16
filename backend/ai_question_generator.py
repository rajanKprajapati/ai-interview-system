from pathlib import Path
import os
import re
import json
from typing import Optional, List
from dotenv import load_dotenv
from google import genai

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in backend/.env")

client = genai.Client(api_key=api_key)


def generate_questions(
    interview_type: str = "technical",
    question_count: int = 5,
    difficulty: str = "intermediate",
    role: Optional[str] = None,
    subject: Optional[str] = None,
    resume_skills: Optional[List[str]] = None,
    skill_gaps: Optional[List[str]] = None,
    job_description: Optional[str] = None,
    resume_text: Optional[str] = None,
) -> List[str]:
    """
    Generates tailored interview questions using Gemini AI.
    Adapts to interview type, difficulty level, target role/subject,
    and optional resume skills / job description requirements.
    """
    valid_types = {"technical", "hr", "behavioral"}
    normalized_type = interview_type.lower() if interview_type else "technical"
    if normalized_type not in valid_types:
        normalized_type = "technical"

    difficulty_clean = (difficulty or "intermediate").lower()
    if difficulty_clean not in {"easy", "intermediate", "advanced"}:
        difficulty_clean = "intermediate"

    target_role = role.strip() if role and role.strip() else "Software Engineer"
    target_subject = f" specifically focusing on {subject.strip()}" if subject and subject.strip() else ""

    # Build context blocks if candidate supplied resume or JD
    context_lines = []
    if resume_skills:
        context_lines.append(f"- Candidate skills from resume: {', '.join(resume_skills)}")
    if skill_gaps:
        context_lines.append(f"- Identified skill gaps vs job description: {', '.join(skill_gaps)}")
    if job_description and job_description.strip():
        # Truncate JD to preserve token budget
        trimmed_jd = job_description.strip()[:1000]
        context_lines.append(f"- Target Job Description excerpt:\n{trimmed_jd}")

    context_str = "\n".join(context_lines)
    if context_str:
        context_str = f"\nCandidate & Role Context:\n{context_str}\n"

    # Type-specific guidance
    if normalized_type == "technical":
        type_guidance = (
            f"Focus on core computer science concepts, practical coding patterns, system design, "
            f"and hands-on problem solving relevant to a {target_role}{target_subject}. "
            f"Difficulty must be strictly '{difficulty_clean}': "
            f"{'fundamentals, clear definitions, and straightforward use cases' if difficulty_clean == 'easy' else 'practical trade-offs, internal mechanics, debugging, and real scenarios' if difficulty_clean == 'intermediate' else 'deep architectural trade-offs, edge cases, scalability, and complex performance optimization'}."
        )
    elif normalized_type == "hr":
        type_guidance = (
            f"Focus on candidate motivation, communication, cultural alignment, career growth, "
            f"work ethics, conflict resolution, and teamwork for a {target_role} position. "
            f"Difficulty: {difficulty_clean}."
        )
    else:  # behavioral
        type_guidance = (
            f"Focus on situational scenarios evaluated through the STAR framework (Situation, Task, Action, Result). "
            f"Ask about handling deadlines, leadership, disagreement with peers/managers, failure recovery, and initiative in a {target_role} role. "
            f"Difficulty: {difficulty_clean}."
        )

    prompt = f"""
You are an expert technical recruiter and interviewer conducting a {normalized_type.upper()} interview for the role of {target_role}.

Instructions:
1. Generate exactly {question_count} distinct, professional interview questions.
2. {type_guidance}
{context_str}
Formatting Rules:
- Return ONLY the questions, exactly one question per line.
- Do NOT include question numbering (e.g. no "1.", "2)", "Q1:").
- Do NOT include bullet points, intro text, answers, or explanations.
- Make each question clear, concise, and realistic.
""".strip()

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "thinking_config": {
                "thinking_level": "minimal"
            },
            "max_output_tokens": 800,
            "temperature": 0.7,
        },
    )

    text = (response.text or "").strip()

    # Parse questions lines
    raw_lines = text.splitlines()
    questions = []

    for line in raw_lines:
        cleaned = line.strip()
        if not cleaned:
            continue
        # Strip markdown bolding or quotes
        cleaned = cleaned.strip('"*\'')
        # Strip leading numbers or bullets like '1. ', '1) ', '- ', '* ', 'Q1: '
        cleaned = re.sub(r'^(?:Q\d+[:.]?|\d+[\.\)]\s*|[-*•]\s*)', '', cleaned).strip()
        if len(cleaned) > 10:
            questions.append(cleaned)

    if not questions:
        raise ValueError("Gemini returned no valid questions.")

    return questions[:question_count]
