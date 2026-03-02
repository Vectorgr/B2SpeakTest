from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    _id: str
    name: str
    email: str
    hashed_password: str
    created_at: datetime | None = None


@dataclass
class UserCreate:
    name: str
    email: str
    hashed_password: str
    created_at: datetime | None = None
