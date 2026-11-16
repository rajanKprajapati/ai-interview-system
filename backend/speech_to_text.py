from typing import Union, Dict, Any
from faster_whisper import WhisperModel


print("Loading Whisper model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("Whisper model loaded.")


def transcribe_audio(
    file_path: str,
    return_metadata: bool = False
) -> Union[str, Dict[str, Any]]:
    """
    Transcribes audio using faster-whisper.
    If return_metadata is True, returns dictionary with transcript, duration, and language.
    Otherwise returns the transcript string directly for backward compatibility.
    """
    segments, info = model.transcribe(
        file_path,
        beam_size=5,
    )

    text_parts = []
    for segment in segments:
        text_parts.append(segment.text.strip())

    transcript = " ".join(text_parts).strip()

    if return_metadata:
        duration = getattr(info, "duration", None)
        return {
            "transcript": transcript,
            "duration_seconds": round(duration, 2) if duration is not None else None,
            "language": getattr(info, "language", "en"),
        }

    return transcript
