import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in backend/.env")

client = genai.Client(api_key=api_key)


def generate_questions(interview_type: str, question_count: int):
    prompt = f"""
You are an expert interview interviewer.

Generate exactly {question_count} interview questions for a
{interview_type} interview.

Candidate:
- B.Tech student
- Fresher
- Preparing for campus placement

Interview type: {interview_type}

Rules:
- Questions must be realistic.
- Questions must be suitable for a fresher.
- Do not provide answers.
- Do not provide explanations.
- Do not add numbering.
- Return exactly one question per line.
"""

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    text = response.output_text.strip()

    questions = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        # Remove common numbering if Gemini adds it anyway.
        if line[0:2].isdigit() and line[2:3] in [".", ")"]:
            line = line[3:].strip()
        elif len(line) >= 2 and line[0].isdigit() and line[1] in [".", ")"]:
            line = line[2:].strip()

        if line:
            questions.append(line)

    return questions[:question_count]