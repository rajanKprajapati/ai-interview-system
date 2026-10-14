import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env")


client = genai.Client(api_key=api_key)


def generate_questions(interview_type, question_count):

    prompt = f"""
You are an expert technical interviewer.

Generate {question_count} realistic interview questions
for a {interview_type} interview.

The candidate is a B.Tech student and fresher.

Rules:
- Questions should be suitable for a fresher.
- Questions should be realistic interview questions.
- Do not provide answers.
- Return only the questions.
- Put each question on a separate line.
- Do not add numbering.
- Do not add explanations.
"""

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    text = interaction.output_text.strip()

    questions = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    return questions