from dataclasses import dataclass
from datetime import datetime

@dataclass
class SpeakingImage:
    _id: str
    image_url: str
    filename: str
    user_id: str | None = None
    created_at: datetime | None = None
    transcription: str | None = None # Just in case we want to add transcription to the image in the future for the LLM

@dataclass
class SpeakingImageCreate:
    image_url: str
    filename: str
    user_id: str | None = None
    created_at: datetime | None = None
    transcription: str | None = None # Just in case we want to add transcription to the image in the future for the LLM