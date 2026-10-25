import os
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ai_question_generator import generate_questions
from ai_evaluator import evaluate_answers
from speech_to_text import transcribe_audio


app = FastAPI(
    title="AI Interview Preparation & Evaluation System",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    interview_type: str = Field(
        pattern="^(technical|hr|behavioral)$"
    )

    question_count: int = Field(
        ge=1,
        le=10
    )


class AnswerItem(BaseModel):
    question: str = Field(
        min_length=1
    )

    answer: str = Field(
        min_length=1
    )


class EvaluationRequest(BaseModel):
    answers: list[AnswerItem] = Field(
        min_length=1
    )


@app.get("/")
def root():
    return {
        "success": True,
        "message": "AI Interview System Backend is running"
    }


@app.get("/api/health")
def health():
    return {
        "success": True,
        "status": "healthy"
    }


@app.post("/api/questions")
def get_questions(request: QuestionRequest):
    try:
        questions = generate_questions(
            request.interview_type,
            request.question_count
        )

        if not questions:
            raise HTTPException(
                status_code=502,
                detail="AI provider returned no questions."
            )

        return {
            "success": True,
            "interview_type": request.interview_type,
            "question_count": len(questions),
            "questions": questions
        }

    except HTTPException:
        raise

    except Exception as e:
        print(
            "QUESTION GENERATION ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=502,
            detail=f"Question generation failed: {str(e)}"
        )


@app.post("/api/evaluate")
def evaluate(request: EvaluationRequest):
    try:
        answers = [
            {
                "question": item.question,
                "answer": item.answer
            }
            for item in request.answers
        ]

        evaluations = evaluate_answers(
            answers
        )

        return {
            "success": True,
            "evaluations": evaluations
        }

    except HTTPException:
        raise

    except Exception as e:
        print(
            "ANSWER EVALUATION ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=502,
            detail=f"Answer evaluation failed: {str(e)}"
        )


@app.post("/api/transcribe")
async def transcribe(
    file: UploadFile = File(...)
):
    temp_path = None

    try:
        suffix = os.path.splitext(
            file.filename or ""
        )[1]

        if not suffix:
            suffix = ".webm"

        audio_data = await file.read()

        if not audio_data:
            raise HTTPException(
                status_code=400,
                detail="Uploaded audio file is empty."
            )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(audio_data)
            temp_path = temp_file.name

        transcript = transcribe_audio(
            temp_path
        )

        return {
            "success": True,
            "transcript": transcript
        }

    except HTTPException:
        raise

    except Exception as e:
        print(
            "TRANSCRIPTION ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Speech-to-text failed."
        )

    finally:
        if temp_path and os.path.exists(
            temp_path
        ):
            try:
                os.remove(temp_path)
            except Exception:
                pass

