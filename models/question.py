from dataclasses import dataclass
from typing import Optional

@dataclass
class Question:
    subject: str
    section: str
    question: str
    marks: int
    answer: Optional[str] = None 