from faster_whisper import WhisperModel


print("Loading Whisper model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("Whisper model loaded.")


def transcribe_audio(file_path):

    segments, info = model.transcribe(
        file_path,
        beam_size=5
    )

    text_parts = []

    for segment in segments:
        text_parts.append(segment.text.strip())

    return " ".join(text_parts).strip()