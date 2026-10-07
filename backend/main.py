from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile

from fastapi import UploadFile, File, HTTPException
from speech_to_text import transcribe_audio


app = FastAPI(
    title="AI Interview Preparation & Evaluation System"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "AI Interview System backend is running"
    }


@app.post("/api/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No audio file provided."
        )

    temp_path = None

    try:
        audio_data = await file.read()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".webm"
        ) as temp_file:
            temp_file.write(audio_data)
            temp_path = temp_file.name

        transcript = transcribe_audio(temp_path)

        return {
            "success": True,
            "transcript": transcript
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)