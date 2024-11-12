from pydantic import BaseModel
from typing import List


class MarkupResponse(BaseModel):
    class _Entity(BaseModel):
        start: int
        end: int
        label: str

    entities: List[_Entity] | None
    text_labels: List[str]
