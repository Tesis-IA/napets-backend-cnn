from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.status import HTTP_200_OK

from app.api.v1.services.prediction_service import PredictionService

prediction_router = InferringRouter()


@cbv(prediction_router)
class PredictionController:
    prediction_service = PredictionService()

    @prediction_router.get('/prediction', status_code=HTTP_200_OK)
    def get_prediction(self):
        return self.prediction_service.get_prediction_image()
