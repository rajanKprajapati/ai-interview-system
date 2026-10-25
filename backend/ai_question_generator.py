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
Generate exactly {question_count} interview questions for a {interview_type} interview.

Candidate: B.Tech fresher preparing for campus placement.

Return ONLY the questions, one per line.
No numbering.
No answers.
No explanations.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "thinking_config": {
                "thinking_level": "minimal"
            },
            "max_output_tokens": 300,
        },
    )

    text = response.text.strip()

    questions = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        # Remove numbering such as 1. or 1)
        if len(line) >= 2 and line[0].isdigit() and line[1] in [".", ")"]:
            line = line[2:].strip()

        if line:
            questions.append(line)

    if not questions:
        raise ValueError("Gemini returned no questions.")

    return questions[:question_count]