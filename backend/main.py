import json

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Interview, InterviewQuestion

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
    answers: list[AnswerItem] = Field(min_length=1)
    development_mode: bool = False
    evaluations: list[dict] | None = None


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
def evaluate(
    request: EvaluationRequest,
    db: Session = Depends(get_db)
):
    try:
        answers = [
            {
                "question": item.question,
                "answer": item.answer
            }
            for item in request.answers
        ]

        # Development mode:
        # Use frontend-provided sample evaluations.
        # This avoids calling Gemini and consuming quota.
        if request.development_mode:
            if not request.evaluations:
                raise HTTPException(
                    status_code=400,
                    detail="Development mode requires evaluations."
                )

            evaluations = request.evaluations

            if len(evaluations) != len(answers):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Expected {len(answers)} evaluations, "
                        f"but received {len(evaluations)}."
                    )
                )

        # Production mode:
        # Ask Gemini to evaluate the answers.
        else:
            evaluations = evaluate_answers(answers)

        # Calculate overall interview score
        overall_scores = [
            float(evaluation["overall_score"])
            for evaluation in evaluations
        ]

        overall_score = round(
            sum(overall_scores) / len(overall_scores),
            2
        )

        # Create interview record
        interview = Interview(
            interview_type="technical",
            question_count=len(answers),
            overall_score=overall_score
        )

        db.add(interview)
        db.flush()

        # Create question/evaluation records
        for index, (answer, evaluation) in enumerate(
            zip(answers, evaluations),
            start=1
        ):
            question_record = InterviewQuestion(
                interview_id=interview.id,
                question_number=index,
                question=answer["question"],
                answer=answer["answer"],
                relevance=evaluation["relevance"],
                technical_accuracy=evaluation["technical_accuracy"],
                communication=evaluation["communication"],
                confidence=evaluation["confidence"],
                overall_score=evaluation["overall_score"],
                strengths=json.dumps(
                    evaluation["strengths"]
                ),
                weaknesses=json.dumps(
                    evaluation["weaknesses"]
                ),
                improvement_feedback=evaluation[
                    "improvement_feedback"
                ]
            )

            db.add(question_record)

        db.commit()
        db.refresh(interview)

        return {
            "success": True,
            "interview_id": interview.id,
            "overall_score": overall_score,
            "evaluations": evaluations
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()

        print(
            "ANSWER EVALUATION / DATABASE ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
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

