from typing import List

from pydantic import BaseModel


class PredictionResponse(BaseModel):
    filename: str
    content_type: str
    prediction: List[float] = []
    likely_class: int
