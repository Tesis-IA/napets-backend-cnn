from pydantic import BaseModel


class Prediction(BaseModel):
    classes: str
