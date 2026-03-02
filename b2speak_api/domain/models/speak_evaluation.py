from dataclasses import dataclass
from datetime import datetime

@dataclass
class SpeakEvaluation:
    _id: str
    audio_url: str
    audio_name: str
    selected_picture: str = "0"
    user_id: str | None = None
    state: str | None = None
    transcription: str | None = None
    result: str | None = None
    created_at: datetime | None = None


@dataclass
class SpeakEvaluationCreate:
    audio_url: str
    audio_name: str
    user_id: str | None = None
    selected_picture: str = "0"
    state: str = "UPLOADING"
    created_at: datetime | None = None
