from dataclasses import dataclass
from datetime import datetime


@dataclass(kw_only=True)
class Visit:
    id: int | None = None
    pet_id: int
    doctor_id: int
    start: datetime  # start of a 30-minute slot, see service/scheduling.py
    description: str
