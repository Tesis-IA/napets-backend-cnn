from app.api.v1.repository.prediction_repository import PredictionRepository
from app.api.v1.schema.prediction import Prediction


class PredictionService:
    prediction_repo = PredictionRepository()

    def get_prediction_image(self) -> Prediction:
        return self.prediction_repo.get_prediction_image()
