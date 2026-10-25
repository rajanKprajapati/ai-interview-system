import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set in backend/.env"
    )


client = genai.Client(api_key=api_key)


def evaluate_answers(answers):
    formatted_answers = []

    for index, item in enumerate(answers, start=1):
        question = item.get("question", "").strip()
        answer = item.get("answer", "").strip()

        formatted_answers.append(
            f"""
Question {index}:
{question}

Candidate Answer:
{answer}
"""
        )

    interview_content = "\n---\n".join(
        formatted_answers
    )

    prompt = f"""
You are an expert AI interview evaluator.

Evaluate the complete interview of a B.Tech fresher preparing for campus placement.

Here are the interview questions and candidate answers:

{interview_content}

For every question, evaluate the candidate using these criteria:

1. Relevance
2. Technical Accuracy
3. Communication
4. Confidence
5. Overall Score

Each score must be between 0 and 10.

Also provide:

- strengths
- weaknesses
- improvement_feedback

Return ONLY valid JSON.

Use exactly this structure:

{{
    "evaluations": [
        {{
            "question_number": 1,
            "relevance": 0,
            "technical_accuracy": 0,
            "communication": 0,
            "confidence": 0,
            "overall_score": 0,
            "strengths": [],
            "weaknesses": [],
            "improvement_feedback": ""
        }}
    ]
}}

Rules:

- Return exactly one evaluation for every question.
- Keep the same question order.
- question_number must match the question number.
- All scores must be numbers from 0 to 10.
- strengths must be an array of short strings.
- weaknesses must be an array of short strings.
- improvement_feedback must be a short paragraph.
- Do not skip any question.
- Do not add extra fields.
- Do not include markdown.
- Do not include ```json.
- Return only JSON.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "thinking_config": {
                "thinking_level": "minimal"
            },
            "max_output_tokens": 2500,
        },
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    try:
        result = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Gemini returned invalid evaluation JSON: {text}"
        ) from e

    if not isinstance(result, dict):
        raise ValueError(
            "Gemini evaluation response is not a JSON object."
        )

    evaluations = result.get("evaluations")

    if not isinstance(evaluations, list):
        raise ValueError(
            "Gemini response is missing evaluations."
        )

    if len(evaluations) != len(answers):
        raise ValueError(
            f"Expected {len(answers)} evaluations, "
            f"but Gemini returned {len(evaluations)}."
        )

    required_fields = [
        "question_number",
        "relevance",
        "technical_accuracy",
        "communication",
        "confidence",
        "overall_score",
        "strengths",
        "weaknesses",
        "improvement_feedback",
    ]

    for index, evaluation in enumerate(
        evaluations,
        start=1
    ):
        if not isinstance(evaluation, dict):
            raise ValueError(
                f"Evaluation {index} is not a valid object."
            )

        for field in required_fields:
            if field not in evaluation:
                raise ValueError(
                    f"Evaluation {index} is missing field: {field}"
                )

        score_fields = [
            "relevance",
            "technical_accuracy",
            "communication",
            "confidence",
            "overall_score",
        ]

        for field in score_fields:
            score = evaluation[field]

            if not isinstance(score, (int, float)):
                raise ValueError(
                    f"Evaluation {index} field '{field}' "
                    "must be a number."
                )

            if score < 0 or score > 10:
                raise ValueError(
                    f"Evaluation {index} field '{field}' "
                    "must be between 0 and 10."
                )

        if not isinstance(
            evaluation["strengths"],
            list
        ):
            raise ValueError(
                f"Evaluation {index} strengths must be a list."
            )

        if not isinstance(
            evaluation["weaknesses"],
            list
        ):
            raise ValueError(
                f"Evaluation {index} weaknesses must be a list."
            )

        if not isinstance(
            evaluation["improvement_feedback"],
            str
        ):
            raise ValueError(
                f"Evaluation {index} improvement_feedback "
                "must be a string."
            )

    return evaluations

