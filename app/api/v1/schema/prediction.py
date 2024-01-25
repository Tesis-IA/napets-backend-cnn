from pydantic import BaseModel


class Prediction(BaseModel):
    url_image: str
