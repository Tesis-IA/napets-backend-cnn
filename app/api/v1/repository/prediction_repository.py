from api.v1.schema.prediction import Prediction


class PredictionRepository:

    def get_prediction_image(self) -> Prediction:
        prediction = Prediction(
            classes="Healthy"
        )
        return prediction
